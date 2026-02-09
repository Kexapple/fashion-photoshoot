"""
Response models and schemas
"""

from pydantic import BaseModel
from typing import List, Optional


class GenerateResponse(BaseModel):
    """Response from generation request"""
    shoot_id: str
    status: str  # "completed" | "failed"
    generatedImages: List[str]
    creditsCost: int
    creditsRemaining: int


class UserProfileResponse(BaseModel):
    """User profile response"""
    uid: str
    email: str
    displayName: str
    credits: int
    plan: str  # "free" | "starter" | "pro"
    firstLoginBonusUsed: bool
    createdAt: str


class CreditsResponse(BaseModel):
    """Credits balance response"""
    credits: int
    plan: str
    firstLoginBonusUsed: bool
    anonTrialRemaining: Optional[int] = None  # For anonymous users


class PurchaseResponse(BaseModel):
    """Credit purchase response"""
    status: str  # "success" | "failed"
    creditsAdded: int
    newBalance: int
    transactionId: str
    message: str


class TokenVerificationResponse(BaseModel):
    """Token verification response"""
    valid: bool
    uid: str
    email: str
    displayName: str


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    code: str
    status_code: int
