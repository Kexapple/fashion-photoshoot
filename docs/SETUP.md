# Setup Guide

This guide provides a quick reference for setting up the Fashion Photoshoot Studio.

## Quick Links

- **Full Setup Instructions:** [INSTRUCTION.txt](INSTRUCTION.txt)
- **Architecture Overview:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Reference:** [API.md](API.md)

## Prerequisites

- Node.js 16+ (for frontend)
- Python 3.11+ (for backend)
- Firebase account
- Nano Banana API key
- Git

## 5-Minute Setup (Development)

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with Firebase and API credentials
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with Firebase credentials
npm run dev
```

Frontend runs on `http://localhost:5173`

## Environment Variables

### Backend (.env)
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-bucket.appspot.com
NANO_BANANA_API_KEY=your-api-key
NANO_BANANA_MODEL_ID=your-model-id
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)
```
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_API_KEY=your-api-key
VITE_BACKEND_URL=http://localhost:8000
```

## Database Setup

1. Create Firestore database in test mode
2. Create Storage bucket
3. Enable Google OAuth in Firebase Authentication
4. Download service account key → save as `backend/firebase-credentials.json`

## Deployment

- **Frontend:** Vercel (free tier)
- **Backend:** Railway or Render ($5-20/month)

See [INSTRUCTION.txt](INSTRUCTION.txt) for detailed deployment steps.

## Testing

```bash
# Test backend
curl http://localhost:8000/health

# View API docs
# Visit: http://localhost:8000/docs
```

## Documentation

- `ARCHITECTURE.md` - System design and data flow
- `API.md` - All API endpoints and examples
- `INSTRUCTION.txt` - Complete setup walkthrough (recommended)
- `frontend/README.md` - Frontend-specific setup
- `backend/README.md` - Backend-specific setup
