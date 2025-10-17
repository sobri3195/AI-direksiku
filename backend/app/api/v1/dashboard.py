from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.core.database import get_db
from app.models.candidate import Candidate
from app.models.screening import ScreeningResult
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/merit")
def get_merit_dashboard(db: Session = Depends(get_db)):
    total_candidates = db.query(func.count(Candidate.id)).scalar() or 0
    
    total_screened = db.query(func.count(ScreeningResult.id)).scalar() or 0
    
    pending_screening = db.query(func.count(Candidate.id)).filter(
        Candidate.status == "pending"
    ).scalar() or 0
    
    layak_candidates = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "layak"
    ).scalar() or 0
    
    top_candidates = db.query(ScreeningResult).join(Candidate).filter(
        ScreeningResult.recommendation == "layak"
    ).order_by(ScreeningResult.overall_score.desc()).limit(10).all()
    
    top_candidates_data = [
        {
            "candidate_id": result.candidate_id,
            "candidate_name": result.candidate.full_name,
            "overall_score": result.overall_score,
            "recommendation": result.recommendation,
            "digital_ethics_score": result.digital_ethics_score,
            "professionalism_score": result.professionalism_score,
            "analyzed_at": result.analyzed_at.isoformat()
        }
        for result in top_candidates
    ]
    
    recent_screenings = db.query(ScreeningResult).join(Candidate).order_by(
        ScreeningResult.analyzed_at.desc()
    ).limit(5).all()
    
    recent_screenings_data = [
        {
            "id": result.id,
            "candidate_id": result.candidate_id,
            "candidate_name": result.candidate.full_name,
            "overall_score": result.overall_score,
            "recommendation": result.recommendation,
            "analyzed_at": result.analyzed_at.isoformat()
        }
        for result in recent_screenings
    ]
    
    return {
        "overview": {
            "total_candidates": total_candidates,
            "total_screened": total_screened,
            "pending_screening": pending_screening,
            "layak_candidates": layak_candidates,
            "screening_completion_rate": round((total_screened / max(total_candidates, 1)) * 100, 2)
        },
        "top_candidates": top_candidates_data,
        "recent_screenings": recent_screenings_data
    }


@router.get("/analytics")
def get_analytics_dashboard(db: Session = Depends(get_db)):
    score_distribution = db.query(
        func.count(ScreeningResult.id).label('count'),
        ScreeningResult.recommendation
    ).group_by(ScreeningResult.recommendation).all()
    
    score_dist_data = {
        "layak": 0,
        "dipertimbangkan": 0,
        "tidak_layak": 0
    }
    
    for count, recommendation in score_distribution:
        if recommendation:
            score_dist_data[recommendation] = count
    
    avg_scores = db.query(
        func.avg(ScreeningResult.overall_score).label('avg_overall'),
        func.avg(ScreeningResult.digital_ethics_score).label('avg_ethics'),
        func.avg(ScreeningResult.professionalism_score).label('avg_professionalism'),
        func.avg(ScreeningResult.sentiment_score).label('avg_sentiment'),
        func.avg(ScreeningResult.social_score).label('avg_social')
    ).first()
    
    avg_scores_data = {
        "overall": round(float(avg_scores.avg_overall or 0), 2),
        "digital_ethics": round(float(avg_scores.avg_ethics or 0), 2),
        "professionalism": round(float(avg_scores.avg_professionalism or 0), 2),
        "sentiment": round(float(avg_scores.avg_sentiment or 0), 2),
        "social": round(float(avg_scores.avg_social or 0), 2)
    }
    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_trend = db.query(
        func.date(ScreeningResult.analyzed_at).label('date'),
        func.count(ScreeningResult.id).label('count')
    ).filter(
        ScreeningResult.analyzed_at >= seven_days_ago
    ).group_by(
        func.date(ScreeningResult.analyzed_at)
    ).all()
    
    trend_data = [
        {
            "date": date.isoformat() if date else None,
            "count": count
        }
        for date, count in recent_trend
    ]
    
    return {
        "score_distribution": score_dist_data,
        "average_scores": avg_scores_data,
        "screening_trend_7days": trend_data
    }


@router.get("/risk-assessment")
def get_risk_assessment_dashboard(db: Session = Depends(get_db)):
    high_risk = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "tidak_layak"
    ).scalar() or 0
    
    medium_risk = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "dipertimbangkan"
    ).scalar() or 0
    
    low_risk = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "layak"
    ).scalar() or 0
    
    flagged_candidates = db.query(ScreeningResult).join(Candidate).filter(
        or_(
            ScreeningResult.recommendation == "tidak_layak",
            ScreeningResult.recommendation == "dipertimbangkan"
        )
    ).order_by(ScreeningResult.overall_score.asc()).limit(20).all()
    
    flagged_data = [
        {
            "candidate_id": result.candidate_id,
            "candidate_name": result.candidate.full_name,
            "overall_score": result.overall_score,
            "recommendation": result.recommendation,
            "risk_flags": result.risk_flags,
            "analyzed_at": result.analyzed_at.isoformat()
        }
        for result in flagged_candidates
    ]
    
    return {
        "risk_summary": {
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk,
            "total": high_risk + medium_risk + low_risk
        },
        "flagged_candidates": flagged_data
    }
