# Fashion Photoshoot Studio - Backend API

## Quick Start

### Prerequisites
- Python 3.11+
- Firebase project with service account
- Nano Banana API key
- JazzCash/EasyPaisa merchant accounts (optional for testing)

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

Server will be available at `http://localhost:8000`

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API docs (Swagger UI)

## Deployment

### Railway

1. Install Railway CLI
2. Connect to your Railway project:
   ```bash
   railway link
   ```
3. Set environment variables:
   ```bash
   railway variables set FIREBASE_PROJECT_ID=...
   railway variables set NANO_BANANA_API_KEY=...
   ```
4. Deploy:
   ```bash
   railway deploy
   ```

### Render

1. Connect GitHub repository
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn -w 4 -b 0.0.0.0:8000 app.main:app`
5. Add environment variables in dashboard
6. Deploy

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Configuration and settings
│   ├── routes/           # API endpoints
│   │   ├── auth.py       # Authentication routes
│   │   ├── generate.py   # Image generation routes
│   │   └── credits.py    # Credit management routes
│   ├── services/         # Business logic
│   │   ├── auth.py       # Firebase auth helpers
│   │   ├── firestore.py  # Database operations
│   │   ├── nano_banana.py # Image generation API
│   │   ├── storage.py    # File storage operations
│   │   └── payment.py    # Payment gateway integration
│   └── models/           # Pydantic models
│       ├── request.py    # Request schemas
│       └── response.py   # Response schemas
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
└── .env.example          # Environment template
```

## API Endpoints

See [API.md](../docs/API.md) for detailed endpoint documentation

## Environment Variables

See [INSTRUCTION.txt](../docs/INSTRUCTION.txt) for detailed setup guide
