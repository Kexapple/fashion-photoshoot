"""
Credits management routes
"""

from fastapi import APIRouter, HTTPException, Request
import logging

from app.models.request import PurchaseCreditsRequest
from app.models.response import CreditsResponse, PurchaseResponse
from app.services.auth import AuthService
from app.services.firestore import FirestoreService
from app.services.payment import PaymentVerificationService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/user/credits")
async def get_user_credits(id_token: str):
    """
    Get user's current credit balance
    
    Fetches from server to prevent frontend tampering
    """
    try:
        uid = AuthService.get_uid_from_token(id_token)
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_data = FirestoreService.get_user(uid)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return CreditsResponse(
            credits=user_data.get("credits", 0),
            plan=user_data.get("plan", "free"),
            firstLoginBonusUsed=user_data.get("firstLoginBonusUsed", False),
            anonTrialRemaining=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching credits: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch credits")


@router.get("/anon/trial-status")
async def get_anon_trial_status(request: Request):
    """
    Get anonymous user's free trial status
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        
        trial_status = FirestoreService.check_anon_trial(client_ip)
        
        return {
            "eligible": trial_status.get("eligible"),
            "generationCount": trial_status.get("generationCount"),
            "remaining": settings.FREE_TRIAL_LIMIT - trial_status.get("generationCount", 0),
            "totalLimit": settings.FREE_TRIAL_LIMIT,
            "status": trial_status.get("status")
        }
    except Exception as e:
        logger.error(f"Error fetching trial status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trial status")


@router.post("/credits/purchase")
async def purchase_credits(request: PurchaseCreditsRequest):
    """
    Process credit purchase via Pakistani payment methods
    
    Validates payment with JazzCash or EasyPaisa API
    Credits only added after successful verification
    """
    try:
        # Verify token
        uid = AuthService.get_uid_from_token(request.idToken)
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Verify user exists
        user_data = FirestoreService.get_user(uid)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify payment based on method
        payment_method = request.paymentMethod.lower()
        
        if payment_method == "jazzcash":
            verification = PaymentVerificationService.verify_jazzcash_payment(
                transaction_id=request.transactionId,
                amount=0,  # Amount calculated from transaction
                phone_number=request.phoneNumber
            )
        elif payment_method == "easypaisa":
            verification = PaymentVerificationService.verify_easypaisa_payment(
                transaction_id=request.transactionId,
                amount=0,
                phone_number=request.phoneNumber
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid payment method")
        
        if not verification.get("verified"):
            logger.warning(f"Payment verification failed for user {uid}: {verification.get('message')}")
            raise HTTPException(
                status_code=402,
                detail=verification.get("message", "Payment verification failed")
            )
        
        # Calculate credits based on amount
        amount = verification.get("amount", request.amount)
        credits_to_add = PaymentVerificationService.calculate_credits_for_amount(amount)
        
        # Add credits to user account
        success = FirestoreService.add_credits(
            uid=uid,
            amount=credits_to_add,
            reason="purchase",
            payment_method=payment_method
        )
        
        if not success:
            logger.error(f"Failed to add credits for user {uid}")
            raise HTTPException(status_code=500, detail="Failed to process credits")
        
        # Get updated balance
        updated_user = FirestoreService.get_user(uid)
        new_balance = updated_user.get("credits", 0) if updated_user else 0
        
        logger.info(f"Credit purchase successful: {uid} purchased {credits_to_add} credits")
        
        return PurchaseResponse(
            status="success",
            creditsAdded=credits_to_add,
            newBalance=new_balance,
            transactionId=request.transactionId,
            message=f"Successfully added {credits_to_add} credits to your account"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Credit purchase error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Purchase processing failed")


@router.get("/credits/packages")
async def get_credit_packages():
    """
    Get available credit package options
    
    Used by frontend to display purchase options
    """
    packages = [
        {
            "id": "pkg_10",
            "credits": 10,
            "priceInPkr": 50,
            "savings": 0,
            "featured": False
        },
        {
            "id": "pkg_25",
            "credits": 25,
            "priceInPkr": 125,
            "savings": 0,
            "featured": True
        },
        {
            "id": "pkg_50",
            "credits": 50,
            "priceInPkr": 250,
            "savings": 0,
            "featured": False
        },
        {
            "id": "pkg_100",
            "credits": 100,
            "priceInPkr": 500,
            "savings": 0,
            "featured": False
        }
    ]
    
    return {"packages": packages}
