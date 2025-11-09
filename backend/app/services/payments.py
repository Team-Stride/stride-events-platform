"""
Payment Gateway Service - Integrated from sa-payments-services
Adapted for Stride Events Platform
"""
import logging
from razorpay import Client as RazorpayClient
import stripe
from typing import Dict, Optional
import uuid
import json
from datetime import datetime

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaymentProcessor:
    """Base payment processor"""
    def __init__(self, gateway_config: Dict):
        self.gateway_config = gateway_config
        
    def generate_order(self, amount: int, metadata: Dict = None):
        raise NotImplementedError("Subclasses must implement this method")
    
    def verify_payment(self, payment_data: Dict):
        raise NotImplementedError("Subclasses must implement this method")
    
    def handle_webhook(self, raw_body: bytes, signature: str):
        raise NotImplementedError("Subclasses must implement this method")


class RazorpayProcessor(PaymentProcessor):
    """Razorpay payment processor"""
    
    def __init__(self):
        self.key_id = settings.RAZORPAY_KEY_ID
        self.key_secret = settings.RAZORPAY_KEY_SECRET
        self.webhook_secret = settings.PAYMENT_WEBHOOK_SECRET
        self.client = RazorpayClient(auth=(self.key_id, self.key_secret))
    
    def generate_order(self, amount: int, metadata: Dict = None) -> Dict:
        """
        Create Razorpay order
        
        Args:
            amount: Amount in paise (e.g., 9900 for ₹99)
            metadata: Additional metadata
            
        Returns:
            Order details with transaction_id
        """
        try:
            transaction_id = str(uuid.uuid4())
            
            # Handle free orders (amount = 0)
            if amount == 0:
                return {
                    "is_free": True,
                    "transaction_id": transaction_id,
                    "amount": 0,
                    "currency": "INR"
                }
            
            order_data = {
                "amount": amount,
                "currency": "INR",
                "receipt": f"event_reg_{transaction_id[:8]}",
                "payment_capture": 1,
                "notes": {
                    "transaction_id": transaction_id,
                    **(metadata or {})
                }
            }
            
            order = self.client.order.create(data=order_data)
            
            return {
                "is_free": False,
                "transaction_id": transaction_id,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "status": order["status"]
            }
            
        except Exception as e:
            logger.error(f"Failed to create Razorpay order: {e}")
            raise Exception(f"Payment order creation failed: {str(e)}")
    
    def verify_payment(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify Razorpay payment signature"""
        try:
            self.client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            return True
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return False
    
    def handle_webhook(self, raw_body: bytes, signature: str) -> Dict:
        """Handle Razorpay webhook"""
        try:
            request_data = json.loads(raw_body.decode('utf-8'))
            
            # Verify webhook signature
            verified = self.client.utility.verify_webhook_signature(
                raw_body.decode('utf-8'),
                signature,
                self.webhook_secret
            )
            
            if not verified:
                raise ValueError("Invalid webhook signature")
            
            event = request_data.get('event')
            
            if event == 'payment.captured':
                payment_entity = request_data['payload']['payment']['entity']
                transaction_id = payment_entity['notes'].get('transaction_id')
                
                return {
                    "event": "payment_captured",
                    "transaction_id": transaction_id,
                    "payment_id": payment_entity['id'],
                    "amount": payment_entity['amount'],
                    "status": "success"
                }
            
            return {"event": event, "status": "unhandled"}
            
        except Exception as e:
            logger.error(f"Webhook handling failed: {e}")
            raise


class StripeProcessor(PaymentProcessor):
    """Stripe payment processor"""
    
    def __init__(self):
        self.secret_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.PAYMENT_WEBHOOK_SECRET
        stripe.api_key = self.secret_key
    
    def generate_order(self, amount: int, metadata: Dict = None) -> Dict:
        """Create Stripe payment intent"""
        try:
            transaction_id = str(uuid.uuid4())
            
            # Handle free orders
            if amount == 0:
                return {
                    "is_free": True,
                    "transaction_id": transaction_id,
                    "amount": 0,
                    "currency": "inr"
                }
            
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="inr",
                metadata={
                    "transaction_id": transaction_id,
                    **(metadata or {})
                },
                automatic_payment_methods={"enabled": True}
            )
            
            return {
                "is_free": False,
                "transaction_id": transaction_id,
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "amount": intent.amount,
                "currency": intent.currency,
                "status": intent.status
            }
            
        except Exception as e:
            logger.error(f"Failed to create Stripe payment intent: {e}")
            raise Exception(f"Payment intent creation failed: {str(e)}")
    
    def verify_payment(self, payment_intent_id: str) -> Dict:
        """Verify Stripe payment"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "success": intent.status == "succeeded",
                "status": intent.status,
                "amount": intent.amount
            }
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return {"success": False, "error": str(e)}
    
    def handle_webhook(self, raw_body: bytes, signature: str) -> Dict:
        """Handle Stripe webhook"""
        try:
            event = stripe.Webhook.construct_event(
                raw_body,
                signature,
                self.webhook_secret
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                transaction_id = payment_intent['metadata'].get('transaction_id')
                
                return {
                    "event": "payment_succeeded",
                    "transaction_id": transaction_id,
                    "payment_id": payment_intent['id'],
                    "amount": payment_intent['amount'],
                    "status": "success"
                }
            
            return {"event": event['type'], "status": "unhandled"}
            
        except Exception as e:
            logger.error(f"Webhook handling failed: {e}")
            raise


class PaymentProcessorFactory:
    """Factory to create payment processors"""
    
    @staticmethod
    def create_processor(gateway: str = "razorpay"):
        if gateway == "razorpay":
            return RazorpayProcessor()
        elif gateway == "stripe":
            return StripeProcessor()
        else:
            raise ValueError(f"Unsupported gateway: {gateway}")


# Coupon validation logic
async def validate_and_apply_coupon(
    db,
    coupon_code: str,
    amount: int,
    event_id: str,
    registration_type: str = "student"
) -> Dict:
    """
    Validate and apply coupon code
    
    Args:
        db: Database session
        coupon_code: Coupon code to validate
        amount: Original amount in paise
        event_id: Event ID
        registration_type: "student" or "school"
        
    Returns:
        Discount details
    """
    from app.models.models import Coupon
    from sqlalchemy import select
    
    # Find coupon
    query = select(Coupon).where(
        Coupon.code == coupon_code.upper(),
        Coupon.is_active == True
    )
    result = await db.execute(query)
    coupon = result.scalar_one_or_none()
    
    if not coupon:
        return {"valid": False, "error": "Invalid coupon code"}
    
    # Check validity period
    now = datetime.utcnow()
    if now < coupon.valid_from or now > coupon.valid_until:
        return {"valid": False, "error": "Coupon has expired"}
    
    # Check usage limit
    if coupon.max_uses and coupon.used_count >= coupon.max_uses:
        return {"valid": False, "error": "Coupon usage limit reached"}
    
    # Check event restriction
    if coupon.event_id and str(coupon.event_id) != event_id:
        return {"valid": False, "error": "Coupon not valid for this event"}
    
    # Check minimum amount
    if coupon.min_amount and amount < coupon.min_amount:
        return {
            "valid": False,
            "error": f"Minimum order amount ₹{coupon.min_amount/100} required"
        }
    
    # Check applicability
    if coupon.applicable_to not in ["all", registration_type]:
        return {"valid": False, "error": "Coupon not applicable"}
    
    # Calculate discount
    if coupon.discount_type == "percentage":
        discount = int((amount * coupon.discount_value) / 100)
    else:  # fixed
        discount = coupon.discount_value
    
    # Ensure discount doesn't exceed amount
    discount = min(discount, amount)
    final_amount = amount - discount
    
    return {
        "valid": True,
        "coupon_id": str(coupon.id),
        "discount_amount": discount,
        "final_amount": final_amount,
        "discount_type": coupon.discount_type,
        "discount_value": coupon.discount_value
    }


async def increment_coupon_usage(db, coupon_id: str):
    """Increment coupon usage count"""
    from app.models.models import Coupon
    from sqlalchemy import update
    
    await db.execute(
        update(Coupon)
        .where(Coupon.id == coupon_id)
        .values(used_count=Coupon.used_count + 1)
    )
    await db.commit()
