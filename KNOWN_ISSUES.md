# Known Issues & Fixes

**Last Updated:** November 9, 2025  
**Status:** UI ported from Node.js, needs integration fixes

---

## 🚨 Critical Issues

These issues will prevent the frontend from building. They MUST be fixed before deployment.

### 1. Missing Radix UI Dependencies

**Problem:**  
Many shadcn/ui components require Radix UI packages that aren't in package.json.

**Error:**
```
Cannot find module '@radix-ui/react-tooltip'
Cannot find module '@radix-ui/react-popover'
Cannot find module '@radix-ui/react-avatar'
... (and 15+ more)
```

**Fix:**
```bash
cd frontend
pnpm add @radix-ui/react-aspect-ratio embla-carousel-react \
  cmdk react-hook-form react-resizable-panels next-themes
```

**Note:** Most Radix UI packages are already installed. Only the above 6 packages are missing.

**Files Affected:**
- `src/components/ui/tooltip.tsx`
- `src/components/ui/popover.tsx`
- `src/components/ui/avatar.tsx`
- `src/components/ui/checkbox.tsx`
- `src/components/ui/calendar.tsx`
- `src/components/ui/carousel.tsx`
- `src/components/ui/chart.tsx`
- ... (30+ UI component files)

---

### 2. Invalid Import in `const.ts`

**Problem:**  
`const.ts` tries to import from `@shared/const` which doesn't exist in FastAPI project (Node.js-specific).

**Error:**
```
Cannot find module '@shared/const'
Property 'env' does not exist on type 'ImportMeta'
```

**Current Code:**
```typescript
export { COOKIE_NAME, ONE_YEAR_MS } from "@shared/const";
export const APP_TITLE = import.meta.env.VITE_APP_TITLE || "App";
export const APP_LOGO = import.meta.env.VITE_APP_LOGO || "/logo.svg";
```

**Fix:**  
Replace `frontend/src/const.ts` with:

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

**Files Affected:**
- `src/const.ts`

---

### 3. Missing Redux Store

**Problem:**  
`main.tsx` imports Redux store that doesn't exist in FastAPI project.

**Error:**
```
Cannot find module './store/store'
```

**Current Code:**
```typescript
import { Provider } from 'react-redux'
import { store } from './store/store'
```

**Fix:**  
Remove Redux dependencies from `frontend/src/main.tsx`:

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

**Files Affected:**
- `src/main.tsx`

---

### 4. TypeScript Errors in `EventLanding.tsx`

**Problem:**  
Several TypeScript type mismatches and unused imports.

**Errors:**
```
'DialogTrigger' is declared but its value is never read
'eventId' does not exist in type 'StudentRegistration'
'schoolName' does not exist in type 'SchoolRegistration'. Did you mean 'school_name'?
Cannot find name 'navigate'
```

**Fix 1:** Remove unused import
```typescript
// Before
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

// After
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
```

**Fix 2:** Remove `eventId` from mutation call (it's passed separately)
```typescript
// Before
registerStudentMutation.mutate({
  eventId: event!.id,
  first_name: formData.get("firstName") as string,
  // ...
});

// After
registerStudentMutation.mutate({
  first_name: formData.get("firstName") as string,
  // ...
});
```

**Fix 3:** Fix field name mismatch
```typescript
// Before
registerSchoolMutation.mutate({
  schoolName: formData.get("schoolName") as string,
  // ...
});

// After
registerSchoolMutation.mutate({
  school_name: formData.get("schoolName") as string,
  // ...
});
```

**Fix 4:** Remove navigate call (or import from react-router-dom)
```typescript
// Option A: Remove the button
// Option B: Import useNavigate
import { useNavigate } from 'react-router-dom';
// Then in component:
const navigate = useNavigate();
```

**Files Affected:**
- `src/pages/EventLanding.tsx`

---

### 5. API Type Mismatch

**Problem:**  
The API client types don't match the mutation calls.

**Current API Types:**
```typescript
export interface StudentRegistration {
  first_name: string;
  last_name: string;
  email: string;
  mobile: string;
  grade: string;
  age: number;
  stream?: string;
  school_name: string;
  city: string;
  state: string;
  coupon_code?: string;
}
```

**Mutation Call Includes:**
```typescript
{
  event_id: eventId,  // ❌ Not in interface
  ...data
}
```

**Fix:**  
The `eventApi.registerStudent()` function already adds `event_id`, so don't include it in the mutation data.

**Files Affected:**
- `src/lib/api.ts`
- `src/pages/EventLanding.tsx`

---

## ⚠️ Non-Critical Issues

These won't prevent building but should be fixed for production.

### 6. Hardcoded API URL

**Problem:**  
API URL is hardcoded in `lib/api.ts` instead of using environment variable.

**Current Code:**
```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

**Fix:**  
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
```

Then create `frontend/.env`:
```bash
VITE_API_URL=http://localhost:8000/api/v1
```

For production:
```bash
VITE_API_URL=https://api.strideahead.in/api/v1
```

**Files Affected:**
- `src/lib/api.ts`

---

### 7. Missing Admin Dashboard Pages

**Problem:**  
`App.tsx` routes to `/admin` but `AdminDashboard` component doesn't exist.

**Error:**
```
Cannot find module './pages/admin/Dashboard'
```

**Fix:**  
Either:
- **Option A:** Remove the admin route from `App.tsx`
- **Option B:** Create a placeholder admin dashboard

**Files Affected:**
- `src/App.tsx`

---

## 📋 Complete Fix Checklist

Run these commands in order:

```bash
# 1. Install missing dependencies
cd frontend
pnpm add @radix-ui/react-aspect-ratio embla-carousel-react \
  cmdk react-hook-form react-resizable-panels next-themes

# 2. Fix const.ts (see Issue #2 above)

# 3. Fix main.tsx (see Issue #3 above)

# 4. Fix EventLanding.tsx (see Issue #4 above)

# 5. Create .env file
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# 6. Try building
pnpm run build

# 7. If successful, start dev server
pnpm run dev
```

---

## 🧪 Testing After Fixes

1. **Backend:** Start FastAPI server on port 8000
2. **Frontend:** Start React dev server on port 5173
3. **Test:** Navigate to `http://localhost:5173/events/ai-olympiad-2025`
4. **Verify:**
   - Page loads without errors
   - Event data fetches from backend
   - Registration forms submit successfully
   - Toast notifications appear

---

## 📞 Need Help?

If you encounter issues not listed here:

1. Check browser console for errors
2. Check backend logs for API errors
3. Verify backend is running and accessible
4. Check CORS configuration in FastAPI

**Common CORS Issue:**

If you see CORS errors, add to FastAPI backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Related Documentation

- **MIGRATION.md** - Complete technical migration details
- **QUICKSTART.md** - 5-minute setup guide
- **README.md** - Project overview

---

**Last Updated:** November 9, 2025  
**Maintainer:** Stride Ahead Engineering Team
