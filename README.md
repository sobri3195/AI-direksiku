# AI-DiReksi: Sistem Analisis Jejak Digital Berbasis AI untuk Seleksi ASN

![AI-DiReksi Logo](docs/logo.png)

## 🎯 Tentang Proyek

**AI-DiReksi** adalah sistem seleksi Aparatur Sipil Negara (ASN) yang cerdas dan objektif dengan menganalisis jejak digital calon pegawai menggunakan kecerdasan buatan. Aplikasi ini membantu Badan Kepegawaian Negara (BKN) dalam pengambilan keputusan berbasis data untuk mewujudkan ASN yang profesional, berintegritas, dan sesuai nilai-nilai Asta Cita.

## ✨ Fitur Utama

### 1. Smart Candidate Screening (AI Screening Engine)
- Machine learning dan Natural Language Processing (NLP) untuk menganalisis data pelamar
- Pattern recognition untuk mendeteksi kesesuaian profil dengan kompetensi jabatan ASN
- Pengelompokan kandidat berdasarkan fit score (kompetensi teknis, sosial, dan digital)

### 2. Digital Footprint Analysis
- Web scraping dari sumber publik (LinkedIn, Twitter/X, Facebook)
- Sentiment analysis untuk mendeteksi etika komunikasi dan profesionalisme
- Rekomendasi otomatis: "Layak / Dipertimbangkan / Tidak Layak"

### 3. AI Behavioral Assessment
- Simulasi perilaku berbasis AI melalui scenario-based testing
- Penilaian emotional intelligence dan decision-making pattern

### 4. Talent Management Intelligence
- Talent profiling engine dengan integrasi data dari berbagai sumber
- AI-powered talent mapping dengan clustering algorithm
- Predictive career path system

### 5. Evaluasi dan Transparansi
- Merit dashboard untuk visualisasi hasil seleksi
- AI fairness & ethics monitor untuk mendeteksi bias
- Public accountability portal

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React.js)                      │
│              Dashboard │ Admin Panel │ Reports              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┬─────────────────┬────────────────────┐   │
│  │   API Layer  │  Business Logic │   AI/ML Services   │   │
│  └──────────────┴─────────────────┴────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────────┐
│  PostgreSQL  │ │  AI Models │ │ Scraping Engine│
│   Database   │ │   (NLP)    │ │   (Social Media)│
└──────────────┘ └────────────┘ └─────────────────┘
```

## 🚀 Teknologi yang Digunakan

### Backend
- **FastAPI**: Modern, high-performance web framework
- **Python 3.11+**: Programming language
- **PostgreSQL**: Database relational
- **SQLAlchemy**: ORM untuk database
- **Pydantic**: Data validation

### AI/ML
- **scikit-learn**: Machine learning algorithms
- **transformers**: Pre-trained NLP models
- **spaCy**: NLP processing
- **NLTK**: Natural language toolkit
- **TextBlob**: Sentiment analysis

### Web Scraping
- **BeautifulSoup4**: HTML parsing
- **Selenium**: Dynamic content scraping
- **requests**: HTTP library

### Frontend
- **React.js**: UI framework
- **Material-UI**: Component library
- **Axios**: HTTP client
- **Chart.js**: Data visualization

## 📋 Prasyarat

- Python 3.11 atau lebih tinggi
- Node.js 18 atau lebih tinggi
- PostgreSQL 14 atau lebih tinggi
- Docker (opsional, untuk deployment)

## ⚙️ Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai-direksi-asn-digital-screening
```

### 2. Setup Backend

```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup database
cp .env.example .env
# Edit .env dengan konfigurasi database Anda

# Jalankan migrations
alembic upgrade head

# Download NLP models
python -m spacy download id_core_news_md

# Jalankan server
uvicorn app.main:app --reload
```

### 3. Setup Frontend

```bash
cd frontend
npm install
npm start
```

### 4. Akses Aplikasi

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📚 Dokumentasi API

Dokumentasi API interaktif tersedia di `/docs` (Swagger UI) dan `/redoc` (ReDoc) setelah menjalankan backend server.

### Endpoint Utama

- `POST /api/v1/candidates` - Registrasi kandidat baru
- `POST /api/v1/screening/analyze` - Mulai analisis digital footprint
- `GET /api/v1/screening/{candidate_id}/results` - Dapatkan hasil analisis
- `GET /api/v1/dashboard/merit` - Dashboard merit
- `POST /api/v1/talent/profile` - Buat profil talenta

## 🔒 Keamanan & Privasi

AI-DiReksi mematuhi standar keamanan dan privasi data:

- ✅ Enkripsi data (AES-256)
- ✅ Kepatuhan Undang-Undang Perlindungan Data Pribadi (UU PDP)
- ✅ Anonimisasi data untuk pelaporan publik
- ✅ Audit log untuk transparansi
- ✅ AI fairness monitoring untuk mencegah bias

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Menggunakan Docker

```bash
# Build dan jalankan semua services
docker-compose up -d

# Akses aplikasi di http://localhost
```

### Deployment Manual

Lihat [Deployment Guide](docs/deployment.md) untuk instruksi lengkap.

## 🤝 Kontribusi

Kami menerima kontribusi! Silakan baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk detail proses kontribusi.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 👥 Tim Pengembang

Dikembangkan untuk Badan Kepegawaian Negara (BKN) sebagai bagian dari inovasi digitalisasi ASN.

## 📞 Kontak & Dukungan

- Email: support@ai-direksi.go.id
- Website: https://ai-direksi.go.id
- Issue Tracker: [GitHub Issues](issues/)

## 🙏 Ucapan Terima Kasih

Terima kasih kepada:
- Badan Kepegawaian Negara (BKN)
- Tim SIASN
- Komunitas open source Indonesia

---

## 👨‍💻 Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

### 📬 Contact

- **Email**: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- **GitHub**: [github.com/sobri3195](https://github.com/sobri3195)
- **Website**: [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- **YouTube**: [Muhammad Sobri Maulana](https://www.youtube.com/@muhammadsobrimaulana6013)
- **Telegram**: [@winlin_exploit](https://t.me/winlin_exploit)
- **TikTok**: [@dr.sobri](https://www.tiktok.com/@dr.sobri)

### 💝 Support & Donation

Jika Anda merasa proyek ini bermanfaat, Anda dapat mendukung pengembangan lebih lanjut melalui:

- **Lynk.id**: [https://lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)
- **Trakteer**: [https://trakteer.id/g9mkave5gauns962u07t](https://trakteer.id/g9mkave5gauns962u07t)
- **Gumroad**: [maulanasobri.gumroad.com](https://maulanasobri.gumroad.com/)
- **Karya Karsa**: [https://karyakarsa.com/muhammadsobrimaulana](https://karyakarsa.com/muhammadsobrimaulana)
- **Nyawer**: [https://nyawer.co/MuhammadSobriMaulana](https://nyawer.co/MuhammadSobriMaulana)

### 👥 Join Our Community

- **WhatsApp Group**: [Join Here](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

---

**AI-DiReksi** - Mewujudkan ASN Digital yang Berintegritas 🇮🇩
