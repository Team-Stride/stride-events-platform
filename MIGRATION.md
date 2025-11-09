# AI Olympiad Landing Page Migration

**Date:** November 9, 2025  
**Migrated From:** Node.js + tRPC prototype  
**Migrated To:** FastAPI + React production codebase

---

## 🎯 What Was Done

This migration ports the complete AI Olympiad landing page UI from a Node.js/tRPC prototype to the production FastAPI + React stack.

### Files Added/Modified

#### Frontend (`frontend/src/`)

**New Files:**
- `pages/EventLanding.tsx` - Complete landing page with all sections and CTAs
- `components/ui/*` - 50+ shadcn/ui components (buttons, dialogs, cards, etc.)
- `lib/api.ts` - REST API client for FastAPI backend
- `lib/utils.ts` - Utility functions (cn helper for Tailwind)
- `const.ts` - App constants (APP_TITLE, APP_LOGO)
- `index.css` - Global styles with Tailwind CSS variables and theme configuration

**Modified Files:**
- `package.json` - Added Radix UI dependencies for shadcn/ui components
- `App.tsx` - Already had routing configured (no changes needed)

---

## 📦 New Dependencies

Added to `package.json`:

```json
{
  "@radix-ui/react-accordion": "^1.1.2",
  "@radix-ui/react-alert-dialog": "^1.0.5",
  "@radix-ui/react-dialog": "^1.0.5",
  "@radix-ui/react-tabs": "^1.0.4",
  "@radix-ui/react-slot": "^1.0.2",
  "@radix-ui/react-label": "^2.0.2",
  "@radix-ui/react-select": "^2.0.0",
  "sonner": "^1.3.1"
}
```

**Why these dependencies?**
- Radix UI provides accessible, unstyled component primitives
- shadcn/ui builds on top of Radix UI with beautiful Tailwind styling
- Sonner provides toast notifications

---

## 🔄 Key Technical Changes

### 1. Data Fetching: tRPC → React Query + REST API

**Before (tRPC):**
```typescript
const { data: event } = trpc.events.getBySlug.useQuery({ slug });
const registerStudent = trpc.registrations.registerStudent.useMutation({...});
```

**After (React Query + REST):**
```typescript
const { data: event } = useQuery({
  queryKey: ['event', slug],
  queryFn: () => eventApi.getBySlug(slug),
});

const registerStudentMutation = useMutation({
  mutationFn: (data) => eventApi.registerStudent(eventId, data),
  onSuccess: () => toast.success("Registration successful!"),
});
```

### 2. API Client Structure

Created `lib/api.ts` with typed API methods:

```typescript
export const eventApi = {
  getBySlug: async (slug: string): Promise<Event> => {
    const response = await api.get(`/events/${slug}`);
    return response.data;
  },
  
  registerStudent: async (eventId: number, data: StudentRegistration) => {
    const response = await api.post(`/registrations/student`, {
      event_id: eventId,
      ...data,
    });
    return response.data;
  },
};
```

### 3. Form Data Mapping

Student registration form fields map to FastAPI schema:

| Frontend Field | Backend Field | Type | Required |
|---|---|---|---|
| firstName | first_name | string | ✅ |
| lastName | last_name | string | ✅ |
| email | email | string | ✅ |
| mobile | mobile | string | ✅ |
| grade | grade | string | ✅ |
| age | age | number | ✅ |
| stream | stream | string | ❌ |
| schoolName | school_name | string | ✅ |
| city | city | string | ✅ |
| state | state | string | ✅ |
| couponCode | coupon_code | string | ❌ |

---

## 🎨 Landing Page Structure

The EventLanding.tsx component includes these sections (in order):

1. **Hero Section** - Gradient background, headline, CTAs, registration deadline
2. **Event Information Table** - Mode, dates, fee, attempt window
3. **What is AI Olympiad** - Description + 3 feature cards
4. **4-Box Value Grid** - Numbered value propositions (1-4)
5. **Why Participate** - 5 benefit cards with icons
6. **CTA Section #1** - After Why Participate
7. **How It Works** - 4-step timeline
8. **Prizes & Rewards** - 3 prize tiers (₹30k/₹15k/₹10k) + certificates
9. **CTA Section #2** - After Prizes
10. **Judging Criteria** - 5 evaluation criteria
11. **CTA Section #3** - After Judging Criteria
12. **Mentor Profiles** - 10 mentor cards + "100+ mentors" callout
13. **CTA Section #4** - After Mentors
14. **Backed By & Featured In** - 11 partner logos
15. **FAQ Section** - 11 questions with accordion UI
16. **Stride Ecosystem** - 4 feature cards + CTA
17. **Sticky Bottom CTA Strip** - Fixed at bottom, always visible
18. **Footer** - Minimal "Powered by Stride Ahead"

### CTA Strategy

**5 conversion points:**
- Hero section (primary CTA)
- After Why Participate (blue gradient)
- After Prizes (yellow border with trophy emoji)
- After Judging Criteria (indigo gradient)
- After Mentors (green gradient)
- Sticky bottom strip (always visible)

Each CTA has both "Register as Student" and "Register as School" buttons.

---

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `frontend/.env`:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

For production:
```bash
VITE_API_URL=https://api.strideahead.in/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

Output will be in `frontend/dist/`

---

## 🔗 Backend Integration

The landing page expects these FastAPI endpoints:

### GET `/api/v1/events/{slug}`

Returns event details:

```json
{
  "id": 1,
  "slug": "ai-olympiad-2025",
  "title": "AI Olympiad 2025",
  "description": "...",
  "start_date": "2025-12-15",
  "end_date": "2025-12-25",
  "registration_deadline": "2025-12-31",
  "base_fee": 99,
  "is_active": true
}
```

### POST `/api/v1/registrations/student`

Accepts student registration:

```json
{
  "event_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "mobile": "+919876543210",
  "grade": "10",
  "age": 15,
  "stream": "science_pcm",
  "school_name": "ABC School",
  "city": "Mumbai",
  "state": "Maharashtra",
  "coupon_code": "KEEPSTRIDING"
}
```

### POST `/api/v1/registrations/school`

Accepts school registration:

```json
{
  "event_id": 1,
  "school_name": "ABC School",
  "contact_person": "Principal Name",
  "email": "principal@abcschool.com",
  "mobile": "+919876543210",
  "city": "Mumbai",
  "state": "Maharashtra",
  "num_students": 50
}
```

---

## 🎨 Styling & Theming

### Tailwind Configuration

The landing page uses Tailwind CSS 3.x with custom theme variables defined in `index.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    /* ... more variables ... */
  }
}
```

### Color Palette

- **Primary:** Blue gradient (blue-600 to purple-600)
- **Accent:** Yellow for highlights and borders
- **Success:** Green for positive actions
- **Neutral:** Gray scale for text and backgrounds

### Responsive Design

- Mobile-first approach
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
- Sticky CTA strip adapts to mobile with stacked buttons

---

## 🧪 Testing Checklist

Before deployment, verify:

- [ ] Event data loads from `/api/v1/events/{slug}`
- [ ] Student registration form submits successfully
- [ ] School registration form submits successfully
- [ ] Coupon code "KEEPSTRIDING" applies 100% discount
- [ ] Toast notifications appear on success/error
- [ ] Sticky CTA strip remains fixed on scroll
- [ ] All 5 CTA sections trigger registration modal
- [ ] FAQ accordion expands/collapses correctly
- [ ] Registration modal switches between Student/School tabs
- [ ] Form validation works (required fields, email format, age range)
- [ ] Mobile responsive design works on all screen sizes

---

## 🐛 Known Issues / TODOs

1. **Placeholder Images**
   - Mentor photos are placeholder icons
   - Partner logos are placeholder icons
   - Hero image is a robot icon
   - **Action:** Replace with actual images

2. **Event Data**
   - Currently hardcoded to "ai-olympiad-2025" slug
   - **Action:** Ensure backend has this event seeded

3. **Payment Integration**
   - Registration forms collect data but don't process payment
   - **Action:** Integrate Razorpay/Stripe payment flow

4. **Email Notifications**
   - Backend should send confirmation emails after registration
   - **Action:** Verify SendGrid integration is working

5. **WhatsApp Notifications**
   - Backend should send WhatsApp messages via Karix
   - **Action:** Verify Karix integration is working

---

## 📝 Code Quality Notes

### Component Structure

- Single-file component (1173 lines) - consider splitting into smaller components
- All UI logic in one file - could extract form components
- Inline styles using Tailwind - no custom CSS needed

### Type Safety

- TypeScript interfaces defined in `lib/api.ts`
- Form data properly typed
- API responses typed

### Accessibility

- Semantic HTML elements used
- ARIA labels on interactive elements (via Radix UI)
- Keyboard navigation supported
- Focus management in modals

---

## 🤝 Developer Handoff

**For the next developer:**

1. Read this document first
2. Check `lib/api.ts` to understand API integration
3. Review `pages/EventLanding.tsx` for component structure
4. Test all registration flows locally
5. Replace placeholder images with real assets
6. Verify backend endpoints match expected schemas
7. Test payment integration thoroughly

**Questions?** Contact the Stride Ahead engineering team.

---

**Migration completed by:** Manus AI Agent  
**Review required by:** Stride Ahead Developer Team  
**Deployment target:** Production (strideahead.in)
