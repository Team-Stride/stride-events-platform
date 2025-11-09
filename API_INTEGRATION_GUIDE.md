# API Integration Guide - Stride Events Platform

This document details how to integrate the Events Platform with existing Stride Ahead services.

---

## Overview

The Events Platform integrates with three main Stride Ahead services:

1. **Stride ID** - User authentication and account management
2. **Assessment Manager** - Test/quiz integration for competitions
3. **SendGrid** - Email notifications
4. **Carex** - WhatsApp notifications (future)

---

## 1. Stride ID API Integration

### Base URL
```
Production: https://stride-id-api.strideahead.in
Staging: https://stride-id-staging.strideahead.in
```

### Authentication
All requests require Bearer token in header:
```
Authorization: Bearer {STRIDE_ID_API_KEY}
```

### Key Endpoints

#### Create User Account
```http
POST /api/register
Content-Type: application/json

{
  "email": "student@example.com",
  "name": "John Doe",
  "mobile": "+919876543210",
  "grade": "10",
  "school_name": "ABC High School"
}

Response 201:
{
  "user_id": "uuid",
  "email": "student@example.com",
  "stride_id": "STR12345",
  "access_token": "jwt_token"
}
```

#### Verify User
```http
GET /api/users/{user_id}
Authorization: Bearer {API_KEY}

Response 200:
{
  "user_id": "uuid",
  "email": "student@example.com",
  "name": "John Doe",
  "is_active": true
}
```

### Implementation in Events Platform

Update `backend/app/api/v1/registrations.py`:

```python
from app.services.stride_id import create_stride_user

@router.post("/student", response_model=StudentRegistrationResponse)
async def register_student(
    registration_data: StudentRegistrationCreate,
    db: AsyncSession = Depends(get_db)
):
    # ... existing validation code ...
    
    # Create Stride ID account
    try:
        stride_user = await create_stride_user(
            email=registration_data.email,
            name=registration_data.full_name,
            mobile=registration_data.mobile
        )
        stride_user_id = stride_user["user_id"]
    except Exception as e:
        # Log error but don't fail registration
        print(f"Failed to create Stride ID: {e}")
        stride_user_id = None
    
    # Create registration with stride_user_id
    registration = StudentRegistration(
        **registration_data.model_dump(),
        tenant_id=event.tenant_id,
        stride_user_id=stride_user_id,
        registration_code=generate_registration_code("STU"),
        status="confirmed"
    )
    
    # ... rest of code ...
```

---

## 2. Assessment Manager API Integration

### Base URL
```
Production: https://assessment-api.strideahead.in
Staging: https://assessment-staging.strideahead.in
```

### Authentication
```
Authorization: Bearer {ASSESSMENT_API_KEY}
```

### Key Endpoints

#### Create Assessment
```http
POST /api/v1/assessments
Content-Type: application/json

{
  "title": "AI Olympiad Round 1",
  "description": "First round assessment",
  "event_id": "uuid",
  "duration_minutes": 60,
  "total_marks": 100,
  "questions": [
    {
      "type": "mcq",
      "question_text": "What is AI?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A",
      "marks": 1
    }
  ]
}

Response 201:
{
  "assessment_id": "uuid",
  "access_url": "https://assessment.strideahead.in/take/{code}"
}
```

#### Get Assessment Results
```http
GET /api/v1/assessments/{assessment_id}/results
Authorization: Bearer {API_KEY}

Response 200:
{
  "assessment_id": "uuid",
  "total_participants": 150,
  "results": [
    {
      "user_id": "uuid",
      "score": 85,
      "rank": 1,
      "completed_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Implementation

Add to `backend/app/models/models.py`:

```python
class EventAssessment(Base):
    """Link events to assessments"""
    __tablename__ = "event_assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    assessment_id = Column(UUID(as_uuid=True), nullable=False)
    round_number = Column(Integer, default=1)
    assessment_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
```

---

## 3. SendGrid Email Integration

### Setup

1. Get SendGrid API Key from: https://app.sendgrid.com/settings/api_keys
2. Add to environment: `SENDGRID_API_KEY=SG.xxx`
3. Verify sender email in SendGrid dashboard

### Email Templates

#### Registration Confirmation
```python
from app.services.email import send_registration_confirmation

await send_registration_confirmation(
    to_email=registration.email,
    student_name=registration.full_name,
    event_name=event.title,
    registration_code=registration.registration_code
)
```

#### School Registration
```python
from app.services.email import send_school_registration_email

unique_url = f"https://events.strideahead.in/register?school={school.school_code}"

await send_school_registration_email(
    to_email=school.contact_email,
    school_name=school.school_name,
    event_name=event.title,
    school_code=school.school_code,
    unique_url=unique_url
)
```

### Email Service Implementation

Already created in `backend/app/services/email.py`. Install SendGrid:

```bash
pip install sendgrid
```

Add to `requirements.txt`:
```
sendgrid==6.11.0
```

---

## 4. Carex WhatsApp Integration (Future)

### Base URL
```
TBD: https://whatsapp-api.strideahead.in
```

### Planned Implementation

```python
async def send_whatsapp_notification(
    mobile: str,
    template_name: str,
    parameters: dict
):
    """Send WhatsApp message via Carex API"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.CAREX_API_URL}/send",
            json={
                "mobile": mobile,
                "template": template_name,
                "params": parameters
            },
            headers={"Authorization": f"Bearer {settings.CAREX_API_KEY}"}
        )
        return response.status_code == 200
```

---

## Integration Checklist

### Pre-Launch
- [ ] Obtain Stride ID API credentials
- [ ] Test Stride ID user creation flow
- [ ] Obtain SendGrid API key
- [ ] Verify sender email in SendGrid
- [ ] Create email templates in SendGrid
- [ ] Test email delivery
- [ ] Obtain Assessment Manager API credentials
- [ ] Test assessment creation

### Post-Launch
- [ ] Monitor API error rates
- [ ] Set up retry logic for failed API calls
- [ ] Implement webhook handlers for async updates
- [ ] Add API rate limiting
- [ ] Set up monitoring/alerting for API failures

---

## Error Handling

### Stride ID API Errors

```python
try:
    stride_user = await create_stride_user(...)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 409:
        # User already exists
        logger.info(f"User {email} already exists in Stride ID")
    elif e.response.status_code == 429:
        # Rate limited
        logger.error("Stride ID API rate limit exceeded")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    else:
        logger.error(f"Stride ID API error: {e}")
        # Continue registration without Stride ID
except httpx.TimeoutException:
    logger.error("Stride ID API timeout")
    # Continue registration, retry later
```

### Email Service Errors

```python
try:
    await send_registration_confirmation(...)
except Exception as e:
    logger.error(f"Failed to send email: {e}")
    # Store in queue for retry
    await queue_email_retry(registration.id)
```

---

## Testing

### Test Stride ID Integration

```python
# tests/test_stride_id.py
import pytest
from app.services.stride_id import create_stride_user

@pytest.mark.asyncio
async def test_create_stride_user():
    user = await create_stride_user(
        email="test@example.com",
        name="Test User",
        mobile="+919876543210"
    )
    assert user["user_id"] is not None
    assert user["email"] == "test@example.com"
```

### Test Email Service

```python
# tests/test_email.py
import pytest
from app.services.email import send_registration_confirmation

@pytest.mark.asyncio
async def test_send_confirmation_email():
    result = await send_registration_confirmation(
        to_email="test@example.com",
        student_name="Test Student",
        event_name="Test Event",
        registration_code="TEST-12345"
    )
    assert result is True
```

---

## Monitoring

### Key Metrics to Track

1. **Stride ID API**
   - Success rate
   - Response time
   - Error rate by status code

2. **Email Service**
   - Delivery rate
   - Bounce rate
   - Open rate

3. **Assessment API**
   - Assessment creation success rate
   - Result fetch latency

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# Log all API calls
logger.info(f"Creating Stride ID for {email}")
logger.error(f"Stride ID API failed: {error}")
```

---

## Support

For API access or issues:
- Stride ID: Contact backend team
- Assessment Manager: Contact assessment team
- SendGrid: Check SendGrid dashboard
- General: Stride Ahead DevOps team
