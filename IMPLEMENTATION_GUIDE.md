# Stride Events Platform - Complete Implementation Guide

**Version:** 1.0  
**Last Updated:** November 9, 2025  
**Tech Stack:** FastAPI 0.110+ | React 18 | PostgreSQL 16 | TypeScript 5.x

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Backend Setup](#backend-setup)
3. [Frontend Implementation](#frontend-implementation)
4. [API Integration](#api-integration)
5. [Database Migrations](#database-migrations)
6. [Deployment](#deployment)

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ with pnpm
- PostgreSQL 16+
- Git

### Initial Setup

```bash
# Clone repository
cd stride-events-fastapi

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
pnpm install

# Create .env file (see Environment Variables section)
```

---

## Backend Setup

### Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/stride_events

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stride ID API
STRIDE_ID_API_URL=https://stride-id-api.strideahead.in
STRIDE_ID_API_KEY=your-api-key

# SendGrid
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=noreply@strideahead.in

# Environment
ENVIRONMENT=development
```

### Run Database Migrations

```bash
cd backend

# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`  
API Docs: `http://localhost:8000/api/v1/docs`

---

## Frontend Implementation

### Redux Store Setup

Create `frontend/src/store/store.ts`:

```typescript
import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {
    // Add slices here
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### API Client Setup

Create `frontend/src/lib/api.ts`:

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### Event Landing Page Component

Create `frontend/src/pages/EventLanding.tsx`:

```typescript
import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import apiClient from '@/lib/api';

interface Event {
  id: string;
  title: string;
  tagline: string;
  description: string;
  banner_image_url: string;
  start_date: string;
  registration_deadline: string;
}

export default function EventLanding() {
  const { slug } = useParams<{ slug: string }>();
  
  const { data: event, isLoading } = useQuery({
    queryKey: ['event', slug || 'ai-olympiad-2025'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/v1/events/${slug || 'ai-olympiad-2025'}`);
      return response.data as Event;
    },
  });

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!event) {
    return <div className="flex items-center justify-center min-h-screen">Event not found</div>;
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="container mx-auto px-4">
          <h1 className="text-5xl font-bold mb-4">{event.title}</h1>
          <p className="text-2xl mb-8">{event.tagline}</p>
          <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
            Register Now
          </button>
        </div>
      </section>

      {/* Content sections - Add more based on LPevents.pdf */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8">About the Competition</h2>
          <p className="text-lg text-gray-700">{event.description}</p>
        </div>
      </section>

      {/* Registration Form Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4 max-w-2xl">
          <h2 className="text-3xl font-bold mb-8 text-center">Register for the Event</h2>
          {/* Add RegistrationForm component here */}
        </div>
      </section>
    </div>
  );
}
```

### Registration Form Component

Create `frontend/src/components/features/RegistrationForm.tsx`:

```typescript
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/lib/api';

interface RegistrationData {
  event_id: string;
  full_name: string;
  email: string;
  mobile: string;
  school_name: string;
  grade: string;
  linkedin_url?: string;
  cv_url?: string;
}

export default function RegistrationForm({ eventId }: { eventId: string }) {
  const [formData, setFormData] = useState<RegistrationData>({
    event_id: eventId,
    full_name: '',
    email: '',
    mobile: '',
    school_name: '',
    grade: '',
  });

  const registerMutation = useMutation({
    mutationFn: async (data: RegistrationData) => {
      const response = await apiClient.post('/api/v1/registrations/student', data);
      return response.data;
    },
    onSuccess: (data) => {
      alert(`Registration successful! Your code: ${data.registration_code}`);
    },
    onError: (error: any) => {
      alert(`Registration failed: ${error.response?.data?.detail || 'Unknown error'}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    registerMutation.mutate(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Full Name *</label>
        <input
          type="text"
          required
          value={formData.full_name}
          onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Email *</label>
        <input
          type="email"
          required
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Mobile *</label>
        <input
          type="tel"
          required
          value={formData.mobile}
          onChange={(e) => setFormData({ ...formData, mobile: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">School Name *</label>
        <input
          type="text"
          required
          value={formData.school_name}
          onChange={(e) => setFormData({ ...formData, school_name: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Grade *</label>
        <select
          required
          value={formData.grade}
          onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select Grade</option>
          <option value="9">Grade 9</option>
          <option value="10">Grade 10</option>
          <option value="11">Grade 11</option>
          <option value="12">Grade 12</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={registerMutation.isPending}
        className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
      >
        {registerMutation.isPending ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

### Admin Dashboard Component

Create `frontend/src/pages/admin/Dashboard.tsx`:

```typescript
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api';

export default function AdminDashboard() {
  const { data: events } = useQuery({
    queryKey: ['admin-events'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/events');
      return response.data;
    },
  });

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Events</h2>
          <div className="space-y-4">
            {events?.map((event: any) => (
              <div key={event.id} className="border-b pb-4">
                <h3 className="font-semibold">{event.title}</h3>
                <p className="text-sm text-gray-600">{event.status}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## API Integration

### Stride ID API Integration

Create `backend/app/services/stride_id.py`:

```python
"""
Stride ID API integration service.
Handles user registration and authentication with Stride ID.
"""
import httpx
from app.core.config import settings


async def create_stride_user(email: str, name: str, mobile: str) -> dict:
    """
    Create a new user in Stride ID system.
    
    Args:
        email: User email
        name: User full name
        mobile: User mobile number
    
    Returns:
        dict: User data including stride_user_id
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.STRIDE_ID_API_URL}/api/register",
            json={
                "email": email,
                "name": name,
                "mobile": mobile,
            },
            headers={
                "Authorization": f"Bearer {settings.STRIDE_ID_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def verify_stride_user(user_id: str) -> dict:
    """Verify a Stride ID user exists"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.STRIDE_ID_API_URL}/api/users/{user_id}",
            headers={"Authorization": f"Bearer {settings.STRIDE_ID_API_KEY}"},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
```

### SendGrid Email Service

Create `backend/app/services/email.py`:

```python
"""
Email service using SendGrid.
Handles all email communications.
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings


async def send_registration_confirmation(
    to_email: str,
    student_name: str,
    event_name: str,
    registration_code: str
):
    """Send registration confirmation email"""
    
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=f"Registration Confirmed - {event_name}",
        html_content=f"""
        <h1>Welcome to {event_name}!</h1>
        <p>Dear {student_name},</p>
        <p>Your registration has been confirmed.</p>
        <p><strong>Registration Code:</strong> {registration_code}</p>
        <p>We look forward to seeing you at the event!</p>
        <p>Best regards,<br>Stride Ahead Team</p>
        """
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


async def send_school_registration_email(
    to_email: str,
    school_name: str,
    event_name: str,
    school_code: str,
    unique_url: str
):
    """Send school registration confirmation with unique URL"""
    
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=f"School Registration Confirmed - {event_name}",
        html_content=f"""
        <h1>School Registration Confirmed!</h1>
        <p>Dear {school_name},</p>
        <p>Your school has been registered for {event_name}.</p>
        <p><strong>School Code:</strong> {school_code}</p>
        <p><strong>Unique Registration URL for your students:</strong></p>
        <p><a href="{unique_url}">{unique_url}</a></p>
        <p>Share this URL with your students to register.</p>
        <p>Best regards,<br>Stride Ahead Team</p>
        """
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
```

---

## Database Migrations

### Creating Migrations

```bash
# After modifying models in app/models/models.py
cd backend
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in alembic/versions/
# Then apply it:
alembic upgrade head
```

### Rollback Migrations

```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

---

## Deployment

### Docker Setup

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: stride_events
      POSTGRES_USER: stride
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://stride:changeme@postgres:5432/stride_events
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Production Deployment Checklist

- [ ] Set strong SECRET_KEY in environment
- [ ] Configure production DATABASE_URL
- [ ] Set up SSL certificates
- [ ] Configure CORS origins properly
- [ ] Set up monitoring (Sentry, DataDog, etc.)
- [ ] Configure backup strategy for PostgreSQL
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Configure CDN for static assets
- [ ] Set up logging aggregation
- [ ] Enable rate limiting on API endpoints

---

## Next Steps

1. **Complete Frontend Components**: Implement all sections from LPevents.pdf
2. **Add Authentication Middleware**: Implement JWT verification for admin endpoints
3. **Integrate Stride ID API**: Connect user registration flow
4. **Set up Email Templates**: Create professional HTML email templates
5. **Add Testing**: Write unit and integration tests
6. **Performance Optimization**: Add caching, database indexing
7. **Security Audit**: Review and fix security vulnerabilities

---

## Support

For questions or issues, contact the Stride Ahead development team.
