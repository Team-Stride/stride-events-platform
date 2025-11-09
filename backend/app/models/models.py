"""
Database models for Stride Events Platform.
Follows Stride Ahead standards:
- UUIDs for primary keys
- snake_case naming
- Multi-tenancy with tenant_id
- Timestamps for audit trail
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class EventStatus(str, enum.Enum):
    """Event status enum"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RegistrationStatus(str, enum.Enum):
    """Registration status enum"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Event(Base):
    """
    Events table - stores competition events.
    Multi-tenant ready with tenant_id.
    """
    __tablename__ = "events"
    
    # Primary key - UUID as per Stride standards
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Multi-tenancy
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Event details
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    tagline = Column(String(500))
    description = Column(Text)
    
    # Event metadata
    event_type = Column(String(100), default="competition")  # competition, workshop, etc.
    status = Column(SQLEnum(EventStatus), default=EventStatus.DRAFT, nullable=False)
    
    # Dates
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    registration_deadline = Column(DateTime(timezone=True))
    
    # Content (JSON stored as Text, can be parsed by Pydantic)
    banner_image_url = Column(String(500))
    content_sections = Column(Text)  # JSON string
    prizes = Column(Text)  # JSON string
    sponsors = Column(Text)  # JSON string
    faqs = Column(Text)  # JSON string
    
    # Settings
    max_participants = Column(Integer)
    is_free = Column(Boolean, default=True)
    registration_fee = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True))
    
    # Relationships
    student_registrations = relationship("StudentRegistration", back_populates="event", cascade="all, delete-orphan")
    school_registrations = relationship("SchoolRegistration", back_populates="event", cascade="all, delete-orphan")


class StudentRegistration(Base):
    """
    Student registrations table.
    Multi-tenant ready with tenant_id.
    """
    __tablename__ = "student_registrations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Multi-tenancy
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Foreign keys
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("school_registrations.id", ondelete="SET NULL"), nullable=True)
    
    # Student details
    full_name = Column(String(255), nullable=False)
    email = Column(String(320), nullable=False)
    mobile = Column(String(20), nullable=False)
    school_name = Column(String(500), nullable=False)
    grade = Column(String(50), nullable=False)  # e.g., "9", "10", "11", "12"
    
    # Optional fields
    linkedin_url = Column(String(500))
    cv_url = Column(String(500))
    dietary_requirements = Column(Text)
    
    # Stride ID integration (populated after account creation)
    stride_user_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Registration metadata
    status = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=False)
    registration_code = Column(String(50), unique=True, index=True)  # Unique code for tracking
    
    # Payment (for future use)
    payment_status = Column(String(50), default="not_required")
    payment_id = Column(String(255))
    
    # Audit fields
    registered_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="student_registrations")
    school = relationship("SchoolRegistration", back_populates="students")


class SchoolRegistration(Base):
    """
    School registrations table.
    Schools can register and get unique URLs for their students.
    Multi-tenant ready with tenant_id.
    """
    __tablename__ = "school_registrations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Multi-tenancy
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Foreign keys
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # School details
    school_name = Column(String(500), nullable=False)
    contact_person_name = Column(String(255), nullable=False)
    contact_email = Column(String(320), nullable=False)
    contact_mobile = Column(String(20), nullable=False)
    
    # School metadata
    school_code = Column(String(50), unique=True, index=True)  # Unique code for URL parameter
    city = Column(String(255))
    state = Column(String(255))
    
    # Stats
    total_students_registered = Column(Integer, default=0)
    
    # Audit fields
    registered_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="school_registrations")
    students = relationship("StudentRegistration", back_populates="school", cascade="all, delete-orphan")


# Payment and Coupon Models

class Coupon(Base):
    """Coupon codes for discounts"""
    __tablename__ = "coupons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_type = Column(String(20), nullable=False)  # percentage, fixed
    discount_value = Column(Integer, nullable=False)  # percentage or amount in paise
    max_uses = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Restrictions
    min_amount = Column(Integer, nullable=True)  # minimum order amount in paise
    applicable_to = Column(String(50), default="all")  # all, student, school
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    """Payment transactions"""
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Registration reference
    registration_id = Column(UUID(as_uuid=True), nullable=False)
    registration_type = Column(String(20), nullable=False)  # student, school
    
    # Payment details
    amount = Column(Integer, nullable=False)  # amount in paise
    currency = Column(String(3), default="INR")
    status = Column(String(20), default="pending")  # pending, success, failed, refunded
    
    # Gateway details
    gateway = Column(String(20), nullable=False)  # razorpay, stripe
    gateway_order_id = Column(String(100), unique=True)
    gateway_payment_id = Column(String(100), unique=True, nullable=True)
    gateway_signature = Column(String(200), nullable=True)
    
    # Coupon
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupons.id"), nullable=True)
    discount_amount = Column(Integer, default=0)
    final_amount = Column(Integer, nullable=False)
    
    # Metadata
    payment_method = Column(String(50), nullable=True)  # card, upi, netbanking, etc.
    error_message = Column(Text, nullable=True)
    gateway_response = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime(timezone=True), nullable=True)


class AuditLog(Base):
    """
    Audit log table for compliance and security tracking.
    Tracks all critical operations especially for student data protection.
    """
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event details
    event_type = Column(String(50), nullable=False, index=True)  # registration, payment, consent, data_access, etc.
    action = Column(String(50), nullable=False)  # create, read, update, delete, consent_given, etc.
    status = Column(String(20), default="success")  # success, failure
    
    # User information
    user_id = Column(Integer, nullable=True, index=True)
    user_email = Column(String(320), nullable=True, index=True)
    
    # Resource information
    resource_type = Column(String(50), nullable=True)  # student, school, event, payment, etc.
    resource_id = Column(Integer, nullable=True)
    
    # Additional details
    details = Column(Text, nullable=True)  # JSON string with additional context
    error_message = Column(Text, nullable=True)
    
    # Request metadata
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.event_type}:{self.action} by {self.user_email} at {self.timestamp}>"
