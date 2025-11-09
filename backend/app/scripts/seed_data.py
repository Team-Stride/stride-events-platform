"""
Seed script for test data
Creates sample event, coupons, and test registrations
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select

from app.core.database import get_db_session
from app.models.models import Event, Coupon, StudentRegistration, SchoolRegistration


async def seed_data():
    """Seed database with test data"""
    
    async for db in get_db_session():
        print("🌱 Seeding database with test data...")
        
        # 1. Create AI Olympiad Event
        print("📅 Creating AI Olympiad 2025 event...")
        event_id = uuid.uuid4()
        event = Event(
            id=event_id,
            tenant_id=uuid.uuid4(),  # Replace with actual tenant ID
            slug="ai-olympiad-2025",
            title="AI Olympiad 2025",
            tagline="Empowering Young Minds to Shape the Future with AI",
            description="Join India's premier AI competition for high school students",
            event_type="competition",
            category="ai_ml",
            registration_fee=9900,  # ₹99 in paise
            early_bird_fee=9900,
            currency="INR",
            start_date=datetime(2025, 2, 15, 10, 0),
            end_date=datetime(2025, 2, 15, 14, 0),
            registration_deadline=datetime(2025, 2, 10, 23, 59),
            max_participants=5000,
            min_age=14,
            max_age=18,
            target_grades="9-12",
            status="published",
            is_active=True,
            banner_image_url="https://example.com/ai-olympiad-banner.jpg",
            content={
                "what_is": "A national-level AI competition for high school students...",
                "why_participate": [
                    "Win exciting prizes worth ₹5 Lakhs",
                    "Get certificates from Stride Ahead",
                    "Mentorship from AI experts",
                    "Internship opportunities"
                ],
                "how_it_works": [
                    "Register for the event",
                    "Complete the online assessment",
                    "Top performers win prizes",
                    "All participants get certificates"
                ],
                "prizes": {
                    "first": "₹1,00,000 + Trophy + Certificate",
                    "second": "₹50,000 + Trophy + Certificate",
                    "third": "₹25,000 + Trophy + Certificate",
                    "top_100": "Certificates of Excellence"
                },
                "faqs": [
                    {
                        "question": "Who can participate?",
                        "answer": "Students in grades 9-12 can participate."
                    },
                    {
                        "question": "Is coding knowledge required?",
                        "answer": "No, the competition is designed for beginners."
                    }
                ]
            },
            assessment_config={
                "duration_minutes": 60,
                "total_questions": 30,
                "passing_score": 50
            }
        )
        
        db.add(event)
        await db.commit()
        print(f"✅ Event created: {event.title} (ID: {event.id})")
        
        # 2. Create KEEPSTRIDING coupon (100% discount)
        print("🎟️  Creating KEEPSTRIDING coupon...")
        coupon_keepstriding = Coupon(
            id=uuid.uuid4(),
            tenant_id=event.tenant_id,
            code="KEEPSTRIDING",
            description="100% discount for all students",
            discount_type="percentage",
            discount_value=100,
            min_amount=0,
            max_discount=9900,
            valid_from=datetime.utcnow(),
            valid_until=datetime(2025, 12, 31, 23, 59),
            max_uses=10000,
            used_count=0,
            applicable_to="student",
            event_id=event_id,
            is_active=True
        )
        
        db.add(coupon_keepstriding)
        
        # 3. Create SCHOOL_FREE coupon (auto-applied for schools)
        print("🏫 Creating SCHOOL_FREE coupon...")
        coupon_school = Coupon(
            id=uuid.uuid4(),
            tenant_id=event.tenant_id,
            code="SCHOOL_FREE",
            description="Free registration for schools",
            discount_type="percentage",
            discount_value=100,
            min_amount=0,
            max_discount=9900,
            valid_from=datetime.utcnow(),
            valid_until=datetime(2025, 12, 31, 23, 59),
            max_uses=1000,
            used_count=0,
            applicable_to="school",
            event_id=event_id,
            is_active=True
        )
        
        db.add(coupon_school)
        
        # 4. Create EARLYBIRD coupon (50% discount)
        print("🐦 Creating EARLYBIRD coupon...")
        coupon_earlybird = Coupon(
            id=uuid.uuid4(),
            tenant_id=event.tenant_id,
            code="EARLYBIRD",
            description="50% early bird discount",
            discount_type="percentage",
            discount_value=50,
            min_amount=0,
            max_discount=4950,
            valid_from=datetime.utcnow(),
            valid_until=datetime(2025, 1, 31, 23, 59),
            max_uses=500,
            used_count=0,
            applicable_to="all",
            event_id=event_id,
            is_active=True
        )
        
        db.add(coupon_earlybird)
        
        await db.commit()
        print("✅ Coupons created: KEEPSTRIDING, SCHOOL_FREE, EARLYBIRD")
        
        # 5. Create sample school registration
        print("🏫 Creating sample school registration...")
        school_id = uuid.uuid4()
        school = SchoolRegistration(
            id=school_id,
            tenant_id=event.tenant_id,
            event_id=event_id,
            school_name="Delhi Public School",
            school_code=f"DPS{uuid.uuid4().hex[:6].upper()}",
            contact_person_name="Principal Sharma",
            contact_person_email="principal@dps.edu",
            contact_person_mobile="+919876543210",
            school_address="Sector 45, Gurgaon, Haryana",
            city="Gurgaon",
            state="Haryana",
            pincode="122003",
            expected_participants=50,
            status="confirmed"
        )
        
        db.add(school)
        await db.commit()
        print(f"✅ School registered: {school.school_name} (Code: {school.school_code})")
        
        # 6. Create sample student registrations
        print("👨‍🎓 Creating sample student registrations...")
        
        students = [
            {
                "name": "Rahul Kumar",
                "email": "rahul@example.com",
                "mobile": "+919876543211",
                "grade": "11",
                "school_name": "Delhi Public School",
                "school_id": school_id
            },
            {
                "name": "Priya Sharma",
                "email": "priya@example.com",
                "mobile": "+919876543212",
                "grade": "12",
                "school_name": "Ryan International School",
                "school_id": None
            },
            {
                "name": "Amit Patel",
                "email": "amit@example.com",
                "mobile": "+919876543213",
                "grade": "10",
                "school_name": "DAV Public School",
                "school_id": None
            }
        ]
        
        for student_data in students:
            student = StudentRegistration(
                id=uuid.uuid4(),
                tenant_id=event.tenant_id,
                event_id=event_id,
                registration_code=f"REG{uuid.uuid4().hex[:8].upper()}",
                student_name=student_data["name"],
                email=student_data["email"],
                mobile=student_data["mobile"],
                grade=student_data["grade"],
                school_name=student_data["school_name"],
                school_id=student_data["school_id"],
                city="Delhi",
                state="Delhi",
                parent_mobile="+919876543200",
                dietary_requirements="None",
                registration_source="direct" if not student_data["school_id"] else "school",
                payment_status="pending",
                amount_paid=0,
                status="registered"
            )
            
            db.add(student)
            print(f"   ✅ {student_data['name']} registered")
        
        await db.commit()
        
        print("\n🎉 Database seeded successfully!")
        print("\n📊 Summary:")
        print(f"   - 1 Event: AI Olympiad 2025")
        print(f"   - 3 Coupons: KEEPSTRIDING, SCHOOL_FREE, EARLYBIRD")
        print(f"   - 1 School: Delhi Public School")
        print(f"   - 3 Students: Rahul, Priya, Amit")
        print("\n🔗 Test URLs:")
        print(f"   - Event Page: http://localhost:3000/events/ai-olympiad-2025")
        print(f"   - School Registration: http://localhost:3000/school-register")
        print(f"   - Admin Dashboard: http://localhost:8000/admin")


if __name__ == "__main__":
    asyncio.run(seed_data())
