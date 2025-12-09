# Lumen - Artistic Photography Platform

A comprehensive artistic photography platform featuring photo management, series organization, and subscription-based monetization.

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Node.js (for frontend development)

### Installation

1. **Clone and setup backend**:
   ```bash
   cd lumen
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Setup database**:
   ```bash
   cd backend
   alembic upgrade head
   ```

4. **Run development server**:
   ```bash
   python3 main.py
   ```

## Architecture

### Core Components

1. **Backend API**: FastAPI-based REST service
   - Photo and series management
   - User authentication via Firebase
   - Search and filtering capabilities
   - Subscription management with Stripe

2. **Frontend Interface**: Modern web UI
   - Glass morphism design system
   - Poor Man's Modules architecture
   - Responsive photo gallery
   - User dashboard and management

3. **Image Processing**: Advanced image manipulation
   - Upload and processing pipeline
   - Metadata extraction and management
   - Storage optimization

4. **Database Layer**: PostgreSQL with SQLAlchemy ORM
   - Photo and series metadata
   - User profiles and preferences
   - Subscription and billing data

## Project Structure

```
lumen/
├── backend/           # FastAPI backend service
│   ├── app/          # Main application code
│   ├── models/       # Database models
│   ├── api/          # API endpoints
│   └── tests/        # Backend tests
├── frontend/         # Web interface
│   ├── static/       # CSS, JS, images
│   ├── templates/    # HTML templates
│   └── components/   # UI components
├── docs/             # Project documentation
├── scripts/          # Utility scripts
└── storage/          # Image processing and storage
```

## Key Features

- **Photo Management**: Upload, organize, and manage artistic photography
- **Series Organization**: Group photos into curated collections and series
- **Advanced Search**: Filter and discover photos by metadata, tags, and collections
- **User Authentication**: Secure login via Firebase authentication
- **Subscription Model**: Stripe-integrated subscription tiers for premium features
- **Responsive Design**: Glass morphism UI that works across all devices

## API Endpoints

### Photos
- `GET /api/v1/photos/` - List photos with pagination and filtering
- `POST /api/v1/photos/` - Upload new photos
- `GET /api/v1/photos/{id}` - Get photo details
- `PUT /api/v1/photos/{id}` - Update photo metadata
- `DELETE /api/v1/photos/{id}` - Delete photos

### Series
- `GET /api/v1/series/` - List photo series
- `POST /api/v1/series/` - Create new series
- `GET /api/v1/series/{id}` - Get series details
- `PUT /api/v1/series/{id}` - Update series
- `DELETE /api/v1/series/{id}` - Delete series

### Users
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/logout` - User logout

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend validation (manual)
# Open frontend/ in browser and test functionality
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/lumen

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Storage
STORAGE_PATH=/path/to/storage
UPLOAD_MAX_SIZE=10485760  # 10MB
```

## Deployment

### Production Setup

1. **Backend**: Deploy with Gunicorn or similar WSGI server
2. **Frontend**: Serve static files via nginx or CDN
3. **Database**: PostgreSQL with proper backup strategy
4. **Storage**: Configurable local or cloud storage

### Docker Support

```bash
# Build and run with Docker
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: See `docs/` directory
- **Issues**: Report in the project repository
- **Questions**: Use project issue tracker

---

*Lumen - Artistic Photography Platform. Built with FastAPI, modern web technologies, and a focus on user experience.*