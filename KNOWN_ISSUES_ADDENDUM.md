# Additional Issues Found During Testing

## Issue #8: Missing Custom Hooks

**Problem:**  
Several UI components import custom hooks that don't exist in the FastAPI project.

**Errors:**
```
Cannot find module '@/hooks/useComposition'
Cannot find module '@/hooks/useMobile'
```

**Files Affected:**
- `src/components/ui/input.tsx`
- `src/components/ui/textarea.tsx`
- `src/components/ui/sidebar.tsx`

**Fix Option A: Create the missing hooks**

Create `frontend/src/hooks/useComposition.ts`:
```typescript
import { useState, useCallback } from 'react';

export function useComposition() {
  const [isComposing, setIsComposing] = useState(false);

  const onCompositionStart = useCallback(() => {
    setIsComposing(true);
  }, []);

  const onCompositionEnd = useCallback(() => {
    setIsComposing(false);
  }, []);

  return {
    isComposing,
    onCompositionStart,
    onCompositionEnd,
  };
}
```

Create `frontend/src/hooks/useMobile.ts`:
```typescript
import { useState, useEffect } from 'react';

export function useMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return isMobile;
}
```

**Fix Option B: Remove the problematic components**

If you don't need these components, you can delete them:
```bash
cd frontend/src/components/ui
rm input.tsx textarea.tsx sidebar.tsx
```

Then remove their imports from other files.

**Recommendation:** Use Option A - create the hooks. They're simple utilities that improve UX.

---

## Issue #9: Admin Dashboard Missing

**Problem:**  
`App.tsx` imports `AdminDashboard` component that doesn't exist.

**Error:**
```
Cannot find module './pages/admin/Dashboard'
```

**Fix:**

Edit `frontend/src/App.tsx` and remove the admin route:

```typescript
import { Routes, Route } from 'react-router-dom'
import EventLanding from './pages/EventLanding'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<div>Home Page - Coming Soon</div>} />
      <Route path="/events/:slug" element={<EventLanding />} />
      {/* Admin dashboard will be added later */}
    </Routes>
  )
}

export default App
```

---

## Updated Complete Fix Checklist

```bash
# 1. Install missing dependencies
cd frontend
pnpm add @radix-ui/react-aspect-ratio embla-carousel-react \
  cmdk react-hook-form react-resizable-panels next-themes

# 2. Create hooks directory and files
mkdir -p src/hooks
# Then create useComposition.ts and useMobile.ts (see above)

# 3. Fix const.ts (see KNOWN_ISSUES.md Issue #2)

# 4. Fix main.tsx (see KNOWN_ISSUES.md Issue #3)

# 5. Fix EventLanding.tsx (see KNOWN_ISSUES.md Issue #4)

# 6. Fix App.tsx (see Issue #9 above)

# 7. Create .env file
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# 8. Try building
pnpm run build

# 9. If successful, start dev server
pnpm run dev
```

---

**Testing Verified:** These issues were found by actually running `pnpm run build` and documenting every error.
