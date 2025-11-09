"""
Audit Logging Service

Tracks all critical operations for compliance and security purposes.
Especially important when dealing with student data and parental consent.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.models import AuditLog
import json
import logging

logger = logging.getLogger(__name__)


class AuditLogService:
    """Service for logging audit events"""
    
    @staticmethod
    async def log_event(
        db: AsyncSession,
        event_type: str,
        user_id: Optional[int],
        user_email: Optional[str],
        resource_type: str,
        resource_id: Optional[int],
        action: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None
    ) -> AuditLog:
        """
        Log an audit event
        
        Args:
            event_type: Type of event (registration, payment, data_access, consent, etc.)
            user_id: ID of the user performing the action
            user_email: Email of the user
            resource_type: Type of resource (student, school, event, etc.)
            resource_id: ID of the resource
            action: Action performed (create, read, update, delete, consent_given, etc.)
            details: Additional details about the event
            ip_address: IP address of the request
            user_agent: User agent string
            status: Status of the operation (success, failure)
            error_message: Error message if status is failure
        """
        try:
            audit_log = AuditLog(
                event_type=event_type,
                user_id=user_id,
                user_email=user_email,
                resource_type=resource_type,
                resource_id=resource_id,
                action=action,
                details=json.dumps(details) if details else None,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                error_message=error_message,
                timestamp=datetime.utcnow()
            )
            
            db.add(audit_log)
            await db.commit()
            await db.refresh(audit_log)
            
            logger.info(f"Audit log created: {event_type} - {action} - {status}")
            return audit_log
            
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            await db.rollback()
            raise
    
    @staticmethod
    async def log_registration(
        db: AsyncSession,
        registration_type: str,  # "student" or "school"
        registration_id: int,
        email: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        consent_details: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log a registration event with consent details"""
        return await AuditLogService.log_event(
            db=db,
            event_type="registration",
            user_id=None,  # No user ID yet for new registrations
            user_email=email,
            resource_type=registration_type,
            resource_id=registration_id,
            action="create",
            details={
                "consent_details": consent_details,
                "registration_type": registration_type
            },
            ip_address=ip_address,
            user_agent=user_agent,
            status="success"
        )
    
    @staticmethod
    async def log_consent_given(
        db: AsyncSession,
        user_id: int,
        user_email: str,
        consent_type: str,  # "terms", "privacy", "parental", "data_processing", "marketing"
        consent_version: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Log consent given by user"""
        return await AuditLogService.log_event(
            db=db,
            event_type="consent",
            user_id=user_id,
            user_email=user_email,
            resource_type="consent",
            resource_id=None,
            action="consent_given",
            details={
                "consent_type": consent_type,
                "consent_version": consent_version,
                "timestamp": datetime.utcnow().isoformat()
            },
            ip_address=ip_address,
            user_agent=user_agent,
            status="success"
        )
    
    @staticmethod
    async def log_payment(
        db: AsyncSession,
        user_id: int,
        user_email: str,
        payment_id: int,
        amount: float,
        currency: str,
        payment_method: str,
        status: str,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log a payment transaction"""
        return await AuditLogService.log_event(
            db=db,
            event_type="payment",
            user_id=user_id,
            user_email=user_email,
            resource_type="payment",
            resource_id=payment_id,
            action="create",
            details={
                "amount": amount,
                "currency": currency,
                "payment_method": payment_method
            },
            ip_address=ip_address,
            status=status
        )
    
    @staticmethod
    async def log_data_access(
        db: AsyncSession,
        user_id: int,
        user_email: str,
        resource_type: str,
        resource_id: int,
        action: str,  # "read", "update", "delete", "export"
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log data access events (important for GDPR compliance)"""
        return await AuditLogService.log_event(
            db=db,
            event_type="data_access",
            user_id=user_id,
            user_email=user_email,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            ip_address=ip_address,
            status="success"
        )
    
    @staticmethod
    async def log_data_deletion(
        db: AsyncSession,
        user_id: int,
        user_email: str,
        resource_type: str,
        resource_id: int,
        reason: str,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Log data deletion events (GDPR right to be forgotten)"""
        return await AuditLogService.log_event(
            db=db,
            event_type="data_deletion",
            user_id=user_id,
            user_email=user_email,
            resource_type=resource_type,
            resource_id=resource_id,
            action="delete",
            details={"reason": reason},
            ip_address=ip_address,
            status="success"
        )
    
    @staticmethod
    async def log_email_sent(
        db: AsyncSession,
        recipient_email: str,
        email_type: str,
        subject: str,
        status: str,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Log email sending events"""
        return await AuditLogService.log_event(
            db=db,
            event_type="email",
            user_id=None,
            user_email=recipient_email,
            resource_type="email",
            resource_id=None,
            action="send",
            details={
                "email_type": email_type,
                "subject": subject
            },
            status=status,
            error_message=error_message
        )
    
    @staticmethod
    async def log_whatsapp_sent(
        db: AsyncSession,
        recipient_phone: str,
        message_type: str,
        status: str,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Log WhatsApp message sending events"""
        return await AuditLogService.log_event(
            db=db,
            event_type="whatsapp",
            user_id=None,
            user_email=None,
            resource_type="whatsapp",
            resource_id=None,
            action="send",
            details={
                "recipient_phone": recipient_phone,
                "message_type": message_type
            },
            status=status,
            error_message=error_message
        )
    
    @staticmethod
    async def get_user_audit_logs(
        db: AsyncSession,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> list[AuditLog]:
        """Retrieve audit logs for a specific user"""
        query = select(AuditLog)
        
        conditions = []
        if user_id:
            conditions.append(AuditLog.user_id == user_id)
        if user_email:
            conditions.append(AuditLog.user_email == user_email)
        if event_type:
            conditions.append(AuditLog.event_type == event_type)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(AuditLog.timestamp.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_resource_audit_logs(
        db: AsyncSession,
        resource_type: str,
        resource_id: int,
        limit: int = 100
    ) -> list[AuditLog]:
        """Retrieve audit logs for a specific resource"""
        query = select(AuditLog).where(
            and_(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id
            )
        ).order_by(AuditLog.timestamp.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()


# Helper function to extract IP address from request
def get_client_ip(request) -> str:
    """Extract client IP address from request"""
    # Check for X-Forwarded-For header (when behind proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    # Check for X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fall back to direct client IP
    return request.client.host if request.client else "unknown"


# Helper function to extract user agent from request
def get_user_agent(request) -> str:
    """Extract user agent from request"""
    return request.headers.get("User-Agent", "unknown")
