"""
Seed data script for AI Olympiad 2025 event
Run this script to populate the database with initial event data
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import json

from app.core.config import settings
from app.models.models import Event, Coupon, EventStatus
from app.core.database import Base


async def seed_ai_olympiad_event(db: AsyncSession):
    """Create AI Olympiad 2025 event with all content"""
    
    tenant_id = uuid.UUID(settings.TENANT_ID) if settings.TENANT_ID else uuid.uuid4()
    
    # Event dates
    start_date = datetime(2025, 12, 15, 0, 0, 0)
    end_date = datetime(2025, 12, 25, 23, 59, 59)
    registration_deadline = datetime(2025, 12, 31, 23, 59, 59)
    
    # Content sections (matches LPevents.pdf)
    content_sections = {
        "hero": {
            "title": "AI Olympiad: The NextGen AI Challenge 2025",
            "tagline": "Where Artificial Intelligence Meets Human Imagination",
            "description": "India's Premier AI Competition for Students"
        },
        "what_is": {
            "title": "What is the AI Olympiad?",
            "description": "The AI Olympiad is India's premier artificial intelligence competition designed to challenge and inspire the next generation of AI innovators. This groundbreaking event brings together talented students from across the country to showcase their skills in machine learning, data science, and AI problem-solving.",
            "features": [
                {
                    "icon": "🎯",
                    "title": "Real-World Challenges",
                    "description": "Tackle actual AI problems faced by industry leaders"
                },
                {
                    "icon": "🏆",
                    "title": "₹1 Lakh in Prizes",
                    "description": "Win cash prizes, internships, and recognition"
                },
                {
                    "icon": "🤝",
                    "title": "100+ Expert Mentors",
                    "description": "Learn from AI professionals and researchers"
                }
            ]
        },
        "value_grid": [
            {
                "number": 1,
                "icon": "🎓",
                "title": "Learn from Experts",
                "description": "Access exclusive workshops and mentorship from 100+ AI professionals"
            },
            {
                "number": 2,
                "icon": "💼",
                "title": "Career Opportunities",
                "description": "Top performers get internship offers from leading tech companies"
            },
            {
                "number": 3,
                "icon": "🌟",
                "title": "National Recognition",
                "description": "Get featured in media and build your professional portfolio"
            },
            {
                "number": 4,
                "icon": "🚀",
                "title": "Skill Development",
                "description": "Enhance your AI/ML skills through hands-on challenges"
            }
        ],
        "why_participate": [
            "Compete with India's brightest minds in AI and showcase your skills on a national platform",
            "Win ₹1 lakh in prizes, internship opportunities, and exclusive mentorship from industry leaders",
            "Access cutting-edge AI tools, datasets, and resources curated specifically for this competition",
            "Get personalized feedback from 100+ expert mentors and build lasting connections in the AI community",
            "Earn recognition through certificates, media features, and opportunities to present your work"
        ],
        "how_it_works": [
            {
                "step": 1,
                "title": "Register",
                "description": "Sign up individually or as a school. Registration closes December 31, 2025.",
                "date": "Dec 15-31, 2025"
            },
            {
                "step": 2,
                "title": "Prepare",
                "description": "Access study materials, attend workshops, and connect with mentors.",
                "date": "Dec 15-25, 2025"
            },
            {
                "step": 3,
                "title": "Compete",
                "description": "Attempt the AI challenge during the 10-day window. Multiple attempts allowed!",
                "date": "Jan 15-25, 2026"
            },
            {
                "step": 4,
                "title": "Win",
                "description": "Top performers announced and prizes distributed.",
                "date": "Jan 30, 2026"
            }
        ],
        "judging_criteria": [
            {
                "criterion": "Technical Accuracy",
                "weight": "30%",
                "description": "Correctness and efficiency of AI solution"
            },
            {
                "criterion": "Innovation",
                "weight": "25%",
                "description": "Creativity and novelty of approach"
            },
            {
                "criterion": "Code Quality",
                "weight": "20%",
                "description": "Clean, documented, and maintainable code"
            },
            {
                "criterion": "Problem Understanding",
                "weight": "15%",
                "description": "Depth of analysis and insights"
            },
            {
                "criterion": "Presentation",
                "weight": "10%",
                "description": "Clarity of explanation and documentation"
            }
        ]
    }
    
    # Prizes (matches LPevents.pdf)
    prizes = {
        "total": "₹1,00,000",
        "tiers": [
            {
                "rank": "1st Place",
                "amount": "₹30,000",
                "benefits": [
                    "Cash prize of ₹30,000",
                    "Internship opportunity at partner companies",
                    "1-year premium Stride Ahead membership",
                    "Featured profile on Stride Ahead platform",
                    "Certificate of Excellence"
                ]
            },
            {
                "rank": "2nd Place",
                "amount": "₹15,000",
                "benefits": [
                    "Cash prize of ₹15,000",
                    "6-month premium Stride Ahead membership",
                    "Mentorship from industry experts",
                    "Certificate of Achievement"
                ]
            },
            {
                "rank": "3rd Place",
                "amount": "₹10,000",
                "benefits": [
                    "Cash prize of ₹10,000",
                    "3-month premium Stride Ahead membership",
                    "Certificate of Participation",
                    "Access to exclusive AI resources"
                ]
            }
        ]
    }
    
    # Sponsors/Partners
    sponsors = {
        "backed_by": [
            "Google for Startups",
            "Microsoft for Startups",
            "AWS Activate",
            "NVIDIA Inception",
            "Intel AI",
            "IBM Watson",
            "Accenture",
            "Deloitte",
            "NASSCOM",
            "IIT Bombay",
            "IIIT Hyderabad"
        ]
    }
    
    # FAQs (all 11 from LPevents.pdf)
    faqs = [
        {
            "question": "Who can participate in the AI Olympiad?",
            "answer": "The AI Olympiad is open to all students in grades 9-12 across India. Both individual students and schools can register."
        },
        {
            "question": "What is the registration fee?",
            "answer": "The registration fee is ₹99 per student. Use code KEEPSTRIDING for 100% discount (limited time offer)."
        },
        {
            "question": "Can I participate as part of a team?",
            "answer": "This is an individual competition. However, schools can register multiple students who will compete individually."
        },
        {
            "question": "What topics will be covered in the competition?",
            "answer": "The competition covers machine learning fundamentals, data analysis, Python programming, neural networks, and practical AI problem-solving."
        },
        {
            "question": "Do I need prior AI/ML experience?",
            "answer": "Basic Python knowledge is recommended. We provide preparatory materials and workshops for beginners."
        },
        {
            "question": "How long is the assessment?",
            "answer": "The assessment window is 10 days (January 15-25, 2026). You can attempt multiple times during this period."
        },
        {
            "question": "What tools/software do I need?",
            "answer": "You'll need a computer with internet access. All AI tools and platforms will be provided online."
        },
        {
            "question": "How are winners selected?",
            "answer": "Winners are selected based on technical accuracy (30%), innovation (25%), code quality (20%), problem understanding (15%), and presentation (10%)."
        },
        {
            "question": "When will results be announced?",
            "answer": "Results will be announced on January 30, 2026. Winners will be notified via email and WhatsApp."
        },
        {
            "question": "What do I get if I win?",
            "answer": "Winners receive cash prizes (₹30k/₹15k/₹10k), internship opportunities, premium memberships, certificates, and national recognition."
        },
        {
            "question": "How do schools benefit from registering?",
            "answer": "Schools get a unique registration link, can track all student registrations, receive bulk updates, and get recognized for student achievements."
        }
    ]
    
    # Create event
    event = Event(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        title="AI Olympiad 2025",
        slug="ai-olympiad-2025",
        tagline="The NextGen AI Challenge",
        description="India's Premier AI Competition for Students - Where Artificial Intelligence Meets Human Imagination",
        event_type="competition",
        status=EventStatus.PUBLISHED,
        start_date=start_date,
        end_date=end_date,
        registration_deadline=registration_deadline,
        banner_image_url="https://placehold.co/1920x1080/667eea/ffffff?text=AI+Olympiad+2025",
        content_sections=json.dumps(content_sections),
        prizes=json.dumps(prizes),
        sponsors=json.dumps(sponsors),
        faqs=json.dumps(faqs),
        max_participants=10000,
        is_free=False,
        registration_fee=9900,  # ₹99 in paise
        created_by=tenant_id
    )
    
    db.add(event)
    
    # Create KEEPSTRIDING coupon (100% discount)
    coupon = Coupon(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        event_id=event.id,
        code="KEEPSTRIDING",
        discount_type="percentage",
        discount_value=100,  # 100% discount
        max_uses=None,  # Unlimited uses
        used_count=0,
        valid_from=datetime(2025, 12, 15, 0, 0, 0),
        valid_until=datetime(2025, 12, 31, 23, 59, 59),
        is_active=True,
        min_amount=0,
        applicable_to="all"
    )
    
    db.add(coupon)
    
    await db.commit()
    
    print("✅ AI Olympiad 2025 event created successfully!")
    print(f"   Event ID: {event.id}")
    print(f"   Slug: {event.slug}")
    print(f"   Registration Fee: ₹99 (use code KEEPSTRIDING for 100% off)")
    print(f"   Registration Deadline: {registration_deadline.strftime('%B %d, %Y')}")
    print(f"   Event Window: {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")


async def main():
    """Main function to run seed script"""
    print("🌱 Seeding AI Olympiad 2025 event data...")
    print(f"   Database: {settings.DATABASE_URL}")
    print()
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        await seed_ai_olympiad_event(session)
    
    await engine.dispose()
    
    print()
    print("🎉 Seed data created successfully!")
    print()
    print("Next steps:")
    print("1. Start the backend server: uvicorn app.main:app --reload")
    print("2. Access the event at: http://localhost:8000/api/v1/events/ai-olympiad-2025")
    print("3. Start the frontend: cd frontend && pnpm dev")


if __name__ == "__main__":
    asyncio.run(main())
