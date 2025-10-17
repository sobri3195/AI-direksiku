# Contributing to AI-DiReksi

Terima kasih atas minat Anda untuk berkontribusi pada AI-DiReksi! Dokumen ini berisi panduan untuk berkontribusi pada proyek.

## Code of Conduct

Dengan berpartisipasi dalam proyek ini, Anda diharapkan menjunjung kode etik kami. Perlakukan semua kontributor dengan rasa hormat dan profesional.

## Cara Berkontribusi

### Melaporkan Bug

Jika Anda menemukan bug, silakan buat issue baru dengan:
- Deskripsi jelas tentang masalah
- Langkah-langkah untuk mereproduksi bug
- Perilaku yang diharapkan vs perilaku aktual
- Screenshot jika relevan
- Environment details (OS, browser, versi aplikasi)

### Mengajukan Fitur Baru

Untuk mengusulkan fitur baru:
1. Cek apakah fitur sudah diusulkan di issues
2. Buat issue baru dengan label "enhancement"
3. Jelaskan use case dan manfaat fitur
4. Diskusikan dengan maintainer sebelum mulai coding

### Pull Request Process

1. **Fork Repository**
   ```bash
   git clone https://github.com/your-username/ai-direksi.git
   cd ai-direksi
   ```

2. **Buat Branch Baru**
   ```bash
   git checkout -b feature/nama-fitur
   # atau
   git checkout -b fix/nama-bug
   ```

3. **Lakukan Perubahan**
   - Ikuti coding standards yang ada
   - Tulis tests untuk kode baru
   - Update dokumentasi jika diperlukan
   - Commit dengan pesan yang jelas

4. **Testing**
   ```bash
   # Backend tests
   cd backend
   pytest tests/ -v
   
   # Frontend tests
   cd frontend
   npm test
   ```

5. **Push dan Buat PR**
   ```bash
   git push origin feature/nama-fitur
   ```
   Kemudian buat Pull Request di GitHub

### Coding Standards

#### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings for functions and classes

Example:
```python
def calculate_score(sentiment_data: Dict, footprints: List[Dict]) -> float:
    """
    Calculate overall score based on sentiment and digital footprints.
    
    Args:
        sentiment_data: Dictionary containing sentiment analysis results
        footprints: List of digital footprint data
        
    Returns:
        Overall score as float between 0-100
    """
    # Implementation
    pass
```

#### JavaScript/React (Frontend)

- Use ES6+ syntax
- Use functional components with hooks
- Use meaningful component and variable names
- Add PropTypes or TypeScript types
- Follow Airbnb JavaScript Style Guide

Example:
```javascript
const CandidateCard = ({ candidate, onSelect }) => {
  const [loading, setLoading] = useState(false);
  
  const handleClick = async () => {
    setLoading(true);
    await onSelect(candidate.id);
    setLoading(false);
  };
  
  return (
    <Card>
      {/* Component content */}
    </Card>
  );
};
```

### Commit Message Guidelines

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(screening): add support for Instagram scraping

Add Instagram profile scraping capability to digital footprint
analysis service.

Closes #123

---

fix(api): correct sentiment score calculation

The sentiment score was being calculated incorrectly for neutral
content. Updated the formula to properly weight neutral sentiments.

Fixes #456
```

### Testing Requirements

- All new features must include tests
- Maintain or improve code coverage
- Tests must pass before PR is merged
- Include both unit and integration tests where applicable

### Documentation

- Update README.md if you change setup process
- Update API.md for API changes
- Add inline comments for complex logic
- Update CHANGELOG.md

### Review Process

1. Maintainer akan review PR Anda
2. Diskusi dan perubahan mungkin diminta
3. Setelah approved, PR akan di-merge
4. Branch akan dihapus setelah merge

## Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/ai-direksi.git
cd ai-direksi

# Run setup script
./setup.sh

# Start development servers
# Terminal 1
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm start
```

## Project Structure

```
ai-direksi/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── tests/           # Backend tests
│   └── scripts/         # Utility scripts
├── frontend/            # React frontend
│   ├── public/
│   └── src/
│       ├── components/  # React components
│       ├── pages/       # Page components
│       └── services/    # API services
├── docs/               # Documentation
└── tests/              # Integration tests
```

## Getting Help

- Check existing issues and documentation
- Ask questions in Discussions
- Contact maintainers: support@ai-direksi.go.id

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors akan dicantumkan dalam:
- README.md contributors section
- Release notes
- CHANGELOG.md

Terima kasih atas kontribusi Anda! 🙏
