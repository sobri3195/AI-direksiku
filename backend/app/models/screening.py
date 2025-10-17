from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class RecommendationStatus(enum.Enum):
    LAYAK = "layak"
    DIPERTIMBANGKAN = "dipertimbangkan"
    TIDAK_LAYAK = "tidak_layak"


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    
    overall_score = Column(Float)
    technical_score = Column(Float)
    social_score = Column(Float)
    digital_ethics_score = Column(Float)
    professionalism_score = Column(Float)
    
    sentiment_score = Column(Float)
    positive_content_ratio = Column(Float)
    negative_content_ratio = Column(Float)
    neutral_content_ratio = Column(Float)
    
    recommendation = Column(SQLEnum(RecommendationStatus))
    recommendation_reason = Column(Text)
    
    risk_flags = Column(JSON)
    positive_indicators = Column(JSON)
    
    ai_analysis_summary = Column(Text)
    detailed_report = Column(JSON)
    
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    analyzed_by = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="screening_results")
    sentiment_analyses = relationship("SentimentAnalysis", back_populates="screening_result", cascade="all, delete-orphan")


class DigitalFootprint(Base):
    __tablename__ = "digital_footprints"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    
    platform = Column(String(50), nullable=False)
    profile_url = Column(String(500))
    
    username = Column(String(255))
    display_name = Column(String(255))
    bio = Column(Text)
    follower_count = Column(Integer)
    following_count = Column(Integer)
    post_count = Column(Integer)
    
    profile_data = Column(JSON)
    posts_data = Column(JSON)
    
    scraped_at = Column(DateTime, default=datetime.utcnow)
    scraping_status = Column(String(50), default="completed")
    scraping_error = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="digital_footprints")


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"

    id = Column(Integer, primary_key=True, index=True)
    screening_result_id = Column(Integer, ForeignKey("screening_results.id"), nullable=False)
    
    platform = Column(String(50))
    content_type = Column(String(50))
    content_text = Column(Text)
    content_url = Column(String(500))
    
    sentiment_label = Column(String(20))
    sentiment_score = Column(Float)
    confidence = Column(Float)
    
    contains_profanity = Column(Integer, default=0)
    contains_hate_speech = Column(Integer, default=0)
    contains_political_content = Column(Integer, default=0)
    
    keywords = Column(JSON)
    entities = Column(JSON)
    
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    screening_result = relationship("ScreeningResult", back_populates="sentiment_analyses")
