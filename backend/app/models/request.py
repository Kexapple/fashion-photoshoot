"""
Request models and schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class GenerateRequest(BaseModel):
    """Request to generate photoshoot"""
    idToken: str = Field(..., description="Firebase ID token for authenticated users")
    articleType: str = Field(..., description="Type of article (shirt, dress, pants, etc.)")
    styleNotes: Optional[str] = Field(None, description="Optional style notes")
    imageSize: str = Field(..., description="Output size: small, medium, large")
    uploadedImageUrls: List[str] = Field(..., description="URLs of uploaded reference images")
    clientIp: Optional[str] = Field(None, description="Client IP address for anonymous tracking")


class RegisterRequest(BaseModel):
    """Request to register new user"""
    idToken: str = Field(..., description="Firebase ID token")
    email: str = Field(..., description="User email")
    displayName: str = Field(..., description="User display name")
    ipAddress: Optional[str] = Field(None, description="Client IP for tracking")


class PurchaseCreditsRequest(BaseModel):
    """Request to purchase credits"""
    idToken: str = Field(..., description="Firebase ID token")
    amount: int = Field(..., description="Number of credits to purchase")
    paymentMethod: str = Field(..., description="jazzcash or easypaisa")
    phoneNumber: str = Field(..., description="Phone number for payment")
    transactionId: str = Field(..., description="Payment provider transaction ID")


class VerifyTokenRequest(BaseModel):
    """Request to verify Firebase token"""
    idToken: str = Field(..., description="Firebase ID token")
