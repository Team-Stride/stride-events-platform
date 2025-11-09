# Quick Start Guide - AI Olympiad Landing Page

**For Developers:** Get the landing page running in 5 minutes.

---

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 16
- Git

---

## 🚀 Setup (5 minutes)

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/Team-Stride/stride-events-platform.git
cd stride-events-platform

# Install frontend dependencies
cd frontend
npm install
```

### 2. Configure Environment

Create `frontend/.env`:

```bash
# For local development
VITE_API_URL=http://localhost:8000/api/v1

# For production
# VITE_API_URL=https://api.strideahead.in/api/v1
```

### 3. Start Backend (FastAPI)

```bash
# In a new terminal, from project root
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed the AI Olympiad event
python -m app.scripts.seed_data

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be at: `http://localhost:8000`  
API docs at: `http://localhost:8000/docs`

### 4. Start Frontend (React)

```bash
# In another terminal, from frontend directory
npm run dev
```

Frontend will be at: `http://localhost:5173`

### 5. View Landing Page

Open browser: `http://localhost:5173/events/ai-olympiad-2025`

---

## 🧪 Test Registration Flow

### Student Registration

1. Click "Register as Student" button
2. Fill in the form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Mobile: +919876543210
   - Grade: 10
   - Age: 15
   - Stream: Science PCM
   - School: ABC School
   - City: Mumbai
   - State: Maharashtra
   - Coupon Code: KEEPSTRIDING (for free entry)
3. Click "Submit Registration"
4. Check console for API response
5. Verify email sent (check SendGrid logs)
6. Verify WhatsApp sent (check Karix logs)

### School Registration

1. Click "Register as School" button
2. Fill in the form:
   - School Name: ABC School
   - Contact Person: Principal Name
   - Email: principal@abcschool.com
   - Mobile: +919876543210
   - City: Mumbai
   - State: Maharashtra
   - Number of Students: 50
3. Click "Submit School Registration"
4. Note the unique school ID in the success message

---

## 📁 Key Files to Know

```
stride-events-platform/
├── MIGRATION.md              ← Read this first! Complete technical docs
├── QUICKSTART.md            ← You are here
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── events.py           ← Event endpoints
│   │   │   └── registrations.py   ← Registration endpoints
│   │   ├── models/models.py        ← Database models
│   │   ├── schemas/schemas.py      ← Pydantic schemas
│   │   └── services/
│   │       ├── payments.py         ← Razorpay/Stripe integration
│   │       └── whatsapp.py         ← Karix WhatsApp API
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   └── EventLanding.tsx    ← Main landing page (1173 lines)
    │   ├── components/ui/          ← 50+ shadcn/ui components
    │   ├── lib/
    │   │   ├── api.ts              ← FastAPI REST client
    │   │   └── utils.ts            ← Utility functions
    │   ├── const.ts                ← App constants
    │   └── index.css               ← Tailwind theme
    └── package.json
```

---

## 🔧 Common Issues & Fixes

### Issue: "Cannot connect to backend"

**Fix:**
```bash
# Check backend is running
curl http://localhost:8000/api/v1/events/ai-olympiad-2025

# If not running, start FastAPI:
cd backend && uvicorn app.main:app --reload
```

### Issue: "Event not found"

**Fix:**
```bash
# Seed the database
cd backend
python -m app.scripts.seed_data
```

### Issue: "Module not found" errors in frontend

**Fix:**
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Radix UI components not rendering"

**Fix:**
```bash
# Ensure all dependencies installed
cd frontend
npm install @radix-ui/react-dialog @radix-ui/react-tabs @radix-ui/react-accordion
```

### Issue: "Tailwind styles not working"

**Fix:**
```bash
# Rebuild Tailwind
cd frontend
npm run build
npm run dev
```

---

## 🎨 Customization Guide

### Change Event Content

Edit `backend/app/scripts/seed_data.py` to modify:
- Event title, description, dates
- Registration deadline
- Base fee
- Event slug

Then re-seed:
```bash
python -m app.scripts.seed_data
```

### Change Colors/Theme

Edit `frontend/src/index.css`:

```css
:root {
  --primary: 221.2 83.2% 53.3%;  /* Blue */
  --secondary: 210 40% 96.1%;     /* Light gray */
  /* ... more variables ... */
}
```

### Add/Remove Sections

Edit `frontend/src/pages/EventLanding.tsx`:
- Each section is clearly commented
- Remove entire `<section>` blocks
- Or duplicate and modify for new sections

### Change CTA Text

Search for "Register as Student" and "Register as School" in `EventLanding.tsx` and replace.

---

## 📊 API Testing with cURL

### Get Event Details
```bash
curl http://localhost:8000/api/v1/events/ai-olympiad-2025
```

### Register Student
```bash
curl -X POST http://localhost:8000/api/v1/registrations/student \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "mobile": "+919876543210",
    "grade": "10",
    "age": 15,
    "school_name": "ABC School",
    "city": "Mumbai",
    "state": "Maharashtra",
    "coupon_code": "KEEPSTRIDING"
  }'
```

### Register School
```bash
curl -X POST http://localhost:8000/api/v1/registrations/school \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "school_name": "ABC School",
    "contact_person": "Principal Name",
    "email": "principal@abcschool.com",
    "mobile": "+919876543210",
    "city": "Mumbai",
    "state": "Maharashtra",
    "num_students": 50
  }'
```

---

## 🚢 Deployment

### Frontend (Vercel/Netlify)

```bash
# Build for production
cd frontend
npm run build

# Output in frontend/dist/
# Deploy dist/ folder to Vercel/Netlify
```

### Backend (AWS Lambda/EC2)

See `DEPLOYMENT_GUIDE.md` for complete instructions.

---

## 📚 Need More Help?

1. **Technical Details:** Read `MIGRATION.md`
2. **API Documentation:** Visit `http://localhost:8000/docs`
3. **Component Library:** Check [shadcn/ui docs](https://ui.shadcn.com/)
4. **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
5. **React Query:** [tanstack.com/query](https://tanstack.com/query/latest)

---

## ✅ Checklist Before Going Live

- [ ] Backend running on production server
- [ ] Database migrations applied
- [ ] AI Olympiad event seeded in production DB
- [ ] Environment variables configured (VITE_API_URL, etc.)
- [ ] Razorpay/Stripe API keys configured
- [ ] SendGrid API key configured
- [ ] Karix WhatsApp API credentials configured
- [ ] Frontend built and deployed
- [ ] SSL certificate configured (HTTPS)
- [ ] Test student registration end-to-end
- [ ] Test school registration end-to-end
- [ ] Verify email notifications working
- [ ] Verify WhatsApp notifications working
- [ ] Test payment flow with real money (small amount)
- [ ] Replace placeholder images with real assets
- [ ] Test on mobile devices
- [ ] Test on different browsers (Chrome, Safari, Firefox)
- [ ] Set up error monitoring (Sentry)
- [ ] Set up analytics (Google Analytics)

---

**Happy coding! 🚀**

Questions? Contact: engineering@strideahead.in
