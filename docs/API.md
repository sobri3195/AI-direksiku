# AI-DiReksi API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API does not require authentication. In production, implement JWT-based authentication.

## Endpoints

### Candidates

#### Create Candidate
```http
POST /candidates
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "081234567890",
  "nik": "1234567890123456",
  "address": "Jakarta",
  "education_level": "S1",
  "institution": "University of Indonesia",
  "major": "Public Administration",
  "graduation_year": 2020,
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "twitter_username": "@johndoe",
  "facebook_url": "https://facebook.com/johndoe",
  "instagram_username": "@johndoe",
  "applied_position": "Analis Kebijakan"
}
```

#### Get All Candidates
```http
GET /candidates?skip=0&limit=100&status_filter=pending
```

#### Get Candidate by ID
```http
GET /candidates/{candidate_id}
```

#### Update Candidate
```http
PUT /candidates/{candidate_id}
Content-Type: application/json

{
  "full_name": "John Doe Updated",
  "status": "screened_layak"
}
```

#### Delete Candidate
```http
DELETE /candidates/{candidate_id}
```

### Screening

#### Start Screening Analysis
```http
POST /screening/analyze
Content-Type: application/json

{
  "candidate_id": 1,
  "platforms": ["linkedin", "twitter", "facebook"],
  "deep_analysis": true
}
```

Response:
```json
{
  "id": 1,
  "candidate_id": 1,
  "overall_score": 85.5,
  "technical_score": 0.0,
  "social_score": 78.0,
  "digital_ethics_score": 90.0,
  "professionalism_score": 88.0,
  "sentiment_score": 85.0,
  "positive_content_ratio": 0.75,
  "negative_content_ratio": 0.10,
  "neutral_content_ratio": 0.15,
  "recommendation": "layak",
  "recommendation_reason": "Kandidat menunjukkan jejak digital yang positif...",
  "risk_flags": {},
  "positive_indicators": {
    "clean_digital_record": {
      "description": "Jejak digital bersih tanpa konten negatif"
    }
  },
  "analyzed_at": "2024-01-16T10:30:00"
}
```

#### Get Screening Results
```http
GET /screening/{candidate_id}/results
```

#### Get Screening Result by ID
```http
GET /screening/result/{result_id}
```

#### Get Digital Footprints
```http
GET /screening/{candidate_id}/digital-footprints
```

#### Get Statistics
```http
GET /screening/statistics/summary
```

Response:
```json
{
  "total_screenings": 150,
  "recommendations": {
    "layak": 90,
    "dipertimbangkan": 40,
    "tidak_layak": 20
  },
  "average_scores": {
    "overall": 75.5,
    "digital_ethics": 82.3,
    "professionalism": 78.9
  },
  "success_rate": 60.0
}
```

### Dashboard

#### Get Merit Dashboard
```http
GET /dashboard/merit
```

Response:
```json
{
  "overview": {
    "total_candidates": 200,
    "total_screened": 150,
    "pending_screening": 50,
    "layak_candidates": 90,
    "screening_completion_rate": 75.0
  },
  "top_candidates": [],
  "recent_screenings": []
}
```

#### Get Analytics
```http
GET /dashboard/analytics
```

#### Get Risk Assessment
```http
GET /dashboard/risk-assessment
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "detail": "Error message description"
}
```

## Recommendation Values

- `layak` - Candidate is suitable
- `dipertimbangkan` - Candidate requires consideration
- `tidak_layak` - Candidate is not suitable

## Scoring System

All scores are on a scale of 0-100:

- **Overall Score**: Weighted combination of all component scores
- **Digital Ethics Score**: Based on content appropriateness and behavior
- **Professionalism Score**: Based on professional presence and communication
- **Sentiment Score**: Based on overall sentiment of social media content
- **Social Score**: Based on social media engagement and presence

## Interactive Documentation

Visit `/docs` for Swagger UI interactive documentation.
Visit `/redoc` for ReDoc interactive documentation.
