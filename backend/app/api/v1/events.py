"""
Events API endpoints.
RESTful API following Stride Ahead standards.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.models import Event
from app.schemas.schemas import EventCreate, EventUpdate, EventResponse, MessageResponse

router = APIRouter()


@router.get("", response_model=List[EventResponse])
async def list_events(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all published events"""
    result = await db.execute(
        select(Event)
        .where(Event.status == "published")
        .offset(skip)
        .limit(limit)
    )
    events = result.scalars().all()
    return events


@router.get("/{slug}", response_model=EventResponse)
async def get_event_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get event by slug"""
    result = await db.execute(
        select(Event).where(Event.slug == slug)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with slug '{slug}' not found"
        )
    
    return event


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new event (Admin only)"""
    # TODO: Add authentication middleware to verify admin role
    
    # Check if slug already exists
    result = await db.execute(
        select(Event).where(Event.slug == event_data.slug)
    )
    existing_event = result.scalar_one_or_none()
    
    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Event with slug '{event_data.slug}' already exists"
        )
    
    # Create event
    import uuid
    event = Event(
        **event_data.model_dump(),
        tenant_id=uuid.uuid4()  # TODO: Get from authenticated user context
    )
    
    db.add(event)
    await db.commit()
    await db.refresh(event)
    
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    event_data: EventUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an event (Admin only)"""
    # TODO: Add authentication middleware
    
    result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID '{event_id}' not found"
        )
    
    # Update fields
    for field, value in event_data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    
    await db.commit()
    await db.refresh(event)
    
    return event


@router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete an event (Admin only)"""
    # TODO: Add authentication middleware
    
    result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID '{event_id}' not found"
        )
    
    await db.delete(event)
    await db.commit()
    
    return MessageResponse(message="Event deleted successfully")
