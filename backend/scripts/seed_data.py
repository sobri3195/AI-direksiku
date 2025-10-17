import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.candidate import Candidate
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)


def create_sample_candidates(db: Session, count: int = 10):
    sample_data = [
        {
            "full_name": "Ahmad Hidayat",
            "email": "ahmad.hidayat@email.com",
            "phone": "081234567890",
            "nik": "3201012345678901",
            "education_level": "S1",
            "institution": "Universitas Indonesia",
            "major": "Administrasi Publik",
            "graduation_year": 2020,
            "linkedin_url": "https://linkedin.com/in/ahmadhidayat",
            "twitter_username": "@ahmadhidayat",
            "facebook_url": "https://facebook.com/ahmad.hidayat",
            "applied_position": "Analis Kebijakan"
        },
        {
            "full_name": "Siti Nurhaliza",
            "email": "siti.nurhaliza@email.com",
            "phone": "081234567891",
            "nik": "3201012345678902",
            "education_level": "S2",
            "institution": "Universitas Gadjah Mada",
            "major": "Manajemen Publik",
            "graduation_year": 2019,
            "linkedin_url": "https://linkedin.com/in/sitinurhaliza",
            "twitter_username": "@sitinurhaliza",
            "applied_position": "Perencana Ahli Muda"
        },
        {
            "full_name": "Budi Santoso",
            "email": "budi.santoso@email.com",
            "phone": "081234567892",
            "nik": "3201012345678903",
            "education_level": "S1",
            "institution": "Institut Teknologi Bandung",
            "major": "Teknik Informatika",
            "graduation_year": 2021,
            "linkedin_url": "https://linkedin.com/in/budisantoso",
            "twitter_username": "@budisantoso",
            "facebook_url": "https://facebook.com/budi.santoso",
            "instagram_username": "@budisantoso",
            "applied_position": "Analis Sistem Informasi"
        },
        {
            "full_name": "Dewi Kusuma",
            "email": "dewi.kusuma@email.com",
            "phone": "081234567893",
            "nik": "3201012345678904",
            "education_level": "S2",
            "institution": "Universitas Padjadjaran",
            "major": "Hukum Administrasi Negara",
            "graduation_year": 2018,
            "linkedin_url": "https://linkedin.com/in/dewikusuma",
            "applied_position": "Analis Hukum"
        },
        {
            "full_name": "Eko Prasetyo",
            "email": "eko.prasetyo@email.com",
            "phone": "081234567894",
            "nik": "3201012345678905",
            "education_level": "S1",
            "institution": "Universitas Brawijaya",
            "major": "Ekonomi Pembangunan",
            "graduation_year": 2020,
            "linkedin_url": "https://linkedin.com/in/ekoprasetyo",
            "twitter_username": "@ekoprasetyo",
            "applied_position": "Analis Anggaran"
        },
        {
            "full_name": "Fitri Handayani",
            "email": "fitri.handayani@email.com",
            "phone": "081234567895",
            "nik": "3201012345678906",
            "education_level": "S1",
            "institution": "Universitas Diponegoro",
            "major": "Ilmu Komunikasi",
            "graduation_year": 2021,
            "linkedin_url": "https://linkedin.com/in/fitrihandayani",
            "twitter_username": "@fitrihandayani",
            "facebook_url": "https://facebook.com/fitri.handayani",
            "instagram_username": "@fitrihandayani",
            "applied_position": "Pranata Humas"
        },
        {
            "full_name": "Gunawan Wijaya",
            "email": "gunawan.wijaya@email.com",
            "phone": "081234567896",
            "nik": "3201012345678907",
            "education_level": "S2",
            "institution": "Institut Pemerintahan Dalam Negeri",
            "major": "Kebijakan Publik",
            "graduation_year": 2019,
            "linkedin_url": "https://linkedin.com/in/gunawanwijaya",
            "applied_position": "Perencana Ahli Madya"
        },
        {
            "full_name": "Hesti Rahmawati",
            "email": "hesti.rahmawati@email.com",
            "phone": "081234567897",
            "nik": "3201012345678908",
            "education_level": "S1",
            "institution": "Universitas Airlangga",
            "major": "Psikologi",
            "graduation_year": 2020,
            "linkedin_url": "https://linkedin.com/in/hestirahmawati",
            "twitter_username": "@hestirahmawati",
            "applied_position": "Analis SDM Aparatur"
        },
        {
            "full_name": "Indra Gunawan",
            "email": "indra.gunawan@email.com",
            "phone": "081234567898",
            "nik": "3201012345678909",
            "education_level": "S1",
            "institution": "Universitas Hasanuddin",
            "major": "Akuntansi",
            "graduation_year": 2021,
            "linkedin_url": "https://linkedin.com/in/indragunawan",
            "twitter_username": "@indragunawan",
            "facebook_url": "https://facebook.com/indra.gunawan",
            "applied_position": "Auditor"
        },
        {
            "full_name": "Julia Kartika",
            "email": "julia.kartika@email.com",
            "phone": "081234567899",
            "nik": "3201012345678910",
            "education_level": "S2",
            "institution": "Universitas Indonesia",
            "major": "Administrasi Negara",
            "graduation_year": 2018,
            "linkedin_url": "https://linkedin.com/in/juliakartika",
            "twitter_username": "@juliakartika",
            "instagram_username": "@juliakartika",
            "applied_position": "Analis Reformasi Birokrasi"
        }
    ]
    
    candidates_created = []
    
    for i in range(min(count, len(sample_data))):
        data = sample_data[i].copy()
        data['application_date'] = datetime.utcnow() - timedelta(days=random.randint(1, 30))
        data['address'] = f"Jakarta, Indonesia"
        data['date_of_birth'] = datetime(1995 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28))
        
        existing = db.query(Candidate).filter(Candidate.email == data['email']).first()
        if not existing:
            candidate = Candidate(**data)
            db.add(candidate)
            candidates_created.append(data['full_name'])
    
    db.commit()
    
    print(f"✅ Created {len(candidates_created)} sample candidates:")
    for name in candidates_created:
        print(f"   - {name}")


def main():
    print("🌱 Seeding database with sample data...")
    
    db = SessionLocal()
    
    try:
        create_sample_candidates(db, count=10)
        print("\n✅ Database seeded successfully!")
        print("\nYou can now:")
        print("1. Start the backend server: uvicorn app.main:app --reload")
        print("2. Visit http://localhost:8000/docs to test the API")
        print("3. Create screening analyses for the candidates")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
