"""
Firestore database operations
Handles user data, credits, transactions, and anonymous trial tracking
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Optional, Dict, Any
import logging
import hashlib

logger = logging.getLogger(__name__)

# Initialize Firebase (assume credentials are set via environment or service account)
try:
    if not firebase_admin.get_app():
        cred = credentials.Certificate("firebase-credentials.json")
        firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized
    pass

db = firestore.client()


class FirestoreService:
    """Firestore database service"""
    
    @staticmethod
    def hash_ip(ip_address: str) -> str:
        """Hash IP address for privacy"""
        return hashlib.sha256(ip_address.encode()).hexdigest()[:16]
    
    @staticmethod
    def create_user(uid: str, email: str, display_name: str, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """
        Create new user document with first login bonus
        
        Args:
            uid: Firebase user ID
            email: User email
            display_name: User display name
            ip_address: Client IP for tracking
            
        Returns:
            User data dictionary
        """
        now = datetime.utcnow().isoformat()
        user_data = {
            "email": email,
            "displayName": display_name,
            "credits": 5,  # First login bonus
            "plan": "free",
            "firstLoginBonusUsed": True,
            "creditsFromFirstLogin": 5,
            "lastLoginAt": now,
            "createdAt": now,
            "anonIpBeforeSignup": ip_address if ip_address else None
        }
        
        db.collection("users").document(uid).set(user_data)
        
        # Log transaction
        db.collection("users").document(uid).collection("transactions").document().set({
            "type": "signup_bonus",
            "amount": 5,
            "status": "completed",
            "timestamp": now,
            "details": {"bonus": "first_login"}
        })
        
        logger.info(f"Created user: {uid}")
        return user_data
    
    @staticmethod
    def get_user(uid: str) -> Optional[Dict[str, Any]]:
        """Get user document"""
        doc = db.collection("users").document(uid).get()
        return doc.to_dict() if doc.exists else None
    
    @staticmethod
    def check_anon_trial(ip_address: str) -> Dict[str, Any]:
        """
        Check anonymous trial status for IP
        
        Returns:
            {
                "eligible": bool,
                "generationCount": int,
                "status": "eligible" | "exhausted"
            }
        """
        ip_hash = FirestoreService.hash_ip(ip_address)
        doc = db.collection("anonUsers").document(ip_hash).get()
        
        if not doc.exists:
            # First time this IP
            return {
                "eligible": True,
                "generationCount": 0,
                "status": "eligible"
            }
        
        data = doc.to_dict()
        return {
            "eligible": data.get("generationCount", 0) < 3,
            "generationCount": data.get("generationCount", 0),
            "status": data.get("status", "eligible")
        }
    
    @staticmethod
    def increment_anon_trial(ip_address: str) -> int:
        """
        Increment anonymous trial counter
        
        Returns:
            New generation count
        """
        ip_hash = FirestoreService.hash_ip(ip_address)
        now = datetime.utcnow().isoformat()
        
        def increment_counter(txn):
            doc_ref = db.collection("anonUsers").document(ip_hash)
            doc = txn.get(doc_ref)
            
            if doc.exists:
                current_count = doc.get("generationCount", 0)
                new_count = current_count + 1
            else:
                new_count = 1
            
            new_status = "exhausted" if new_count >= 3 else "eligible"
            
            txn.set(doc_ref, {
                "ipAddress": ip_address,
                "ipHash": ip_hash,
                "generationCount": new_count,
                "firstGenerationAt": doc.get("firstGenerationAt") if doc.exists else now,
                "lastGenerationAt": now,
                "status": new_status
            })
            
            return new_count
        
        transaction = db.transaction()
        count = transaction(increment_counter)
        logger.info(f"Incremented anon trial for IP {ip_hash}: {count}/3")
        return count
    
    @staticmethod
    def deduct_credits(uid: str, amount: int, shoot_id: str) -> bool:
        """
        Atomically deduct credits from user
        
        Args:
            uid: User ID
            amount: Credits to deduct
            shoot_id: Photoshoot ID for transaction log
            
        Returns:
            Success status
        """
        now = datetime.utcnow().isoformat()
        
        def deduct(txn):
            user_ref = db.collection("users").document(uid)
            user_doc = txn.get(user_ref)
            
            if not user_doc.exists:
                raise ValueError("User not found")
            
            current_credits = user_doc.get("credits", 0)
            
            if current_credits < amount:
                raise ValueError(f"Insufficient credits: {current_credits} < {amount}")
            
            new_credits = current_credits - amount
            
            # Update credits
            txn.update(user_ref, {"credits": new_credits})
            
            # Log transaction
            txn.set(
                user_ref.collection("transactions").document(),
                {
                    "type": "generation",
                    "amount": amount,
                    "status": "completed",
                    "shootId": shoot_id,
                    "timestamp": now,
                    "details": {"credits_remaining": new_credits}
                }
            )
            
            return new_credits
        
        try:
            transaction = db.transaction()
            new_balance = transaction(deduct)
            logger.info(f"Deducted {amount} credits from user {uid}. New balance: {new_balance}")
            return True
        except Exception as e:
            logger.error(f"Failed to deduct credits: {str(e)}")
            return False
    
    @staticmethod
    def add_credits(uid: str, amount: int, reason: str = "purchase", payment_method: Optional[str] = None) -> bool:
        """
        Add credits to user account
        
        Args:
            uid: User ID
            amount: Credits to add
            reason: Reason for credit addition
            payment_method: Payment method used (if applicable)
            
        Returns:
            Success status
        """
        now = datetime.utcnow().isoformat()
        
        try:
            user_ref = db.collection("users").document(uid)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                logger.error(f"User {uid} not found")
                return False
            
            current_credits = user_doc.get("credits", 0)
            new_credits = current_credits + amount
            
            user_ref.update({"credits": new_credits})
            
            # Log transaction
            user_ref.collection("transactions").document().set({
                "type": "purchase",
                "amount": amount,
                "status": "completed",
                "paymentMethod": payment_method,
                "timestamp": now,
                "details": {"credits_total": new_credits}
            })
            
            logger.info(f"Added {amount} credits to user {uid}. New balance: {new_credits}")
            return True
        except Exception as e:
            logger.error(f"Failed to add credits: {str(e)}")
            return False
    
    @staticmethod
    def get_credits(uid: str) -> Optional[int]:
        """Get user's current credit balance"""
        user = FirestoreService.get_user(uid)
        return user.get("credits", 0) if user else None
    
    @staticmethod
    def save_photoshoot(uid_or_anon: str, shoot_data: Dict[str, Any]) -> str:
        """
        Save photoshoot document
        
        Args:
            uid_or_anon: User ID or "anon-{ipHash}"
            shoot_data: Photoshoot data
            
        Returns:
            Shoot ID
        """
        now = datetime.utcnow().isoformat()
        shoot_id = db.collection("photoshoots").document().id
        
        db.collection("photoshoots").document(uid_or_anon).collection("shoots").document(shoot_id).set({
            "articleType": shoot_data.get("articleType"),
            "styleNotes": shoot_data.get("styleNotes"),
            "imageSize": shoot_data.get("imageSize"),
            "uploadedImages": shoot_data.get("uploadedImages", []),
            "generatedImages": shoot_data.get("generatedImages", []),
            "creditsCost": shoot_data.get("creditsCost", 0),
            "isFreeTrial": shoot_data.get("isFreeTrial", False),
            "status": shoot_data.get("status", "completed"),
            "createdAt": now
        })
        
        logger.info(f"Saved photoshoot {shoot_id} for {uid_or_anon}")
        return shoot_id
