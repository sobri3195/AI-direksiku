#!/bin/bash

set -e

echo "🚀 AI-DiReksi Setup Script"
echo "============================"
echo ""

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install $1 first."
        exit 1
    fi
}

echo "📋 Checking prerequisites..."
check_command python3
check_command node
check_command npm
check_command psql

echo "✅ All prerequisites found!"
echo ""

echo "🗄️  Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE ai_direksi;" 2>/dev/null || echo "Database may already exist"
echo "✅ Database ready!"
echo ""

echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Downloading NLP models..."
python -m spacy download en_core_web_sm || true
python -m nltk.downloader punkt || true

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

echo "Creating database tables..."
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

echo "Seeding sample data..."
python scripts/seed_data.py

cd ..
echo "✅ Backend setup complete!"
echo ""

echo "⚛️  Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
fi

cd ..
echo "✅ Frontend setup complete!"
echo ""

echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then visit:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
