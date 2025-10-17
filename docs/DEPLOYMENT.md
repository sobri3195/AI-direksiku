# Deployment Guide - AI-DiReksi

## Prerequisites

- Docker & Docker Compose
- PostgreSQL 14+
- Python 3.11+
- Node.js 18+

## Environment Setup

### 1. Backend Configuration

Create `.env` file in the `backend` directory:

```bash
cp backend/.env.example backend/.env
```

Update the following critical values:
```env
SECRET_KEY=your-secure-random-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/ai_direksi
ENCRYPTION_KEY=your-encryption-key
```

### 2. Frontend Configuration

Create `.env` file in the `frontend` directory:

```bash
echo "REACT_APP_API_URL=http://localhost:8000" > frontend/.env
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Option 2: Manual Deployment

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm

# Run migrations (if using Alembic)
# alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

#### Database

```bash
# Create database
createdb ai_direksi

# Or using psql
psql -U postgres
CREATE DATABASE ai_direksi;
\q
```

## Production Deployment

### 1. Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and ENCRYPTION_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set DEBUG=False
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Configure firewall rules

### 2. Backend Production Setup

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 3. Frontend Production Build

```bash
cd frontend
npm run build

# Serve with nginx or any static file server
# Copy build/ contents to your web server
```

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/ai-direksi/frontend/build;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
}
```

### 5. Systemd Service (Linux)

Create `/etc/systemd/system/ai-direksi.service`:

```ini
[Unit]
Description=AI-DiReksi Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-direksi/backend
Environment="PATH=/var/www/ai-direksi/backend/venv/bin"
ExecStart=/var/www/ai-direksi/backend/venv/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-direksi
sudo systemctl start ai-direksi
sudo systemctl status ai-direksi
```

## Database Migrations

If using Alembic:

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Systemd logs
sudo journalctl -u ai-direksi -f
```

## Backup Strategy

### Database Backup

```bash
# Backup
pg_dump -U postgres ai_direksi > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres ai_direksi < backup_20240116.sql
```

### Automated Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/backup/ai-direksi"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres ai_direksi | gzip > $BACKUP_DIR/db_$DATE.sql.gz
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
```

## Scaling

### Horizontal Scaling

- Use load balancer (nginx, HAProxy)
- Deploy multiple backend instances
- Use Redis for session management and caching
- Consider PostgreSQL read replicas

### Vertical Scaling

- Increase worker processes
- Allocate more CPU/RAM
- Optimize database queries
- Add database indexes

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Verify connection string
   psql -U postgres -d ai_direksi
   ```

2. **CORS Errors**
   - Check BACKEND_CORS_ORIGINS in .env
   - Verify frontend URL is whitelisted

3. **Module Not Found**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Port Already in Use**
   ```bash
   # Find and kill process
   lsof -i :8000
   kill -9 <PID>
   ```

## Performance Optimization

- Enable database query caching
- Use Redis for caching
- Implement CDN for static assets
- Enable gzip compression
- Use connection pooling
- Optimize database indexes

## Security Best Practices

1. Keep all dependencies updated
2. Use environment variables for secrets
3. Implement rate limiting
4. Enable SQL injection prevention
5. Use HTTPS everywhere
6. Regular security audits
7. Implement input validation
8. Use parameterized queries
9. Enable CSRF protection
10. Regular backups

## Support

For deployment issues:
- Email: support@ai-direksi.go.id
- Documentation: https://docs.ai-direksi.go.id
- Issue Tracker: GitHub Issues
