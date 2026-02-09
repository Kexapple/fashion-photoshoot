# Fashion Photoshoot Studio 📸✨

A production-ready, AI-powered fashion photoshoot generation platform with Firebase authentication and credit-based system.

**Features:**
- 🔐 Firebase Authentication (Google, Email/Password)
- 📸 Multi-image upload and reference grouping
- ✨ AI-powered photoshoot generation (Nano Banana)
- 💳 Credit-based system with Pakistani payment methods
- 🎨 Modern, premium UI with Tailwind CSS
- 📱 Fully responsive design
- 🚀 Deployable on Vercel + Railway/Render

## Quick Start

### Prerequisites
- Node.js 16+
- Python 3.11+
- Firebase account
- Nano Banana API key

### Development (5 minutes)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with credentials
npm run dev
# Runs on http://localhost:5173
```

Test the app:
- Landing page: http://localhost:5173
- API docs: http://localhost:8000/docs
- Try free trial: Upload images without login

## Documentation

| Document | Purpose |
|----------|---------|
| [INSTRUCTION.txt](docs/INSTRUCTION.txt) | Complete step-by-step setup guide |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, data flow, credit system |
| [API.md](docs/API.md) | All endpoints with examples |
| [SETUP.md](docs/SETUP.md) | Quick reference setup guide |

## Project Structure

```
fashion-photoshoot/
├── frontend/                    # SvelteKit + Tailwind (deployed to Vercel)
│   ├── src/
│   │   ├── routes/             # Pages: landing, auth, dashboard, create, buy
│   │   └── lib/                # Components, stores, Firebase config
│   ├── package.json
│   └── .env.example
│
├── backend/                     # FastAPI (deployed to Railway/Render)
│   ├── app/
│   │   ├── main.py             # FastAPI app
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic (Firebase, Nano Banana, etc.)
│   │   └── models/             # Request/response schemas
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── INSTRUCTION.txt         # Complete setup guide
│   ├── ARCHITECTURE.md        # System design
│   ├── API.md                 # API reference
│   └── SETUP.md               # Quick setup
│
└── README.md                   # This file
```

## Key Features Explained

### Free Trial (3 images per IP)
- Anonymous users get 3 free generations per IP address
- One-time limit, lifetime duration
- Creates freemium user acquisition

### First Login Bonus (5 credits)
- Every new user gets 5 free credits automatically
- Credits = image generation power
- Only granted once per account

### Credit System
- 1 generation = 1 credit
- Atomic, server-side enforced
- No frontend manipulation possible
- Prevents race conditions with Firestore transactions

### Pakistani Payment Methods
- JazzCash & EasyPaisa integration
- Backend-verified payments
- Credits only added after verification

## Technology Stack

**Frontend:**
- SvelteKit (lightweight, fast)
- Tailwind CSS (modern styling)
- Firebase SDK (auth, real-time)
- Vite (fast build tool)

**Backend:**
- FastAPI (async, auto-docs)
- Firebase Admin SDK (token validation, database)
- Python 3.11+ (modern syntax)

**Infrastructure:**
- Vercel (frontend CDN, free tier)
- Railway/Render (backend servers, $5-20/mo)
- Firebase (auth, database, storage, free tier)
- Nano Banana (AI image generation, pay-per-use)

## Security

✅ Firebase token validation on every request
✅ Server-side credit enforcement (never trust frontend)
✅ Atomic transactions for credit deduction
✅ Payment verification before credit addition
✅ IP hashing for anonymous user privacy
✅ CORS whitelisting
✅ Rate limiting per user

## Cost Estimate (100 users)

| Service | Cost |
|---------|------|
| Firebase | $0-10 |
| Vercel | $0 (free tier) |
| Railway | $5-20 |
| AI API | $10-50 |
| **Total** | **$15-80/month** |

## Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Connect repo to Vercel
3. Set env variables
4. Auto-deploys on push

### Backend (Railway)
1. Push code to GitHub
2. Create project on Railway
3. Set env variables
4. Deploy from Git

See [INSTRUCTION.txt](docs/INSTRUCTION.txt) for detailed deployment walkthrough.

## API Examples

**Anonymous generation:**
```bash
curl -X POST http://localhost:8000/api/photoshoots/create \
  -H "Content-Type: application/json" \
  -d '{
    "articleType": "shirt",
    "imageSize": "medium",
    "uploadedImageUrls": ["url1", "url2"],
    "clientIp": "192.168.1.1"
  }'
```

**Authenticated generation with credit check:**
```bash
# Check credits first
curl "http://localhost:8000/api/user/credits?id_token=eyJ..."

# Generate with token
curl -X POST http://localhost:8000/api/photoshoots/create \
  -H "Content-Type: application/json" \
  -d '{
    "idToken": "eyJ...",
    "articleType": "dress",
    "imageSize": "large",
    "uploadedImageUrls": ["url1", "url2"]
  }'
```

See [API.md](docs/API.md) for complete reference.

## Testing

**Test free trial:**
1. Open http://localhost:5173
2. Click "Try Free (3 Images)"
3. Upload images → Generate
4. Can generate 3 times

**Test authenticated flow:**
1. Click "Login / Sign up"
2. Create account with email
3. Automatically get 5 credits
4. Generate photoshoots (costs 1 credit each)

**Test API directly:**
```bash
# Health check
curl http://localhost:8000/health

# View Swagger UI
open http://localhost:8000/docs
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Firebase credentials error | Ensure `backend/firebase-credentials.json` exists |
| CORS errors | Update `ALLOWED_ORIGINS` in `backend/app/config.py` |
| Storage permission denied | Apply security rules in Firebase Console |
| Build fails on Vercel | Check `VITE_*` env vars are set in Vercel dashboard |

For detailed troubleshooting, see [INSTRUCTION.txt](docs/INSTRUCTION.txt).

## Roadmap

- ✅ Anonymous free trial (3 images)
- ✅ User authentication & first login bonus
- ✅ Credit-based system
- ✅ Image generation
- ⏳ Mobile app (Flutter)
- ⏳ Subscription plans
- ⏳ Advanced styling options
- ⏳ Image editing tools
- ⏳ Team/collaboration features

## License

MIT License - See LICENSE file for details

## Support

- 📚 Full documentation: [docs/INSTRUCTION.txt](docs/INSTRUCTION.txt)
- 🐛 Found a bug? Open an issue
- 💬 Questions? Check the docs first

---

**Built with ❤️ for fashion creators**

Start with [INSTRUCTION.txt](docs/INSTRUCTION.txt) for complete setup guide.
