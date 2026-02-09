"""
Authentication and Firebase token validation
"""

import firebase_admin
from firebase_admin import credentials, auth
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class AuthService:
    """Firebase authentication service"""
    
    @staticmethod
    def verify_id_token(id_token: str) -> Optional[dict]:
        """
        Verify Firebase ID token
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Decoded token dict with user info, or None if invalid
        """
        try:
            decoded = auth.verify_id_token(id_token)
            logger.info(f"Token verified for user: {decoded.get('email')}")
            return decoded
        except auth.InvalidIdTokenError:
            logger.warning("Invalid ID token")
            return None
        except auth.ExpiredIdTokenError:
            logger.warning("Expired ID token")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return None
    
    @staticmethod
    def get_uid_from_token(id_token: str) -> Optional[str]:
        """Extract user ID from Firebase token"""
        decoded = AuthService.verify_id_token(id_token)
        return decoded.get("uid") if decoded else None
    
    @staticmethod
    def get_email_from_token(id_token: str) -> Optional[str]:
        """Extract email from Firebase token"""
        decoded = AuthService.verify_id_token(id_token)
        return decoded.get("email") if decoded else None
    
    @staticmethod
    def create_user(email: str, password: str = None, display_name: str = None):
        """
        Create Firebase user (typically already exists via Google/Email auth)
        This is a utility function for admin operations.
        """
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name)
            logger.info(f"Created user: {email}")
            return user
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            return None
