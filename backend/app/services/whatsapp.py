"""
WhatsApp Messaging Service via Karix RCM API
Integrated from sa-emails-service
"""
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class KarixWhatsAppAPI:
    """
    Karix RCM API implementation for WhatsApp messaging
    Adapted from sa-emails-service/src/services/whatsapp/karix_api.py
    """
    
    def __init__(self):
        self.base_url = settings.KARIX_API_URL
        self.api_key = settings.KARIX_API_KEY
        self.sender = settings.KARIX_SENDER_NUMBER
        
        self.headers = {
            "Authentication": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def send_template_message(
        self,
        template_id: str,
        recipient: str,
        parameters: Optional[Dict] = None,
        header_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a template message using approved Karix template
        
        Args:
            template_id: The ID of the approved template in Karix
            recipient: Phone number with country code (e.g., +919876543210)
            parameters: Key-value pairs for template parameters
            header_title: Header title if required
            
        Returns:
            Message send status
        """
        url = f"{self.base_url.rstrip('/')}/sendMessage"
        
        # Build parameter values
        param_values = {}
        if parameters:
            for i, value in enumerate(parameters.values()):
                param_values[str(i)] = value
        
        payload = {
            "message": {
                "channel": "WABA",
                "content": {
                    "preview_url": False,
                    "type": "TEMPLATE",
                    "template": {
                        "templateId": template_id,
                        "parameterValues": param_values
                    },
                    "shorten_url": True
                },
                "recipient": {
                    "to": recipient,
                    "recipient_type": "individual",
                    "reference": {
                        "cust_ref": "Stride Events",
                        "messageTag1": "Event Registration",
                        "conversationId": f"conv-{int(time.time())}"
                    }
                },
                "sender": {
                    "from": self.sender
                }
            },
            "metaData": {
                "version": "v1.0.9"
            }
        }
        
        if header_title:
            payload["message"]["content"]["template"]["headerTitle"] = header_title
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("mid", ""),
                "status": "sent",
                "response": result
            }
        except Exception as e:
            logger.error(f"Template message send failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_text_message(self, recipient: str, text: str) -> Dict[str, Any]:
        """
        Send text message via Karix
        
        Args:
            recipient: Phone number with country code
            text: Message text
            
        Returns:
            Message send status
        """
        url = f"{self.base_url.rstrip('/')}/sendMessage"
        
        payload = {
            "message": {
                "channel": "WABA",
                "content": {
                    "preview_url": False,
                    "text": text,
                    "type": "TEXT"
                },
                "recipient": {
                    "to": recipient,
                    "recipient_type": "individual",
                    "reference": {
                        "cust_ref": "Stride Events",
                        "messageTag1": "Event Notification",
                        "conversationId": f"conv-{int(time.time())}"
                    }
                },
                "sender": {
                    "from": self.sender
                }
            },
            "metaData": {
                "version": "v1.0.9"
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("mid", ""),
                "status": result.get("statusDesc", "sent"),
                "response": result
            }
        except Exception as e:
            logger.error(f"Text message send failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_media_message(
        self,
        recipient: str,
        media_type: str,
        media_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send media message via Karix
        
        Args:
            recipient: Phone number with country code
            media_type: Type (image, document, video, audio)
            media_url: Public URL of media file
            caption: Optional caption
            
        Returns:
            Message send status
        """
        url = f"{self.base_url.rstrip('/')}/sendMessage"
        
        attachment_type_map = {
            "image": "image",
            "document": "document",
            "video": "video",
            "audio": "audio",
            "sticker": "sticker"
        }
        
        attachment_type = attachment_type_map.get(media_type.lower(), "document")
        
        attachment = {
            "type": attachment_type,
            "url": media_url
        }
        
        if caption and attachment_type in ["image", "document", "video"]:
            attachment["caption"] = caption
        
        payload = {
            "message": {
                "channel": "WABA",
                "content": {
                    "preview_url": False,
                    "type": "ATTACHMENT",
                    "attachment": attachment
                },
                "recipient": {
                    "to": recipient,
                    "recipient_type": "individual",
                    "reference": {
                        "cust_ref": "Stride Events",
                        "messageTag1": "Event Media",
                        "conversationId": f"conv-{int(time.time())}"
                    }
                },
                "sender": {
                    "from": self.sender
                }
            },
            "metaData": {
                "version": "v1.0.9"
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("mid", ""),
                "status": result.get("statusDesc", "sent"),
                "response": result
            }
        except Exception as e:
            logger.error(f"Media message send failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Event-specific WhatsApp notification functions

async def send_registration_confirmation(
    mobile: str,
    student_name: str,
    event_name: str,
    registration_code: str,
    event_date: str
) -> Dict:
    """Send registration confirmation WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""🎉 Registration Confirmed!

Hi {student_name},

You have successfully registered for {event_name}.

📋 Registration Code: {registration_code}
📅 Event Date: {event_date}

You will receive further details via email.

Best regards,
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_payment_confirmation(
    mobile: str,
    student_name: str,
    event_name: str,
    amount_paid: int,
    transaction_id: str
) -> Dict:
    """Send payment confirmation WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    amount_rupees = amount_paid / 100
    message = f"""✅ Payment Successful!

Hi {student_name},

Your payment for {event_name} has been confirmed.

💰 Amount Paid: ₹{amount_rupees}
🔖 Transaction ID: {transaction_id}

You're all set for the event!

Best regards,
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_event_reminder(
    mobile: str,
    student_name: str,
    event_name: str,
    event_date: str,
    event_time: str
) -> Dict:
    """Send event reminder WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""⏰ Event Reminder

Hi {student_name},

This is a reminder that {event_name} is scheduled for:

📅 Date: {event_date}
🕐 Time: {event_time}

Make sure you're prepared!

Good luck!
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_assessment_link(
    mobile: str,
    student_name: str,
    event_name: str,
    assessment_url: str
) -> Dict:
    """Send assessment link WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""📝 Assessment Link

Hi {student_name},

The assessment for {event_name} is now live!

🔗 Access your assessment here:
{assessment_url}

Good luck!
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_results_notification(
    mobile: str,
    student_name: str,
    event_name: str,
    result_url: str
) -> Dict:
    """Send results notification WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""📊 Results Announced!

Hi {student_name},

The results for {event_name} are now available.

🏆 View your results here:
{result_url}

Congratulations on completing the event!
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_certificate_notification(
    mobile: str,
    student_name: str,
    event_name: str,
    certificate_url: str
) -> Dict:
    """Send certificate notification WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""🎓 Certificate Ready!

Hi {student_name},

Your certificate for {event_name} is ready!

📜 Download your certificate:
{certificate_url}

Congratulations!
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)


async def send_school_registration_confirmation(
    mobile: str,
    school_name: str,
    event_name: str,
    school_code: str,
    registration_url: str
) -> Dict:
    """Send school registration confirmation WhatsApp message"""
    karix = KarixWhatsAppAPI()
    
    message = f"""🏫 School Registration Confirmed!

Hi {school_name},

Your school has been successfully registered for {event_name}.

🔑 School Code: {school_code}

Share this registration link with your students:
{registration_url}

Students can use this link to register under your school.

Best regards,
Stride Ahead Team"""
    
    return karix.send_text_message(mobile, message)
