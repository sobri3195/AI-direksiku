# Quick Start Guide - AI-DiReksi

Panduan cepat untuk menjalankan AI-DiReksi dalam 5 menit!

## Prerequisites

Pastikan sudah terinstall:
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

## Instalasi Cepat

### Opsi 1: Menggunakan Script Otomatis (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd ai-direksi-asn-digital-screening

# Jalankan setup script
chmod +x setup.sh
./setup.sh
```

### Opsi 2: Docker Compose (Paling Mudah)

```bash
# Clone repository
git clone <repository-url>
cd ai-direksi-asn-digital-screening

# Start semua services
docker-compose up -d

# Lihat logs
docker-compose logs -f
```

Akses aplikasi:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Opsi 3: Manual Setup

#### 1. Setup Database

```bash
# Buat database
sudo -u postgres psql -c "CREATE DATABASE ai_direksi;"
```

#### 2. Setup Backend

```bash
cd backend

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm

# Setup environment
cp .env.example .env
# Edit .env sesuai konfigurasi Anda

# Buat tables dan seed data
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
python scripts/seed_data.py

# Jalankan server
uvicorn app.main:app --reload
```

Backend akan berjalan di http://localhost:8000

#### 3. Setup Frontend

```bash
# Buka terminal baru
cd frontend

# Install dependencies
npm install

# Setup environment
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Jalankan development server
npm start
```

Frontend akan berjalan di http://localhost:3000

## Penggunaan Aplikasi

### 1. Tambah Kandidat Baru

1. Buka http://localhost:3000
2. Klik menu "Kandidat"
3. Klik tombol "Tambah Kandidat"
4. Isi form dengan data kandidat:
   - Nama lengkap
   - Email
   - NIK (16 digit)
   - Posisi yang dilamar
   - Akun media sosial (LinkedIn, Twitter, Facebook, Instagram)
5. Klik "Simpan"

### 2. Jalankan Screening

1. Di halaman "Daftar Kandidat"
2. Klik icon "Assessment" (📊) pada kandidat yang dipilih
3. Sistem akan melakukan:
   - Scraping profil media sosial
   - Analisis sentimen konten
   - Perhitungan skor
   - Pemberian rekomendasi
4. Proses займет beberapa detik
5. Klik icon "View" (👁️) untuk melihat hasil

### 3. Lihat Hasil Screening

Hasil screening menampilkan:
- **Rekomendasi**: Layak / Dipertimbangkan / Tidak Layak
- **Skor Keseluruhan**: 0-100
- **Skor Detail**:
  - Etika Digital
  - Profesionalisme
  - Sentimen
  - Sosial
- **Analisis Sentimen**: Rasio positif/negatif/netral
- **Indikator Risiko**: Jika ditemukan
- **Indikator Positif**: Aspek positif kandidat

### 4. Lihat Dashboard

Dashboard menampilkan:
- Total kandidat
- Distribusi rekomendasi (Layak/Dipertimbangkan/Tidak Layak)
- Rata-rata skor
- Kandidat teratas
- Screening terbaru

### 5. Lihat Analytics

Analytics menampilkan:
- Distribusi rekomendasi
- Rata-rata skor komponen
- Risk assessment summary
- Kandidat yang memerlukan perhatian

## Testing API

### Menggunakan Swagger UI

1. Buka http://localhost:8000/docs
2. Expand endpoint yang ingin dicoba
3. Klik "Try it out"
4. Isi parameter/body
5. Klik "Execute"
6. Lihat response

### Menggunakan cURL

```bash
# Health check
curl http://localhost:8000/health

# Get all candidates
curl http://localhost:8000/api/v1/candidates

# Create candidate
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "nik": "1234567890123456",
    "applied_position": "Test Position",
    "linkedin_url": "https://linkedin.com/in/testuser"
  }'

# Start screening
curl -X POST http://localhost:8000/api/v1/screening/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "platforms": ["linkedin", "twitter", "facebook"],
    "deep_analysis": true
  }'

# Get screening results
curl http://localhost:8000/api/v1/screening/1/results

# Get statistics
curl http://localhost:8000/api/v1/screening/statistics/summary
```

## Troubleshooting

### Port sudah digunakan

```bash
# Cari process yang menggunakan port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill process
kill -9 <PID>
```

### Database connection error

```bash
# Pastikan PostgreSQL running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Cek koneksi
psql -U postgres -d ai_direksi
```

### Module not found

```bash
# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install
```

### NLP model error

```bash
cd backend
source venv/bin/activate
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt
```

## Data Sample

Sistem sudah include 10 kandidat sample setelah menjalankan seed script:
1. Ahmad Hidayat - Analis Kebijakan
2. Siti Nurhaliza - Perencana Ahli Muda
3. Budi Santoso - Analis Sistem Informasi
4. Dewi Kusuma - Analis Hukum
5. Eko Prasetyo - Analis Anggaran
6. Dan 5 kandidat lainnya...

## Next Steps

1. ✅ Explore API documentation: http://localhost:8000/docs
2. ✅ Test screening dengan sample candidates
3. ✅ Customize scoring weights di `backend/app/services/ai/scoring_engine.py`
4. ✅ Add more candidates
5. ✅ Review hasil analytics
6. ✅ Baca dokumentasi lengkap di `docs/`

## Need Help?

- 📖 Baca [README.md](README.md) untuk informasi lengkap
- 📚 Lihat [docs/API.md](docs/API.md) untuk API reference
- 🚀 Baca [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) untuk production deployment
- 🤝 Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk kontribusi

## Support

- Email: support@ai-direksi.go.id
- GitHub Issues: [Create issue](issues/)

---

**Selamat menggunakan AI-DiReksi!** 🎉
