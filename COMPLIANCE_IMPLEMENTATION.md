# Compliance Implementation Guide

## Overview

This document describes the JWT authentication, legal compliance pages, and audit logging implementation for the Stride Events Platform.

---

## 🔐 JWT Authentication

### Implementation

**Backend:** `backend/app/core/auth.py`

- JWT token validation middleware
- Integration with Stride ID SSO
- Token verification and user extraction
- Dependency injection for protected routes

### Configuration

Add to `.env`:
```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stride ID SSO
STRIDE_ID_API_URL=https://id.strideahead.in/api
STRIDE_ID_VALIDATION_ENDPOINT=/v1/auth/validate
```

### Usage in FastAPI

```python
from app.core.auth import get_current_user
from fastapi import Depends

@app.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
```

### Frontend Integration

The frontend should:
1. Store JWT token in localStorage after login
2. Send token in Authorization header: `Bearer <token>`
3. Handle 401 responses by redirecting to login

Example:
```typescript
// In api.ts
const token = localStorage.getItem('jwt_token');
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

## 📄 Legal Compliance Pages

### Terms & Conditions

**File:** `frontend/src/pages/TermsAndConditions.tsx`

**Route:** `/terms`

**Content Includes:**
- Platform usage terms
- User responsibilities
- Event participation rules
- Payment and refund policy
- Intellectual property rights
- Liability limitations
- Dispute resolution
- Governing law

### Privacy Policy

**File:** `frontend/src/pages/PrivacyPolicy.tsx`

**Route:** `/privacy`

**Content Includes:**
- Data collection practices
- Protection of minors' privacy
- Parental consent requirements
- Data usage and sharing
- Security measures
- Data retention policies
- User rights (GDPR compliant)
- Cookie policy
- Contact information

### ⚠️ IMPORTANT

Both pages are **placeholder templates** compliant with GDPR and Indian data protection laws. 

**Before going live:**
1. Have your legal team review both documents
2. Customize content to match your specific practices
3. Add your company address and contact details
4. Update the "Last Updated" date

---

## ✅ Consent Management

### Student Registration Form

**Consent Checkboxes Added:**

1. **Terms & Conditions** (Required)
   - Links to `/terms`
   - Must be checked to submit

2. **Privacy Policy** (Required)
   - Links to `/privacy`
   - Must be checked to submit

3. **Parental Consent** (Required for minors)
   - Explicit consent for child's participation
   - Consent for data collection and processing
   - Must be checked to submit

4. **Data Processing Consent** (Required)
   - Consent for event management use
   - Consent for communication
   - Must be checked to submit

5. **Marketing Consent** (Optional)
   - Opt-in for future event updates
   - Can be unchecked

### Parental Information Fields

**Added for students under 18:**
- Parent/Guardian Name (Required)
- Parent/Guardian Email (Required)
- Parent/Guardian Mobile (Required)

### School Registration Form

**Consent Checkboxes Added:**

1. Terms & Conditions (Required)
2. Privacy Policy (Required)
3. Data Processing Consent (Required)
4. Marketing Consent (Optional)

---

## 📊 Audit Logging System

### Implementation

**File:** `backend/app/services/audit_log.py`

**Database Model:** `backend/app/models/models.py` - `AuditLog` table

### Features

**Tracks:**
- All registrations (student/school)
- Consent given (terms, privacy, parental, data processing, marketing)
- Payment transactions
- Data access events (read, update, delete, export)
- Data deletion requests (GDPR right to be forgotten)
- Email sending events
- WhatsApp message sending events

**Captures:**
- Event type and action
- User ID and email
- Resource type and ID
- IP address
- User agent
- Timestamp
- Success/failure status
- Error messages
- Additional details (JSON)

### Usage Examples

#### Log Registration
```python
from app.services.audit_log import AuditLogService

await AuditLogService.log_registration(
    db=db,
    registration_type="student",
    registration_id=registration.id,
    email=registration.email,
    ip_address=get_client_ip(request),
    user_agent=get_user_agent(request),
    consent_details={
        "terms": True,
        "privacy": True,
        "parental": True,
        "data_processing": True,
        "marketing": False
    }
)
```

#### Log Consent
```python
await AuditLogService.log_consent_given(
    db=db,
    user_id=user.id,
    user_email=user.email,
    consent_type="parental",
    consent_version="v1.0",
    ip_address=get_client_ip(request),
    user_agent=get_user_agent(request)
)
```

#### Log Payment
```python
await AuditLogService.log_payment(
    db=db,
    user_id=user.id,
    user_email=user.email,
    payment_id=payment.id,
    amount=payment.amount,
    currency="INR",
    payment_method="razorpay",
    status="success",
    ip_address=get_client_ip(request)
)
```

#### Log Data Access
```python
await AuditLogService.log_data_access(
    db=db,
    user_id=admin.id,
    user_email=admin.email,
    resource_type="student",
    resource_id=student.id,
    action="read",
    ip_address=get_client_ip(request)
)
```

#### Retrieve Audit Logs
```python
# Get user's audit logs
logs = await AuditLogService.get_user_audit_logs(
    db=db,
    user_email="student@example.com",
    event_type="registration",
    limit=100
)

# Get resource audit logs
logs = await AuditLogService.get_resource_audit_logs(
    db=db,
    resource_type="student",
    resource_id=student_id,
    limit=100
)
```

### Helper Functions

```python
from app.services.audit_log import get_client_ip, get_user_agent

# Extract IP address from request
ip = get_client_ip(request)

# Extract user agent from request
user_agent = get_user_agent(request)
```

---

## 🗄️ Database Migration

### Create Migration

```bash
cd backend
alembic revision --autogenerate -m "Add audit_log table and update consent fields"
alembic upgrade head
```

### AuditLog Table Schema

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    user_id INTEGER,
    user_email VARCHAR(320),
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details TEXT,
    error_message TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    INDEX idx_event_type (event_type),
    INDEX idx_user_id (user_id),
    INDEX idx_user_email (user_email),
    INDEX idx_timestamp (timestamp)
);
```

---

## 🔒 Security Best Practices

### JWT Tokens
- Store securely in localStorage (not cookies to avoid CSRF)
- Set reasonable expiration times (30 minutes recommended)
- Implement refresh token mechanism
- Clear tokens on logout

### Consent Management
- Always require explicit consent (no pre-checked boxes)
- Store consent timestamp and version
- Allow users to withdraw consent
- Provide easy access to legal documents

### Audit Logging
- Log all sensitive operations
- Never log passwords or payment details
- Retain logs for at least 3 years (compliance requirement)
- Implement log rotation and archival
- Restrict access to audit logs (admin only)

### Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Implement rate limiting on APIs
- Validate and sanitize all inputs
- Implement CORS properly

---

## 📋 Compliance Checklist

### Before Launch

- [ ] Legal team reviews Terms & Conditions
- [ ] Legal team reviews Privacy Policy
- [ ] Update company address and contact details
- [ ] Configure JWT secret key (strong, random)
- [ ] Set up Stride ID SSO integration
- [ ] Test parental consent flow
- [ ] Verify all consent checkboxes work
- [ ] Test audit logging for all operations
- [ ] Set up database backups
- [ ] Configure log retention policy
- [ ] Test GDPR data export functionality
- [ ] Test GDPR data deletion functionality
- [ ] Implement email verification
- [ ] Set up monitoring and alerts
- [ ] Conduct security audit
- [ ] Train staff on data protection procedures

### Ongoing Compliance

- [ ] Review audit logs monthly
- [ ] Respond to data access requests within 30 days
- [ ] Process data deletion requests within 30 days
- [ ] Update legal documents annually
- [ ] Conduct security audits quarterly
- [ ] Train new staff on compliance procedures
- [ ] Monitor for data breaches
- [ ] Report breaches within 72 hours (GDPR requirement)

---

## 🚨 Incident Response

### Data Breach Procedure

1. **Detect:** Monitor audit logs and security alerts
2. **Contain:** Immediately isolate affected systems
3. **Assess:** Determine scope and impact
4. **Notify:** Inform affected users within 72 hours
5. **Report:** File breach report with authorities
6. **Remediate:** Fix vulnerabilities
7. **Review:** Update security procedures

### Contact Information

**Data Protection Officer:**
- Email: dpo@strideahead.in
- Phone: [Your Contact Number]

**Security Team:**
- Email: security@strideahead.in
- Emergency: [24/7 Contact]

---

## 📞 Support

For questions about compliance implementation:
- **Technical:** dev@strideahead.in
- **Legal:** legal@strideahead.in
- **Privacy:** privacy@strideahead.in

---

**Last Updated:** November 9, 2025
**Version:** 1.0
