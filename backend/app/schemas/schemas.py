"""
Pydantic schemas for request/response validation.
Follows Stride Ahead standards for data validation.
"""
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.models import EventStatus, RegistrationStatus


# ============================================================================
# Event Schemas
# ============================================================================

class EventBase(BaseModel):
    """Base event schema"""
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    tagline: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    event_type: str = "competition"
    status: EventStatus = EventStatus.DRAFT


class EventCreate(EventBase):
    """Schema for creating an event"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None
    banner_image_url: Optional[str] = None
    content_sections: Optional[str] = None  # JSON string
    prizes: Optional[str] = None  # JSON string
    sponsors: Optional[str] = None  # JSON string
    faqs: Optional[str] = None  # JSON string
    max_participants: Optional[int] = None
    is_free: bool = True
    registration_fee: int = 0


class EventUpdate(BaseModel):
    """Schema for updating an event"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    tagline: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    status: Optional[EventStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None
    banner_image_url: Optional[str] = None
    content_sections: Optional[str] = None
    prizes: Optional[str] = None
    sponsors: Optional[str] = None
    faqs: Optional[str] = None
    max_participants: Optional[int] = None
    is_free: Optional[bool] = None
    registration_fee: Optional[int] = None


class EventResponse(EventBase):
    """Schema for event response"""
    id: UUID
    tenant_id: UUID
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    registration_deadline: Optional[datetime]
    banner_image_url: Optional[str]
    content_sections: Optional[str]
    prizes: Optional[str]
    sponsors: Optional[str]
    faqs: Optional[str]
    max_participants: Optional[int]
    is_free: bool
    registration_fee: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Student Registration Schemas
# ============================================================================

class StudentRegistrationBase(BaseModel):
    """Base student registration schema"""
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=20)
    school_name: str = Field(..., min_length=1, max_length=500)
    grade: str = Field(..., min_length=1, max_length=50)


class StudentRegistrationCreate(StudentRegistrationBase):
    """Schema for creating a student registration"""
    event_id: UUID
    school_id: Optional[UUID] = None
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    dietary_requirements: Optional[str] = None


class StudentRegistrationResponse(StudentRegistrationBase):
    """Schema for student registration response"""
    id: UUID
    tenant_id: UUID
    event_id: UUID
    school_id: Optional[UUID]
    linkedin_url: Optional[str]
    cv_url: Optional[str]
    dietary_requirements: Optional[str]
    stride_user_id: Optional[UUID]
    status: RegistrationStatus
    registration_code: str
    payment_status: str
    registered_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# School Registration Schemas
# ============================================================================

class SchoolRegistrationBase(BaseModel):
    """Base school registration schema"""
    school_name: str = Field(..., min_length=1, max_length=500)
    contact_person_name: str = Field(..., min_length=1, max_length=255)
    contact_email: EmailStr
    contact_mobile: str = Field(..., min_length=10, max_length=20)


class SchoolRegistrationCreate(SchoolRegistrationBase):
    """Schema for creating a school registration"""
    event_id: UUID
    city: Optional[str] = Field(None, max_length=255)
    state: Optional[str] = Field(None, max_length=255)


class SchoolRegistrationResponse(SchoolRegistrationBase):
    """Schema for school registration response"""
    id: UUID
    tenant_id: UUID
    event_id: UUID
    school_code: str
    city: Optional[str]
    state: Optional[str]
    total_students_registered: int
    registered_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Generic Response Schemas
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None
