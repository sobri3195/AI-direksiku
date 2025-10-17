from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    nik = Column(String(16), unique=True, index=True, nullable=False)
    date_of_birth = Column(DateTime)
    address = Column(Text)
    
    education_level = Column(String(100))
    institution = Column(String(255))
    major = Column(String(255))
    graduation_year = Column(Integer)
    
    linkedin_url = Column(String(500))
    twitter_username = Column(String(100))
    facebook_url = Column(String(500))
    instagram_username = Column(String(100))
    
    applied_position = Column(String(255))
    application_date = Column(DateTime, default=datetime.utcnow)
    
    cv_file_path = Column(String(500))
    motivation_letter_path = Column(String(500))
    
    additional_data = Column(JSON)
    
    status = Column(String(50), default="pending")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    screening_results = relationship("ScreeningResult", back_populates="candidate", cascade="all, delete-orphan")
    digital_footprints = relationship("DigitalFootprint", back_populates="candidate", cascade="all, delete-orphan")
