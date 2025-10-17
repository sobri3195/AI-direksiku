from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.screening import ScreeningResult, DigitalFootprint
from app.schemas.screening import (
    ScreeningResultResponse,
    ScreeningRequest,
    DigitalFootprintResponse
)
from app.services.screening_service import ScreeningService

router = APIRouter()


@router.post("/analyze", response_model=ScreeningResultResponse, status_code=status.HTTP_201_CREATED)
def start_screening_analysis(
    request: ScreeningRequest,
    db: Session = Depends(get_db)
):
    screening_service = ScreeningService(db)
    
    try:
        screening_result = screening_service.conduct_screening(request.candidate_id)
        return screening_result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Screening analysis failed: {str(e)}"
        )


@router.get("/{candidate_id}/results", response_model=List[ScreeningResultResponse])
def get_screening_results(candidate_id: int, db: Session = Depends(get_db)):
    results = db.query(ScreeningResult).filter(
        ScreeningResult.candidate_id == candidate_id
    ).order_by(ScreeningResult.analyzed_at.desc()).all()
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No screening results found for this candidate"
        )
    
    return results


@router.get("/result/{result_id}", response_model=ScreeningResultResponse)
def get_screening_result_by_id(result_id: int, db: Session = Depends(get_db)):
    result = db.query(ScreeningResult).filter(ScreeningResult.id == result_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening result not found"
        )
    
    return result


@router.get("/{candidate_id}/digital-footprints", response_model=List[DigitalFootprintResponse])
def get_digital_footprints(candidate_id: int, db: Session = Depends(get_db)):
    footprints = db.query(DigitalFootprint).filter(
        DigitalFootprint.candidate_id == candidate_id
    ).order_by(DigitalFootprint.scraped_at.desc()).all()
    
    return footprints


@router.get("/statistics/summary")
def get_screening_statistics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    total_screenings = db.query(func.count(ScreeningResult.id)).scalar()
    
    layak_count = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "layak"
    ).scalar()
    
    dipertimbangkan_count = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "dipertimbangkan"
    ).scalar()
    
    tidak_layak_count = db.query(func.count(ScreeningResult.id)).filter(
        ScreeningResult.recommendation == "tidak_layak"
    ).scalar()
    
    avg_overall_score = db.query(func.avg(ScreeningResult.overall_score)).scalar() or 0
    avg_ethics_score = db.query(func.avg(ScreeningResult.digital_ethics_score)).scalar() or 0
    avg_professionalism = db.query(func.avg(ScreeningResult.professionalism_score)).scalar() or 0
    
    return {
        "total_screenings": total_screenings or 0,
        "recommendations": {
            "layak": layak_count or 0,
            "dipertimbangkan": dipertimbangkan_count or 0,
            "tidak_layak": tidak_layak_count or 0
        },
        "average_scores": {
            "overall": round(float(avg_overall_score), 2),
            "digital_ethics": round(float(avg_ethics_score), 2),
            "professionalism": round(float(avg_professionalism), 2)
        },
        "success_rate": round((layak_count or 0) / max(total_screenings or 1, 1) * 100, 2)
    }
