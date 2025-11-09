# Backend Setup Guide - Stride Events Platform

Complete guide for setting up and running the FastAPI backend with all integrations.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Server](#running-the-server)
6. [API Documentation](#api-documentation)
7. [Testing Integrations](#testing-integrations)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip or poetry for package management
- Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Team-Stride/stride-events-platform.git
cd stride-events-platform/backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- fastapi
- uvicorn[standard]
- sqlalchemy[asyncio]
- asyncpg
- alembic
- pydantic-settings
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart
- sendgrid
- razorpay
- stripe
- requests

---

## Configuration

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Fill in Required Values

Edit `.env` and provide your actual credentials:

```bash
# Critical - Must be set
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/stride_events
SECRET_KEY=$(openssl rand -hex 32)

# Payment (choose one or both)
RAZORPAY_KEY_ID=rzp_test_your_key
RAZORPAY_KEY_SECRET=your_secret
PAYMENT_GATEWAY=razorpay

# Email
SENDGRID_API_KEY=SG.your_api_key
SENDGRID_FROM_EMAIL=noreply@strideahead.in

# WhatsApp
KARIX_API_KEY=your_karix_key
KARIX_SENDER_NUMBER=+919876543210

# Frontend
FRONTEND_URL=http://localhost:5173
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3. Generate Secret Key

```bash
openssl rand -hex 32
```

Copy the output and paste it as `SECRET_KEY` in `.env`.

---

## Database Setup

### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE stride_events;

# Create user (optional)
CREATE USER stride_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE stride_events TO stride_user;

\q
```

### 2. Run Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 3. Seed Data

```bash
# Seed AI Olympiad 2025 event
python seed_data.py
```

**Expected output:**
```
✅ AI Olympiad 2025 event created successfully!
   Event ID: <uuid>
   Slug: ai-olympiad-2025
   Registration Fee: ₹99 (use code KEEPSTRIDING for 100% off)
```

---

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn (Production)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Server will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

Most endpoints require JWT authentication. Include token in header:

```
Authorization: Bearer <your_jwt_token>
```

### Key Endpoints

#### Events

```bash
# Get event by slug
GET /api/v1/events/{slug}

# List all events
GET /api/v1/events

# Create event (admin only)
POST /api/v1/events

# Update event (admin only)
PUT /api/v1/events/{event_id}
```

#### Registrations

```bash
# Register student
POST /api/v1/registrations/student

# Register school
POST /api/v1/registrations/school

# List event registrations (admin only)
GET /api/v1/registrations/event/{event_id}/students
```

#### Payments

```bash
# Create payment order
POST /api/v1/payments/create-order

# Verify payment
POST /api/v1/payments/verify

# Webhook (Razorpay)
POST /api/v1/payments/webhook/razorpay

# Webhook (Stripe)
POST /api/v1/payments/webhook/stripe
```

---

## Testing Integrations

### 1. Test Email Service

```python
from app.services.email import send_registration_confirmation_email

# Send test email
await send_registration_confirmation_email(
    to_email="test@example.com",
    student_name="Test Student",
    event_name="AI Olympiad 2025",
    registration_code="STU-ABC123",
    event_date="December 15, 2025",
    event_url="http://localhost:5173/events/ai-olympiad-2025"
)
```

### 2. Test WhatsApp Service

```python
from app.services.whatsapp import send_registration_confirmation

# Send test WhatsApp
await send_registration_confirmation(
    mobile="+919876543210",
    student_name="Test Student",
    event_name="AI Olympiad 2025",
    registration_code="STU-ABC123",
    event_date="December 15, 2025"
)
```

### 3. Test Payment Integration

```bash
# Create Razorpay order
curl -X POST http://localhost:8000/api/v1/payments/create-order \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 9900,
    "currency": "INR",
    "registration_id": "<uuid>",
    "registration_type": "student"
  }'
```

### 4. Test Coupon Validation

```python
from app.services.payments import validate_and_apply_coupon

# Test KEEPSTRIDING coupon
result = await validate_and_apply_coupon(
    db=db,
    coupon_code="KEEPSTRIDING",
    amount=9900,
    event_id="<event_uuid>",
    registration_type="student"
)

# Should return: {"valid": True, "final_amount": 0, "discount_amount": 9900}
```

---

## Service Integration Details

### SendGrid Email Service

**Location:** `app/services/email.py`

**Features:**
- HTML email templates
- Registration confirmation emails
- Payment confirmation emails
- School registration emails
- Attachment support

**Usage:**
```python
from app.services.email import EmailService

email_service = EmailService()
result = email_service.send_email(
    to_email="user@example.com",
    subject="Test Email",
    html_content="<h1>Hello</h1>",
    text_content="Hello"
)
```

### Karix WhatsApp Service

**Location:** `app/services/whatsapp.py`

**Features:**
- Template messages
- Text messages
- Media messages
- Registration confirmations
- Payment confirmations
- Event reminders

**Usage:**
```python
from app.services.whatsapp import KarixWhatsAppAPI

karix = KarixWhatsAppAPI()
result = karix.send_text_message(
    recipient="+919876543210",
    text="Hello from Stride Ahead!"
)
```

### Payment Services

**Location:** `app/services/payments.py`

**Supported Gateways:**
- Razorpay (default)
- Stripe

**Features:**
- Order creation
- Payment verification
- Webhook handling
- Coupon validation
- Free order handling

**Usage:**
```python
from app.services.payments import PaymentProcessorFactory

# Create processor
processor = PaymentProcessorFactory.create_processor("razorpay")

# Create order
order = processor.generate_order(
    amount=9900,  # ₹99 in paise
    metadata={"event_id": "ai-olympiad-2025"}
)

# Verify payment
is_valid = processor.verify_payment(
    order_id=order["order_id"],
    payment_id="pay_xxx",
    signature="signature_xxx"
)
```

---

## Environment Variables Reference

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/db` |
| `SECRET_KEY` | JWT signing key | `openssl rand -hex 32` |

### Payment (Required if ENABLE_PAYMENTS=True)

| Variable | Description | Example |
|----------|-------------|---------|
| `RAZORPAY_KEY_ID` | Razorpay key ID | `rzp_test_xxx` |
| `RAZORPAY_KEY_SECRET` | Razorpay secret | `xxx` |
| `STRIPE_SECRET_KEY` | Stripe secret key | `sk_test_xxx` |
| `PAYMENT_GATEWAY` | Default gateway | `razorpay` or `stripe` |

### Email (Required if ENABLE_EMAIL_NOTIFICATIONS=True)

| Variable | Description | Example |
|----------|-------------|---------|
| `SENDGRID_API_KEY` | SendGrid API key | `SG.xxx` |
| `SENDGRID_FROM_EMAIL` | From email address | `noreply@strideahead.in` |
| `SENDGRID_FROM_NAME` | From name | `Stride Ahead` |

### WhatsApp (Required if ENABLE_WHATSAPP_NOTIFICATIONS=True)

| Variable | Description | Example |
|----------|-------------|---------|
| `KARIX_API_KEY` | Karix API key | `xxx` |
| `KARIX_SENDER_NUMBER` | Karix WhatsApp number | `+919876543210` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `development` |
| `DEBUG` | Debug mode | `False` |
| `FRONTEND_URL` | Frontend base URL | `http://localhost:5173` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## Troubleshooting

### Database Connection Issues

**Error:** `could not connect to server`

**Solution:**
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify DATABASE_URL in `.env`
3. Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-14-main.log`

### Migration Errors

**Error:** `Target database is not up to date`

**Solution:**
```bash
# Check current revision
alembic current

# Upgrade to latest
alembic upgrade head

# If stuck, downgrade and re-upgrade
alembic downgrade -1
alembic upgrade head
```

### Payment Integration Issues

**Error:** `Invalid API key`

**Solution:**
1. Verify API keys in `.env`
2. Check if using test vs live keys correctly
3. Ensure PAYMENT_GATEWAY matches the credentials provided

### Email Not Sending

**Error:** `Unauthorized`

**Solution:**
1. Verify SENDGRID_API_KEY is correct
2. Check SendGrid account status
3. Verify sender email is verified in SendGrid
4. Check SendGrid API logs

### WhatsApp Not Sending

**Error:** `Authentication failed`

**Solution:**
1. Verify KARIX_API_KEY is correct
2. Check KARIX_SENDER_NUMBER format (+country code)
3. Ensure Karix account has credits
4. Verify WhatsApp Business API is approved

---

## Production Deployment Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Use production database (not localhost)
- [ ] Use live payment gateway keys (not test keys)
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test all integrations in staging first

---

## Support

For issues or questions:
- Check KNOWN_ISSUES.md
- Review API docs at http://localhost:8000/docs
- Contact: dev@strideahead.in

---

**Last Updated:** November 9, 2025  
**Version:** 1.0.0
