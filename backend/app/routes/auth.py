"""
Authentication routes
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Optional
import logging

from app.models.request import RegisterRequest, VerifyTokenRequest
from app.models.response import UserProfileResponse, TokenVerificationResponse
from app.services.auth import AuthService
from app.services.firestore import FirestoreService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/verify")
async def verify_token(request: VerifyTokenRequest):
    """
    Verify Firebase ID token
    
    Returns user information if token is valid
    """
    decoded = AuthService.verify_id_token(request.idToken)
    
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    uid = decoded.get("uid")
    email = decoded.get("email")
    display_name = decoded.get("name", "User")
    
    return TokenVerificationResponse(
        valid=True,
        uid=uid,
        email=email,
        displayName=display_name
    )


@router.post("/register")
async def register_user(request: RegisterRequest, req: Request):
    """
    Register or create new user after Firebase authentication
    
    Automatically grants first-login bonus of 5 credits
    """
    try:
        # Verify token
        decoded = AuthService.verify_id_token(request.idToken)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        uid = decoded.get("uid")
        
        # Check if user already exists
        existing_user = FirestoreService.get_user(uid)
        if existing_user:
            # User already registered
            return {
                "status": "user_exists",
                "credits": existing_user.get("credits", 0),
                "firstLoginBonusUsed": existing_user.get("firstLoginBonusUsed", False)
            }
        
        # Get client IP
        client_ip = request.client.host if request.client else None
        
        # Create new user with first-login bonus
        user_data = FirestoreService.create_user(
            uid=uid,
            email=request.email,
            display_name=request.displayName,
            ip_address=client_ip
        )
        
        logger.info(f"New user registered: {uid} ({request.email})")
        
        return {
            "status": "registered",
            "uid": uid,
            "email": request.email,
            "displayName": request.displayName,
            "credits": user_data.get("credits", 5),
            "firstLoginBonusUsed": user_data.get("firstLoginBonusUsed", True),
            "message": "Welcome! You received 5 free credits."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed")


@router.get("/user/profile")
async def get_user_profile(id_token: str):
    """Get user profile information"""
    try:
        uid = AuthService.get_uid_from_token(id_token)
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_data = FirestoreService.get_user(uid)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserProfileResponse(
            uid=uid,
            email=user_data.get("email"),
            displayName=user_data.get("displayName"),
            credits=user_data.get("credits", 0),
            plan=user_data.get("plan", "free"),
            firstLoginBonusUsed=user_data.get("firstLoginBonusUsed", False),
            createdAt=user_data.get("createdAt")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")
