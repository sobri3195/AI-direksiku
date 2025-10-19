from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class DigitalFootprintResponse(BaseModel):
    id: int
    candidate_id: int
    platform: str
    profile_url: Optional[str]
    username: Optional[str]
    display_name: Optional[str]
    bio: Optional[str]
    follower_count: Optional[int]
    following_count: Optional[int]
    post_count: Optional[int]
    scraped_at: datetime
    scraping_status: str

    class Config:
        from_attributes = True


class SentimentAnalysisResponse(BaseModel):
    id: int
    platform: Optional[str]
    content_type: Optional[str]
    content_text: Optional[str]
    sentiment_label: Optional[str]
    sentiment_score: Optional[float]
    confidence: Optional[float]
    contains_profanity: int
    contains_hate_speech: int
    contains_political_content: int
    analyzed_at: datetime

    class Config:
        from_attributes = True


class ScreeningResultResponse(BaseModel):
    id: int
    candidate_id: int
    overall_score: Optional[float]
    technical_score: Optional[float]
    social_score: Optional[float]
    digital_ethics_score: Optional[float]
    professionalism_score: Optional[float]
    sentiment_score: Optional[float]
    positive_content_ratio: Optional[float]
    negative_content_ratio: Optional[float]
    neutral_content_ratio: Optional[float]
    recommendation: Optional[str]
    recommendation_reason: Optional[str]
    risk_flags: Optional[Dict[str, Any]]
    positive_indicators: Optional[Dict[str, Any]]
    ai_analysis_summary: Optional[str]
    detailed_report: Optional[Dict[str, Any]]
    analyzed_at: datetime
    sentiment_analyses: Optional[List[SentimentAnalysisResponse]] = []

    class Config:
        from_attributes = True


class ScreeningRequest(BaseModel):
    candidate_id: int
    platforms: Optional[List[str]] = ["linkedin", "twitter", "facebook"]
    deep_analysis: bool = True


class TextAnalysisRequest(BaseModel):
    texts: List[str]
