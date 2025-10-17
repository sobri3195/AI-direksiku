import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-DiReksi" in response.json()["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_candidate():
    candidate_data = {
        "full_name": "Test Candidate",
        "email": "test@example.com",
        "nik": "1234567890123456",
        "applied_position": "Test Position"
    }
    response = client.post("/api/v1/candidates/", json=candidate_data)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_get_candidates():
    response = client.get("/api/v1/candidates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_screening_statistics():
    response = client.get("/api/v1/screening/statistics/summary")
    assert response.status_code == 200
    assert "total_screenings" in response.json()


def test_dashboard_merit():
    response = client.get("/api/v1/dashboard/merit")
    assert response.status_code == 200
    assert "overview" in response.json()
