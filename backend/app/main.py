from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1 import candidates, screening, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistem Analisis Jejak Digital Berbasis AI untuk Seleksi ASN yang Berintegritas",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    candidates.router,
    prefix=f"{settings.API_V1_PREFIX}/candidates",
    tags=["Candidates"]
)

app.include_router(
    screening.router,
    prefix=f"{settings.API_V1_PREFIX}/screening",
    tags=["Screening"]
)

app.include_router(
    dashboard.router,
    prefix=f"{settings.API_V1_PREFIX}/dashboard",
    tags=["Dashboard"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI-DiReksi API",
        "version": settings.APP_VERSION,
        "description": "Sistem Analisis Jejak Digital Berbasis AI untuk Seleksi ASN",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
