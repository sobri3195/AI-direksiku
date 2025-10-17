# AI-DiReksi - Project Summary

## 📋 Project Overview

**AI-DiReksi** (Digital Recruitment System using AI) adalah sistem seleksi Aparatur Sipil Negara (ASN) berbasis kecerdasan buatan yang menganalisis jejak digital calon pegawai untuk memberikan rekomendasi objektif dalam proses rekrutmen.

### 🎯 Tujuan Proyek

1. Meningkatkan objektivitas dalam seleksi ASN
2. Menganalisis integritas kandidat melalui jejak digital
3. Mendukung meritokrasi dalam rekrutmen
4. Mempercepat proses screening kandidat
5. Mengurangi bias subjektif dalam penilaian

### 🌟 Fitur Utama

#### 1. Smart Candidate Screening
- Machine learning untuk analisis profil kandidat
- Pattern recognition untuk kesesuaian kompetensi
- Fit score: teknis, sosial, dan digital

#### 2. Digital Footprint Analysis
- Web scraping multi-platform (LinkedIn, Twitter, Facebook, Instagram)
- Sentiment analysis untuk etika komunikasi
- Deteksi profesionalisme dan risiko perilaku
- Rekomendasi otomatis: Layak/Dipertimbangkan/Tidak Layak

#### 3. AI Behavioral Assessment
- Analisis emotional intelligence
- Decision-making pattern analysis
- Evaluasi etika digital

#### 4. Dashboard & Analytics
- Merit dashboard dengan visualisasi data
- Real-time statistics
- Risk assessment
- Performance tracking

## 🏗️ Arsitektur Teknis

### Technology Stack

#### Backend
```
- Framework: FastAPI (Python 3.11+)
- Database: PostgreSQL 14+
- ORM: SQLAlchemy 2.0+
- AI/ML: scikit-learn, transformers
- NLP: spaCy, NLTK, TextBlob
- Web Scraping: BeautifulSoup4, Selenium
```

#### Frontend
```
- Framework: React 18+
- UI Library: Material-UI 5+
- Routing: React Router 6+
- HTTP Client: Axios
- Charts: Recharts
```

#### Infrastructure
```
- Containerization: Docker & Docker Compose
- Web Server: Nginx (production)
- ASGI Server: Uvicorn/Gunicorn
- Version Control: Git
```

### Database Schema

#### Main Tables

1. **candidates** - Data kandidat
   - Personal information (name, email, NIK, etc.)
   - Education background
   - Social media accounts
   - Application details

2. **screening_results** - Hasil screening
   - Overall scores (0-100)
   - Component scores (ethics, professionalism, sentiment, social)
   - Recommendation (layak/dipertimbangkan/tidak_layak)
   - Risk flags and positive indicators

3. **digital_footprints** - Jejak digital
   - Platform information
   - Profile data
   - Posts and engagement metrics
   - Scraping metadata

4. **sentiment_analyses** - Analisis sentimen
   - Content text and type
   - Sentiment labels and scores
   - Risk indicators (profanity, hate speech, political content)
   - Keywords and entities

5. **users** - Admin users
   - Authentication credentials
   - Role-based access
   - Activity tracking

### API Endpoints Structure

```
/api/v1/
├── candidates/                  # Candidate management
│   ├── POST /                  # Create candidate
│   ├── GET /                   # List candidates
│   ├── GET /{id}              # Get candidate
│   ├── PUT /{id}              # Update candidate
│   └── DELETE /{id}           # Delete candidate
│
├── screening/                   # Screening operations
│   ├── POST /analyze          # Start screening
│   ├── GET /{id}/results      # Get results
│   ├── GET /result/{id}       # Get result by ID
│   ├── GET /{id}/digital-footprints  # Get footprints
│   └── GET /statistics/summary # Get statistics
│
└── dashboard/                   # Dashboard & analytics
    ├── GET /merit             # Merit dashboard
    ├── GET /analytics         # Analytics data
    └── GET /risk-assessment   # Risk assessment
```

## 📊 Scoring Algorithm

### Score Components (Weighted)

```python
Overall Score = (
    Sentiment Score × 30% +
    Professionalism Score × 25% +
    Digital Ethics Score × 25% +
    Social Score × 20%
)
```

### Score Calculation Details

#### 1. Sentiment Score (0-100)
- Average sentiment from all content
- Positive content ratio
- Negative content penalty
- Based on TextBlob polarity analysis

#### 2. Professionalism Score (0-100)
- Base score: 70
- LinkedIn presence: +10
- Professional bio: +10
- High follower count: +5
- Profanity penalty: -5 per occurrence

#### 3. Digital Ethics Score (0-100)
- Base score: 80
- Hate speech: -20 per occurrence (critical)
- Profanity: -5 per occurrence
- High negativity: -50 × (ratio - 0.3)

#### 4. Social Score (0-100)
- Base score: 60
- Multiple platforms: +5 per platform (max +20)
- High followers (>1000): +10
- Active posting (>100 posts): +10

### Risk Flags

#### Critical Severity
- Hate speech content → Automatic "Tidak Layak"

#### High Severity
- Excessive profanity (≥3 occurrences)
- Strong recommendation against

#### Medium Severity
- High negativity ratio (≥50%)
- Requires careful consideration

#### Low Severity
- Political activity (>10 posts)
- Requires manual review

### Recommendation Logic

```
IF hate_speech OR critical_flags:
    → Tidak Layak (Not Suitable)
ELIF high_severity_flags OR score < 60:
    → Dipertimbangkan (Needs Consideration)
ELIF score >= 75:
    → Layak (Suitable)
ELSE:
    → Dipertimbangkan (Needs Consideration)
```

## 📁 Project Structure

```
ai-direksi-asn-digital-screening/
│
├── backend/                         # Backend application
│   ├── app/
│   │   ├── api/                    # API endpoints
│   │   │   └── v1/
│   │   │       ├── candidates.py   # Candidate CRUD
│   │   │       ├── screening.py    # Screening operations
│   │   │       └── dashboard.py    # Dashboard & analytics
│   │   │
│   │   ├── core/                   # Core functionality
│   │   │   ├── config.py          # Configuration
│   │   │   ├── database.py        # Database connection
│   │   │   └── security.py        # Security functions
│   │   │
│   │   ├── models/                 # Database models
│   │   │   ├── candidate.py       # Candidate model
│   │   │   ├── screening.py       # Screening models
│   │   │   └── user.py            # User model
│   │   │
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── candidate.py       # Candidate schemas
│   │   │   ├── screening.py       # Screening schemas
│   │   │   └── user.py            # User schemas
│   │   │
│   │   ├── services/               # Business logic
│   │   │   ├── ai/
│   │   │   │   ├── sentiment_analyzer.py  # Sentiment analysis
│   │   │   │   └── scoring_engine.py      # Score calculation
│   │   │   ├── scraping/
│   │   │   │   └── social_media_scraper.py # Web scraping
│   │   │   └── screening_service.py        # Main screening logic
│   │   │
│   │   └── main.py                 # FastAPI application
│   │
│   ├── scripts/
│   │   └── seed_data.py           # Sample data seeder
│   │
│   ├── tests/                      # Backend tests
│   │   ├── test_api.py            # API tests
│   │   └── test_services.py       # Service tests
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend Docker image
│   └── .env.example               # Environment template
│
├── frontend/                       # Frontend application
│   ├── public/
│   │   └── index.html             # HTML template
│   │
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.js          # App layout with sidebar
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.js       # Main dashboard
│   │   │   ├── CandidatesList.js  # Candidate list
│   │   │   ├── CandidateForm.js   # Add/edit candidate
│   │   │   ├── ScreeningResults.js # Screening results
│   │   │   └── Analytics.js       # Analytics page
│   │   │
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   │
│   │   ├── App.js                 # Main App component
│   │   └── index.js               # React entry point
│   │
│   ├── package.json                # Node dependencies
│   └── Dockerfile                  # Frontend Docker image
│
├── docs/                           # Documentation
│   ├── API.md                     # API documentation
│   └── DEPLOYMENT.md              # Deployment guide
│
├── docker-compose.yml              # Docker Compose config
├── setup.sh                        # Setup script
├── .gitignore                     # Git ignore rules
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── CONTRIBUTING.md                # Contributing guide
├── CHANGELOG.md                   # Version history
├── LICENSE                        # MIT License
└── PROJECT_SUMMARY.md             # This file
```

## 🚀 Deployment

### Development
```bash
./setup.sh
```

### Production (Docker)
```bash
docker-compose up -d
```

### Manual Production
See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Performance Metrics

### Expected Performance
- API Response Time: < 200ms (average)
- Screening Time: 5-10 seconds per candidate
- Concurrent Users: 100+ (with proper scaling)
- Database Queries: Optimized with indexes

### Scalability
- Horizontal scaling ready
- Stateless API design
- Database connection pooling
- Redis caching support (optional)

## 🔒 Security Features

### Implemented
- Password hashing (bcrypt)
- SQL injection prevention (SQLAlchemy ORM)
- CORS protection
- Input validation (Pydantic)
- Environment variable for secrets

### Recommended for Production
- JWT authentication
- HTTPS/SSL encryption
- Rate limiting
- API key management
- Audit logging
- Regular security audits

## 📊 Data Privacy & Compliance

### Indonesian Data Protection
- Compliant with UU PDP (Undang-Undang Perlindungan Data Pribadi)
- Data minimization principle
- Purpose limitation
- Data retention policies (90 days default)
- User consent mechanisms

### Ethical AI
- Bias detection monitoring
- Transparent scoring algorithm
- Explainable recommendations
- Human oversight required
- Regular fairness audits

## 🎓 Sample Use Case

### Scenario: Screening New Candidate

1. **Input**: HR menambahkan kandidat "Ahmad Hidayat"
   - Data pribadi: Nama, Email, NIK
   - Pendidikan: S1 Administrasi Publik
   - Media sosial: LinkedIn, Twitter

2. **Process**: Sistem melakukan:
   - Scraping profil LinkedIn → 500 followers, bio profesional
   - Scraping Twitter → 50 tweets, sentimen 80% positif
   - Analisis konten → Tidak ada profanity/hate speech
   - Kalkulasi skor → 85/100

3. **Output**: Rekomendasi "LAYAK"
   - Overall Score: 85/100
   - Digital Ethics: 90/100
   - Professionalism: 88/100
   - Sentiment: 85/100
   - Social: 78/100
   
4. **Decision**: HR review hasil dan lanjutkan proses seleksi

## 🔄 Future Roadmap

### Phase 2 (Q2 2024)
- [ ] Real social media API integration
- [ ] Advanced Indonesian NLP model
- [ ] Machine learning model training
- [ ] Mobile application (Flutter)

### Phase 3 (Q3 2024)
- [ ] Integration with SIASN
- [ ] Behavioral assessment simulations
- [ ] Advanced talent mapping
- [ ] Predictive analytics

### Phase 4 (Q4 2024)
- [ ] Blockchain verification
- [ ] Public accountability portal
- [ ] Multi-tenant support
- [ ] AI bias mitigation tools

## 👥 Team & Support

### Development Team
- Backend Engineers
- Frontend Engineers
- AI/ML Engineers
- DevOps Engineers
- Security Specialists

### Support Channels
- Email: support@ai-direksi.go.id
- Documentation: [README.md](README.md)
- Issue Tracker: GitHub Issues

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Badan Kepegawaian Negara (BKN)
- SIASN Development Team
- Open Source Community Indonesia
- All contributors and supporters

---

**Version**: 1.0.0  
**Last Updated**: January 16, 2024  
**Status**: Production Ready (with noted limitations)

For questions or contributions, see [CONTRIBUTING.md](CONTRIBUTING.md)
