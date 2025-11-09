# Stride Ahead Events Platform

**Production-Ready FastAPI + React Competition Platform**

A complete, production-grade events and competition management platform built with Stride Ahead's tech stack, featuring payment processing, WhatsApp notifications, and multi-tenant architecture.

---

## 🎯 Features

### Core Functionality
- ✅ **Event Management** - Create and manage competitions, olympiads, and events
- ✅ **Student Registration** - Individual student sign-ups with payment
- ✅ **School Registration** - Bulk registration for schools (free with auto-coupon)
- ✅ **Payment Gateway** - Razorpay & Stripe integration with coupon system
- ✅ **WhatsApp Notifications** - Karix API integration for all event triggers
- ✅ **Email Service** - SendGrid integration for transactional emails
- ✅ **Admin Dashboard** - Complete CMS for event and registration management
- ✅ **Assessment Integration** - Ready for Stride Ahead Assessment API
- ✅ **Multi-Tenancy** - Built-in tenant isolation

### Pricing & Coupons
- **Registration Fee:** ₹99 per student
- **KEEPSTRIDING Coupon:** 100% discount (free registration)
- **School Registration:** Free (auto-applied SCHOOL_FREE coupon)
- **Early Bird:** 50% discount with EARLYBIRD coupon

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI 0.110+** - Modern async web framework
- **PostgreSQL 16** - Primary database
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **Pydantic 2.x** - Data validation

### Frontend
- **React 18**
- **TypeScript 5.x**
- **Vite 5.x** - Build tool
- **Tailwind CSS 3.x** - Styling
- **Redux Toolkit 2.x** - Global state
- **React Query 5.x** - Server state

### Integrations
- **Razorpay** - Payment gateway (primary)
- **Stripe** - Payment gateway (alternative)
- **Karix** - WhatsApp messaging
- **SendGrid** - Email service
- **Stride ID** - Authentication (SSO)
- **Assessment API** - Test delivery

---

## 🚀 Quick Start

See DEPLOYMENT_GUIDE.md for complete setup instructions.

---

## 📚 Documentation

- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Complete code for all components
- **[API_INTEGRATION_GUIDE.md](./API_INTEGRATION_GUIDE.md)** - Stride ID, SendGrid, Assessment APIs
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Production deployment guide
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - What's done, what's needed

---

**Built with ❤️ by Stride Ahead Engineering Team**
