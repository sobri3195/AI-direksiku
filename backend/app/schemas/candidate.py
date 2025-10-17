from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


class CandidateBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    nik: str = Field(..., min_length=16, max_length=16)
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    
    education_level: Optional[str] = None
    institution: Optional[str] = None
    major: Optional[str] = None
    graduation_year: Optional[int] = None
    
    linkedin_url: Optional[str] = None
    twitter_username: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_username: Optional[str] = None
    
    applied_position: str


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_username: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_username: Optional[str] = None
    status: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: int
    application_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    additional_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
