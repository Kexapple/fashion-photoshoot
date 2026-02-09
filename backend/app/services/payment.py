"""
Payment gateway integration for JazzCash and EasyPaisa
Handles payment verification and credit addition
"""

import logging
import hashlib
import requests
from typing import Dict, Any, Optional
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


class PaymentService:
    """Payment gateway service for Pakistani payment methods"""
    
    @staticmethod
    def verify_jazzcash_payment(
        transaction_id: str,
        amount: float,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Verify JazzCash payment
        
        Args:
            transaction_id: JazzCash transaction ID
            amount: Amount in PKR
            phone_number: Customer phone number
            
        Returns:
            {
                "verified": bool,
                "message": str,
                "amount": float
            }
        """
        try:
            # JazzCash verification endpoint
            verify_url = "https://sandbox.jazzcash.com.pk/ApplicationAPI/API/DoTransaction"
            
            # JazzCash request format
            # Note: This is a simplified example. Real implementation needs proper signing.
            payload = {
                "pp_merchant_id": settings.JAZZCASH_MERCHANT_ID,
                "pp_password": settings.JAZZCASH_PASSWORD,
                "pp_txn_ref": transaction_id,
            }
            
            # In production, add proper request signing with JAZZCASH_INTEGRITY_KEY
            # signature = create_jazzcash_signature(payload, settings.JAZZCASH_INTEGRITY_KEY)
            # payload["pp_request_signature"] = signature
            
            response = requests.post(verify_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response status (JazzCash specific)
                if data.get("pp_status") == "1":  # Success
                    logger.info(f"JazzCash payment verified: {transaction_id}")
                    return {
                        "verified": True,
                        "message": "Payment verified successfully",
                        "amount": amount,
                        "transactionId": transaction_id,
                        "gateway": "jazzcash"
                    }
                else:
                    logger.warning(f"JazzCash payment failed: {data.get('pp_response_message')}")
                    return {
                        "verified": False,
                        "message": data.get("pp_response_message", "Payment verification failed"),
                        "amount": 0
                    }
            else:
                logger.error(f"JazzCash API error: {response.status_code}")
                return {
                    "verified": False,
                    "message": f"API error: {response.status_code}",
                    "amount": 0
                }
        except Exception as e:
            logger.error(f"JazzCash verification error: {str(e)}", exc_info=True)
            return {
                "verified": False,
                "message": f"Verification error: {str(e)}",
                "amount": 0
            }
    
    @staticmethod
    def verify_easypaisa_payment(
        transaction_id: str,
        amount: float,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Verify EasyPaisa payment
        
        Args:
            transaction_id: EasyPaisa transaction ID
            amount: Amount in PKR
            phone_number: Customer phone number
            
        Returns:
            {
                "verified": bool,
                "message": str,
                "amount": float
            }
        """
        try:
            # EasyPaisa verification endpoint
            verify_url = "https://easypaisavx.easypaisa.com.pk/api/merchantaccount/getTransaction"
            
            payload = {
                "merchantId": settings.EASYPAISA_MERCHANT_ID,
                "password": settings.EASYPAISA_PASSWORD,
                "transactionId": transaction_id
            }
            
            response = requests.post(verify_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response status (EasyPaisa specific)
                if data.get("responseCode") == "000":  # Success
                    logger.info(f"EasyPaisa payment verified: {transaction_id}")
                    return {
                        "verified": True,
                        "message": "Payment verified successfully",
                        "amount": amount,
                        "transactionId": transaction_id,
                        "gateway": "easypaisa"
                    }
                else:
                    logger.warning(f"EasyPaisa payment failed: {data.get('responseMessage')}")
                    return {
                        "verified": False,
                        "message": data.get("responseMessage", "Payment verification failed"),
                        "amount": 0
                    }
            else:
                logger.error(f"EasyPaisa API error: {response.status_code}")
                return {
                    "verified": False,
                    "message": f"API error: {response.status_code}",
                    "amount": 0
                }
        except Exception as e:
            logger.error(f"EasyPaisa verification error: {str(e)}", exc_info=True)
            return {
                "verified": False,
                "message": f"Verification error: {str(e)}",
                "amount": 0
            }
    
    @staticmethod
    def calculate_credits_for_amount(amount_pkr: float) -> int:
        """
        Calculate number of credits for given PKR amount
        
        Example rates:
        - 500 PKR = 10 credits
        - 1000 PKR = 25 credits
        - 2000 PKR = 50 credits
        - 4000 PKR = 100 credits
        """
        # Simple rate: 5 PKR per credit
        credits = int(amount_pkr / 5)
        return max(1, credits)  # Minimum 1 credit


class MockPaymentService:
    """Mock payment service for testing"""
    
    @staticmethod
    def verify_jazzcash_payment(
        transaction_id: str,
        amount: float,
        phone_number: str
    ) -> Dict[str, Any]:
        """Mock JazzCash verification"""
        logger.info(f"MOCK: Verifying JazzCash payment {transaction_id}")
        return {
            "verified": True,
            "message": "Mock payment verified",
            "amount": amount,
            "transactionId": transaction_id,
            "gateway": "jazzcash"
        }
    
    @staticmethod
    def verify_easypaisa_payment(
        transaction_id: str,
        amount: float,
        phone_number: str
    ) -> Dict[str, Any]:
        """Mock EasyPaisa verification"""
        logger.info(f"MOCK: Verifying EasyPaisa payment {transaction_id}")
        return {
            "verified": True,
            "message": "Mock payment verified",
            "amount": amount,
            "transactionId": transaction_id,
            "gateway": "easypaisa"
        }
    
    @staticmethod
    def calculate_credits_for_amount(amount_pkr: float) -> int:
        """Calculate credits for amount"""
        credits = int(amount_pkr / 5)
        return max(1, credits)


# Use mock service if credentials not configured
if settings.JAZZCASH_MERCHANT_ID and settings.EASYPAISA_MERCHANT_ID:
    PaymentVerificationService = PaymentService
else:
    PaymentVerificationService = MockPaymentService
    logger.warning("Payment credentials not configured. Using mock payment service.")
