"""
Registrations API endpoints.
RESTful API following Stride Ahead standards.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
import secrets
import string

from app.core.database import get_db
from app.models.models import StudentRegistration, SchoolRegistration, Event
from app.schemas.schemas import (
    StudentRegistrationCreate,
    StudentRegistrationResponse,
    SchoolRegistrationCreate,
    SchoolRegistrationResponse,
    MessageResponse
)

router = APIRouter()


def generate_registration_code(prefix: str = "REG") -> str:
    """Generate unique registration code"""
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return f"{prefix}-{random_part}"


@router.post("/student", response_model=StudentRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_student(
    registration_data: StudentRegistrationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a student for an event"""
    
    # Verify event exists
    result = await db.execute(
        select(Event).where(Event.id == registration_data.event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if student already registered
    result = await db.execute(
        select(StudentRegistration).where(
            StudentRegistration.event_id == registration_data.event_id,
            StudentRegistration.email == registration_data.email
        )
    )
    existing_registration = result.scalar_one_or_none()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already registered for this event"
        )
    
    # Create registration
    import uuid
    registration = StudentRegistration(
        **registration_data.model_dump(),
        tenant_id=event.tenant_id,
        registration_code=generate_registration_code("STU"),
        status="confirmed"  # Auto-confirm for free events
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    # TODO: Send confirmation email
    # TODO: Create Stride ID account via API
    
    return registration


@router.post("/school", response_model=SchoolRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_school(
    registration_data: SchoolRegistrationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a school for an event"""
    
    # Verify event exists
    result = await db.execute(
        select(Event).where(Event.id == registration_data.event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if school already registered
    result = await db.execute(
        select(SchoolRegistration).where(
            SchoolRegistration.event_id == registration_data.event_id,
            SchoolRegistration.contact_email == registration_data.contact_email
        )
    )
    existing_registration = result.scalar_one_or_none()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School already registered for this event"
        )
    
    # Create registration
    import uuid
    registration = SchoolRegistration(
        **registration_data.model_dump(),
        tenant_id=event.tenant_id,
        school_code=generate_registration_code("SCH")
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    # TODO: Send confirmation email with unique URL
    
    return registration


@router.get("/event/{event_id}/students", response_model=List[StudentRegistrationResponse])
async def list_event_registrations(
    event_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all student registrations for an event (Admin only)"""
    # TODO: Add authentication middleware
    
    result = await db.execute(
        select(StudentRegistration)
        .where(StudentRegistration.event_id == event_id)
        .offset(skip)
        .limit(limit)
    )
    registrations = result.scalars().all()
    return registrations
