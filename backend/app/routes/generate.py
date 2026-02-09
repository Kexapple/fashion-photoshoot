"""
Image generation routes
Handles both anonymous and authenticated photoshoot generation
"""

from fastapi import APIRouter, HTTPException, Request
import uuid
import logging
from datetime import datetime

from app.models.request import GenerateRequest
from app.models.response import GenerateResponse
from app.services.auth import AuthService
from app.services.firestore import FirestoreService
from app.services.nano_banana import GenerationService
from app.services.storage import StorageService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/photoshoots/create")
async def create_photoshoot(request: GenerateRequest, req: Request):
    """
    Create and generate a photoshoot
    
    Handles both anonymous users (free trial) and authenticated users (credit-based)
    
    Returns:
        - 200: Generation successful
        - 402: Insufficient credits
        - 401: Invalid token
        - 400: Bad request
        - 500: Generation failed
    """
    try:
        client_ip = req.client.host if req.client else "unknown"
        shoot_id = str(uuid.uuid4())
        
        # Determine if user is authenticated
        is_authenticated = bool(request.idToken)
        
        if is_authenticated:
            # Authenticated user - check credits
            return await _handle_authenticated_generation(
                request, shoot_id, client_ip
            )
        else:
            # Anonymous user - check free trial
            return await _handle_anonymous_generation(
                request, shoot_id, client_ip
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Generation failed")


async def _handle_authenticated_generation(request: GenerateRequest, shoot_id: str, client_ip: str):
    """Handle generation for authenticated users (credit-based)"""
    
    # Verify token
    uid = AuthService.get_uid_from_token(request.idToken)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Check user exists
    user_data = FirestoreService.get_user(uid)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate credit cost (1 credit per image)
    credit_cost = 1  # Fixed cost: 1 credit per generation
    
    # Check credit balance
    current_credits = user_data.get("credits", 0)
    if current_credits < credit_cost:
        logger.warning(f"Insufficient credits for user {uid}: {current_credits} < {credit_cost}")
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient credits. You have {current_credits}, need {credit_cost}"
        )
    
    # Lock credits (attempt deduction - will fail if insufficient in transaction)
    logger.info(f"Generating photoshoot for user {uid}: {request.articleType}")
    
    # Call generation service
    generation_result = GenerationService.generate_photoshoot(
        reference_images=request.uploadedImageUrls,
        article_type=request.articleType,
        style_notes=request.styleNotes or "",
        image_size=request.imageSize
    )
    
    if not generation_result.get("success"):
        logger.error(f"Generation failed: {generation_result.get('message')}")
        raise HTTPException(status_code=500, detail=generation_result.get("message"))
    
    # Save generated images to Firebase Storage
    generated_images = generation_result.get("images", [])
    
    # For now, we just store the image URLs/data returned from API
    # In production, you might want to upload to Firebase Storage and get permanent URLs
    
    # Deduct credits (atomic transaction)
    deduction_success = FirestoreService.deduct_credits(uid, credit_cost, shoot_id)
    
    if not deduction_success:
        logger.error(f"Failed to deduct credits for user {uid}")
        raise HTTPException(status_code=500, detail="Failed to process credits")
    
    # Save photoshoot record
    FirestoreService.save_photoshoot(uid, {
        "articleType": request.articleType,
        "styleNotes": request.styleNotes,
        "imageSize": request.imageSize,
        "uploadedImages": request.uploadedImageUrls,
        "generatedImages": generated_images,
        "creditsCost": credit_cost,
        "isFreeTrial": False,
        "status": "completed"
    })
    
    # Get updated credits
    new_credits = FirestoreService.get_credits(uid)
    
    logger.info(f"Generation completed for user {uid}. Credits: {new_credits}")
    
    return GenerateResponse(
        shoot_id=shoot_id,
        status="completed",
        generatedImages=generated_images,
        creditsCost=credit_cost,
        creditsRemaining=new_credits or 0
    )


async def _handle_anonymous_generation(request: GenerateRequest, shoot_id: str, client_ip: str):
    """Handle generation for anonymous users (3-image free trial per IP)"""
    
    # Check anonymous trial status
    trial_status = FirestoreService.check_anon_trial(client_ip)
    
    if not trial_status.get("eligible"):
        logger.warning(f"Anonymous trial exhausted for IP {client_ip}")
        raise HTTPException(
            status_code=402,
            detail="Free trial limit reached (3 images). Please log in to continue."
        )
    
    logger.info(f"Anonymous generation for IP {client_ip}: {request.articleType}")
    
    # Call generation service
    generation_result = GenerationService.generate_photoshoot(
        reference_images=request.uploadedImageUrls,
        article_type=request.articleType,
        style_notes=request.styleNotes or "",
        image_size=request.imageSize
    )
    
    if not generation_result.get("success"):
        logger.error(f"Generation failed: {generation_result.get('message')}")
        raise HTTPException(status_code=500, detail=generation_result.get("message"))
    
    generated_images = generation_result.get("images", [])
    
    # Increment anonymous trial counter
    count = FirestoreService.increment_anon_trial(client_ip)
    
    # Create anon user identifier
    ip_hash = FirestoreService.hash_ip(client_ip)
    anon_uid = f"anon-{ip_hash}"
    
    # Save photoshoot record
    FirestoreService.save_photoshoot(anon_uid, {
        "articleType": request.articleType,
        "styleNotes": request.styleNotes,
        "imageSize": request.imageSize,
        "uploadedImages": request.uploadedImageUrls,
        "generatedImages": generated_images,
        "creditsCost": 0,
        "isFreeTrial": True,
        "status": "completed"
    })
    
    remaining_free = settings.FREE_TRIAL_LIMIT - count
    
    logger.info(f"Anonymous generation completed. Trial usage: {count}/{settings.FREE_TRIAL_LIMIT}")
    
    return GenerateResponse(
        shoot_id=shoot_id,
        status="completed",
        generatedImages=generated_images,
        creditsCost=0,
        creditsRemaining=remaining_free  # For anonymous, show remaining free generations
    )
