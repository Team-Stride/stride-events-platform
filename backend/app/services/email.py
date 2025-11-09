"""
Email Service using SendGrid
Integrated from sa-emails-service standards
"""
import logging
from typing import Dict, List, Optional, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """SendGrid email service"""
    
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.from_name = settings.SENDGRID_FROM_NAME
        self.client = SendGridAPIClient(self.api_key)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[Dict]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send email via SendGrid
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text content (optional)
            attachments: List of attachments (optional)
            cc: CC email addresses (optional)
            bcc: BCC email addresses (optional)
            
        Returns:
            Send status
        """
        try:
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                message.add_content(Content("text/plain", text_content))
            
            if cc:
                for cc_email in cc:
                    message.add_cc(cc_email)
            
            if bcc:
                for bcc_email in bcc:
                    message.add_bcc(bcc_email)
            
            if attachments:
                for attachment in attachments:
                    att = Attachment(
                        FileContent(attachment['content']),
                        FileName(attachment['filename']),
                        FileType(attachment.get('type', 'application/octet-stream')),
                        Disposition(attachment.get('disposition', 'attachment'))
                    )
                    message.add_attachment(att)
            
            response = self.client.send(message)
            
            return {
                "success": True,
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id', ''),
                "message": "Email sent successfully"
            }
            
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_template_email(
        self,
        to_email: str,
        template_id: str,
        dynamic_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send email using SendGrid dynamic template
        
        Args:
            to_email: Recipient email
            template_id: SendGrid template ID
            dynamic_data: Template variables
            
        Returns:
            Send status
        """
        try:
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email)
            )
            
            message.template_id = template_id
            message.dynamic_template_data = dynamic_data
            
            response = self.client.send(message)
            
            return {
                "success": True,
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id', ''),
                "message": "Template email sent successfully"
            }
            
        except Exception as e:
            logger.error(f"Template email send failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Email Templates

def get_registration_confirmation_email(
    student_name: str,
    event_name: str,
    registration_code: str,
    event_date: str,
    event_url: str
) -> Dict[str, str]:
    """Generate registration confirmation email HTML"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registration Confirmed</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .info-box {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #667eea;
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                color: #667eea;
                letter-spacing: 2px;
            }}
            .button {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 12px;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 Registration Confirmed!</h1>
        </div>
        <div class="content">
            <p>Hi {student_name},</p>
            
            <p>Congratulations! You have successfully registered for <strong>{event_name}</strong>.</p>
            
            <div class="info-box">
                <p><strong>📋 Registration Code:</strong></p>
                <p class="code">{registration_code}</p>
                
                <p><strong>📅 Event Date:</strong> {event_date}</p>
            </div>
            
            <p>Please save this registration code for your records. You will need it to access the event.</p>
            
            <a href="{event_url}" class="button">View Event Details</a>
            
            <p>You will receive further instructions via email as the event date approaches.</p>
            
            <p>If you have any questions, feel free to reply to this email.</p>
            
            <p>Best regards,<br><strong>Stride Ahead Team</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 Stride Ahead. All rights reserved.</p>
            <p>This is an automated email. Please do not reply directly to this message.</p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Registration Confirmed!
    
    Hi {student_name},
    
    Congratulations! You have successfully registered for {event_name}.
    
    Registration Code: {registration_code}
    Event Date: {event_date}
    
    Please save this registration code for your records.
    
    View event details: {event_url}
    
    Best regards,
    Stride Ahead Team
    """
    
    return {
        "html": html_content,
        "text": text_content
    }


def get_payment_confirmation_email(
    student_name: str,
    event_name: str,
    amount_paid: int,
    transaction_id: str,
    registration_code: str
) -> Dict[str, str]:
    """Generate payment confirmation email HTML"""
    
    amount_rupees = amount_paid / 100
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Confirmed</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .receipt-box {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .amount {{
                font-size: 32px;
                font-weight: bold;
                color: #10b981;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 12px;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>✅ Payment Successful!</h1>
        </div>
        <div class="content">
            <p>Hi {student_name},</p>
            
            <p>Your payment for <strong>{event_name}</strong> has been successfully processed.</p>
            
            <div class="receipt-box">
                <p><strong>💰 Amount Paid:</strong></p>
                <p class="amount">₹{amount_rupees}</p>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                
                <p><strong>🔖 Transaction ID:</strong> {transaction_id}</p>
                <p><strong>📋 Registration Code:</strong> {registration_code}</p>
                <p><strong>📅 Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <p>You're all set for the event! Keep this email as your payment receipt.</p>
            
            <p>Best regards,<br><strong>Stride Ahead Team</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 Stride Ahead. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Payment Successful!
    
    Hi {student_name},
    
    Your payment for {event_name} has been successfully processed.
    
    Amount Paid: ₹{amount_rupees}
    Transaction ID: {transaction_id}
    Registration Code: {registration_code}
    Date: {datetime.now().strftime('%B %d, %Y')}
    
    You're all set for the event!
    
    Best regards,
    Stride Ahead Team
    """
    
    return {
        "html": html_content,
        "text": text_content
    }


def get_school_registration_email(
    school_name: str,
    contact_person: str,
    event_name: str,
    school_code: str,
    registration_url: str
) -> Dict[str, str]:
    """Generate school registration confirmation email HTML"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>School Registration Confirmed</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .info-box {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #3b82f6;
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                color: #3b82f6;
                letter-spacing: 2px;
            }}
            .url-box {{
                background: #eff6ff;
                padding: 15px;
                border-radius: 6px;
                word-break: break-all;
                font-family: monospace;
                font-size: 14px;
            }}
            .button {{
                display: inline-block;
                background: #3b82f6;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 12px;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏫 School Registration Confirmed!</h1>
        </div>
        <div class="content">
            <p>Hi {contact_person},</p>
            
            <p><strong>{school_name}</strong> has been successfully registered for <strong>{event_name}</strong>.</p>
            
            <div class="info-box">
                <p><strong>🔑 School Code:</strong></p>
                <p class="code">{school_code}</p>
            </div>
            
            <p><strong>📝 Student Registration Link:</strong></p>
            <div class="url-box">{registration_url}</div>
            
            <p>Share this link with your students so they can register under your school. Students will automatically be associated with {school_name} when they use this link.</p>
            
            <a href="{registration_url}" class="button">Open Registration Link</a>
            
            <p><strong>What's Next?</strong></p>
            <ul>
                <li>Share the registration link with your students</li>
                <li>Track registrations through your school dashboard</li>
                <li>Receive event updates via email</li>
            </ul>
            
            <p>If you have any questions, feel free to reply to this email.</p>
            
            <p>Best regards,<br><strong>Stride Ahead Team</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 Stride Ahead. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    School Registration Confirmed!
    
    Hi {contact_person},
    
    {school_name} has been successfully registered for {event_name}.
    
    School Code: {school_code}
    
    Student Registration Link:
    {registration_url}
    
    Share this link with your students so they can register under your school.
    
    What's Next?
    - Share the registration link with your students
    - Track registrations through your school dashboard
    - Receive event updates via email
    
    Best regards,
    Stride Ahead Team
    """
    
    return {
        "html": html_content,
        "text": text_content
    }


# Event-specific email functions

async def send_registration_confirmation_email(
    to_email: str,
    student_name: str,
    event_name: str,
    registration_code: str,
    event_date: str,
    event_url: str
) -> Dict:
    """Send registration confirmation email"""
    email_service = EmailService()
    
    email_content = get_registration_confirmation_email(
        student_name, event_name, registration_code, event_date, event_url
    )
    
    return email_service.send_email(
        to_email=to_email,
        subject=f"Registration Confirmed - {event_name}",
        html_content=email_content["html"],
        text_content=email_content["text"]
    )


async def send_payment_confirmation_email(
    to_email: str,
    student_name: str,
    event_name: str,
    amount_paid: int,
    transaction_id: str,
    registration_code: str
) -> Dict:
    """Send payment confirmation email"""
    email_service = EmailService()
    
    email_content = get_payment_confirmation_email(
        student_name, event_name, amount_paid, transaction_id, registration_code
    )
    
    return email_service.send_email(
        to_email=to_email,
        subject=f"Payment Confirmed - {event_name}",
        html_content=email_content["html"],
        text_content=email_content["text"]
    )


async def send_school_registration_email(
    to_email: str,
    school_name: str,
    contact_person: str,
    event_name: str,
    school_code: str,
    registration_url: str
) -> Dict:
    """Send school registration confirmation email"""
    email_service = EmailService()
    
    email_content = get_school_registration_email(
        school_name, contact_person, event_name, school_code, registration_url
    )
    
    return email_service.send_email(
        to_email=to_email,
        subject=f"School Registration Confirmed - {event_name}",
        html_content=email_content["html"],
        text_content=email_content["text"]
    )
