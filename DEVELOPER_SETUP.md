# Developer Setup Guide

**For:** Fixing integration issues and getting the landing page running locally  
**Time:** 15-20 minutes  
**Prerequisites:** Node.js 18+, Python 3.11+, PostgreSQL 16

---

## 🎯 Goal

Get the AI Olympiad landing page running with FastAPI backend on your local machine.

---

## 📋 Step-by-Step Instructions

### Step 1: Clone and Understand the Structure

```bash
git clone https://github.com/Team-Stride/stride-events-platform.git
cd stride-events-platform
```

**Project Structure:**
```
stride-events-platform/
├── backend/          ← FastAPI + PostgreSQL
├── frontend/         ← React + TypeScript + Vite
├── KNOWN_ISSUES.md   ← Read this first!
├── MIGRATION.md      ← Technical details
└── QUICKSTART.md     ← Quick reference
```

---

### Step 2: Read KNOWN_ISSUES.md

**IMPORTANT:** Before proceeding, read `KNOWN_ISSUES.md` to understand what's broken and why.

```bash
cat KNOWN_ISSUES.md
```

---

### Step 3: Fix Frontend Dependencies

```bash
cd frontend

# Install all dependencies
pnpm install

# Add missing Radix UI packages
pnpm add @radix-ui/react-tooltip @radix-ui/react-popover \
  @radix-ui/react-avatar @radix-ui/react-checkbox \
  @radix-ui/react-collapsible @radix-ui/react-context-menu \
  @radix-ui/react-dropdown-menu @radix-ui/react-hover-card \
  @radix-ui/react-menubar @radix-ui/react-navigation-menu \
  @radix-ui/react-progress @radix-ui/react-radio-group \
  @radix-ui/react-scroll-area @radix-ui/react-separator \
  @radix-ui/react-slider @radix-ui/react-switch \
  @radix-ui/react-toggle @radix-ui/react-toggle-group \
  input-otp vaul recharts date-fns react-day-picker
```

---

### Step 4: Fix `const.ts`

**File:** `frontend/src/const.ts`

Replace entire file with:

```typescript
export const COOKIE_NAME = "session";
export const ONE_YEAR_MS = 365 * 24 * 60 * 60 * 1000;

export const APP_TITLE = "Stride Ahead Events Platform";
export const APP_LOGO = "/logo.svg";

export const getLoginUrl = () => {
  // TODO: Implement FastAPI auth flow
  return "/api/auth/login";
};
```

---

### Step 5: Fix `main.tsx`

**File:** `frontend/src/main.tsx`

Replace entire file with:

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from './components/ui/sonner'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
        <Toaster />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
```

---

### Step 6: Fix `EventLanding.tsx`

**File:** `frontend/src/pages/EventLanding.tsx`

Make these changes:

**Change 1:** Remove unused import
```typescript
// Line 6: Remove DialogTrigger
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
```

**Change 2:** Fix student registration mutation (around line 61)
```typescript
// Remove eventId from the mutation data
registerStudentMutation.mutate({
  first_name: formData.get("firstName") as string,
  last_name: formData.get("lastName") as string,
  // ... rest of fields
  // ❌ Remove: eventId: event!.id,
});
```

**Change 3:** Fix school registration mutation (around line 77)
```typescript
// Change schoolName to school_name
registerSchoolMutation.mutate({
  school_name: formData.get("schoolName") as string,  // ← Changed
  contact_person: formData.get("contactPerson") as string,
  // ... rest of fields
});
```

**Change 4:** Remove or fix navigate call (around line 99)
```typescript
// Option A: Remove the entire button with navigate()
// Option B: Add this import at top
import { useNavigate } from 'react-router-dom';
// Then add in component:
const navigate = useNavigate();
```

---

### Step 7: Fix `App.tsx`

**File:** `frontend/src/App.tsx`

Remove the admin route (since AdminDashboard doesn't exist):

```typescript
import { Routes, Route } from 'react-router-dom'
import EventLanding from './pages/EventLanding'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<EventLanding />} />
      <Route path="/events/:slug" element={<EventLanding />} />
      {/* Removed: <Route path="/admin" element={<AdminDashboard />} /> */}
    </Routes>
  )
}

export default App
```

---

### Step 8: Create Environment File

**File:** `frontend/.env`

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

---

### Step 9: Test Frontend Build

```bash
cd frontend
pnpm run build
```

**Expected Output:**
```
✓ built in XXXms
```

**If you see errors:**
- Check KNOWN_ISSUES.md
- Verify all files were fixed correctly
- Check for typos in your edits

---

### Step 10: Set Up Backend

```bash
cd ../backend

# Install Python dependencies
pip install -r requirements.txt

# Set up database
# Option A: Use PostgreSQL (production)
export DATABASE_URL="postgresql://user:pass@localhost:5432/stride_events"

# Option B: Use SQLite (development)
export DATABASE_URL="sqlite:///./stride_events.db"

# Run migrations
alembic upgrade head

# Seed the AI Olympiad event
python -m app.scripts.seed_data
```

---

### Step 11: Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend is running:**
```bash
curl http://localhost:8000/
# Should return: {"message": "Stride Events API"}

curl http://localhost:8000/api/v1/events/ai-olympiad-2025
# Should return event JSON
```

---

### Step 12: Start Frontend

**In a new terminal:**

```bash
cd frontend
pnpm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

### Step 13: Test the Landing Page

1. Open browser: `http://localhost:5173/events/ai-olympiad-2025`
2. **Verify:**
   - ✅ Page loads without errors
   - ✅ Hero section displays correctly
   - ✅ All 17 sections render
   - ✅ Sticky CTA strip at bottom
   - ✅ Registration buttons open modal
3. **Test registration:**
   - Click "Register as Student"
   - Fill out form
   - Submit
   - Check browser console for API call
   - Check backend logs for request

---

## 🐛 Troubleshooting

### Issue: "Cannot find module '@radix-ui/...'"

**Solution:** Run Step 3 again to install missing dependencies.

---

### Issue: "CORS error" in browser console

**Solution:** Add CORS middleware to FastAPI backend:

```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue: "Event not found" error

**Solution:** Seed the database:

```bash
cd backend
python -m app.scripts.seed_data
```

---

### Issue: TypeScript errors during build

**Solution:**
1. Check you completed Steps 4-7 correctly
2. Review KNOWN_ISSUES.md for specific error
3. Delete `node_modules` and reinstall:
   ```bash
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

---

### Issue: Backend won't start

**Solution:**
1. Check PostgreSQL is running
2. Verify DATABASE_URL is correct
3. Run migrations: `alembic upgrade head`
4. Check Python version: `python --version` (should be 3.11+)

---

## ✅ Success Checklist

- [ ] All dependencies installed
- [ ] All 7 files fixed (const.ts, main.tsx, EventLanding.tsx, App.tsx, api.ts, .env)
- [ ] Frontend builds without errors
- [ ] Backend starts without errors
- [ ] Database seeded with AI Olympiad event
- [ ] Landing page loads at localhost:5173
- [ ] Registration form submits successfully
- [ ] Toast notifications appear

---

## 🚀 Next Steps

Once everything works locally:

1. **Replace placeholder images** - Mentors, partners, hero
2. **Test payment integration** - Razorpay/Stripe
3. **Test email notifications** - SendGrid
4. **Test WhatsApp notifications** - Karix
5. **Deploy to production** - Follow DEPLOYMENT_GUIDE.md

---

## 📚 Additional Resources

- **KNOWN_ISSUES.md** - Detailed issue explanations
- **MIGRATION.md** - Technical migration details
- **QUICKSTART.md** - Quick reference guide
- **API Docs** - http://localhost:8000/docs (after starting backend)

---

## 💬 Questions?

If you're stuck:
1. Re-read KNOWN_ISSUES.md
2. Check browser console for errors
3. Check backend logs for API errors
4. Verify all steps were completed in order

---

**Good luck! 🚀**

---

**Last Updated:** November 9, 2025  
**Maintainer:** Stride Ahead Engineering Team
