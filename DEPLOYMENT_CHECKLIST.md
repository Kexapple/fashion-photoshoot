# 🎯 Fashion Photoshoot Studio - Deployment Checklist

## Prerequisites (Install First)
- [ ] **Git for Windows** - https://git-scm.com/download/win
- [ ] **Node.js** - https://nodejs.org (if not already installed)
- [ ] **Vercel Account** - https://vercel.com (sign up with GitHub)
- [ ] **Railway Account** - https://railway.app (for backend deployment)
- [ ] **GitHub Account** - https://github.com

## Services Setup
### Firebase Configuration
- [ ] Create Firebase project at https://console.firebase.google.com
- [ ] Enable Google Authentication
- [ ] Enable Email/Password Authentication
- [ ] Create Firestore Database (test mode for now)
- [ ] Create Storage bucket
- [ ] Download service account JSON key
- [ ] Save key as `backend/firebase-credentials.json` OR add env vars to backend/.env

### Nano Banana API (Image Generation)
- [ ] Sign up at https://www.nanobana.com
- [ ] Get API key
- [ ] Select a Stable Diffusion model
- [ ] Add `NANO_BANANA_API_KEY` to backend/.env
- [ ] Add `NANO_BANANA_MODEL_ID` to backend/.env

### Payment Methods (Optional for Testing)
- [ ] JazzCash merchant account (contact JazzCash support)
- [ ] EasyPaisa merchant account (contact EasyPaisa support)
- [ ] Add merchant IDs/API keys to backend/.env

## Code Preparation
- [ ] Run `.\deploy-setup.ps1` from project root
- [ ] Update `frontend/.env` with Firebase config:
  ```
  VITE_FIREBASE_API_KEY=...
  VITE_FIREBASE_AUTH_DOMAIN=...
  VITE_FIREBASE_PROJECT_ID=...
  VITE_FIREBASE_STORAGE_BUCKET=...
  VITE_FIREBASE_MESSAGING_SENDER_ID=...
  VITE_FIREBASE_APP_ID=...
  VITE_BACKEND_URL=http://localhost:8000  # Update after backend deployed
  ```

- [ ] Update `backend/.env` with:
  ```
  FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
  # OR individual env vars:
  FIREBASE_PROJECT_ID=...
  FIREBASE_PRIVATE_KEY_ID=...
  # etc (see backend/.env.example)
  
  NANO_BANANA_API_KEY=...
  NANO_BANANA_MODEL_ID=...
  NANO_BANANA_TIMEOUT=180
  
  PYTHONENV=production
  ```

## Deployment Sequence
### Step 1: Push to GitHub
- [ ] `git branch -M main`
- [ ] `git push -u origin main`

### Step 2: Deploy Backend to Railway
- [ ] Log in to https://railway.app
- [ ] Create new project → Import from GitHub
- [ ] Select your `fashion-photoshoot` repository
- [ ] Add environment variables:
  - Firebase credentials
  - Nano Banana API key
  - CORS settings if needed
- [ ] Deploy (auto-builds with Dockerfile)
- [ ] Note the Railway deployment URL (e.g., project-xxx.railway.app)

### Step 3: Deploy Frontend to Vercel
- [ ] Log in to https://vercel.com
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Add environment variables:
  ```
  VITE_FIREBASE_API_KEY
  VITE_FIREBASE_AUTH_DOMAIN
  VITE_FIREBASE_PROJECT_ID
  VITE_FIREBASE_STORAGE_BUCKET
  VITE_FIREBASE_MESSAGING_SENDER_ID
  VITE_FIREBASE_APP_ID
  VITE_BACKEND_URL=https://your-railway-backend.railway.app
  ```
- [ ] Deploy
- [ ] Note the Vercel URL (e.g., fashion-photoshoot.vercel.app)

### Step 4: Update Backend with Frontend URL
- [ ] Go to Railway dashboard
- [ ] Update `FRONTEND_URL` env variable
- [ ] Redeploy backend

## Testing
- [ ] Visit your Vercel frontend URL
- [ ] Click "Try Free" button
- [ ] Upload an image (should work with mock service if Nano Banana not configured)
- [ ] Sign up with email
- [ ] Check that 5 credits were granted
- [ ] Try to generate (should make backend API call)

## Post-Deployment
- [ ] Set up Firestore security rules (see docs/INSTRUCTION.txt Part 7)
- [ ] Set up Storage security rules
- [ ] Configure payment gateway credentials in Railway
- [ ] Switch Firebase from test to production mode
- [ ] Set up custom domain (optional)
- [ ] Monitor logs: Railway dashboard + Vercel logs
- [ ] Set up error tracking (optional)

## Environment Variables Reference

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_BACKEND_URL=http://localhost:8000
```

### Backend (.env)
```
# Firebase (option 1: path to JSON)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Firebase (option 2: individual vars)
FIREBASE_PROJECT_ID=...
FIREBASE_PRIVATE_KEY_ID=...
FIREBASE_PRIVATE_KEY=...
FIREBASE_CLIENT_EMAIL=...
FIREBASE_CLIENT_ID=...
FIREBASE_AUTH_URI=...
FIREBASE_TOKEN_URI=...

# Nano Banana
NANO_BANANA_API_KEY=your_key
NANO_BANANA_MODEL_ID=your_model_id
NANO_BANANA_TIMEOUT=180

# Payment (optional)
JAZZCASH_MERCHANT_ID=...
JAZZCASH_API_KEY=...
EASYPAISA_MERCHANT_ID=...
EASYPAISA_API_KEY=...

# App
PYTHONENV=production
FRONTEND_URL=https://your-vercel-url.vercel.app
```

## Troubleshooting Commands

```powershell
# Check Git status
git status

# View git remotes
git remote -v

# Install npm packages
npm install

# Test frontend locally
cd frontend
npm run dev

# Test backend locally
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Check environment variables
Get-Item env:VITE_*
```

## Common Issues & Solutions

**Issue:** Vercel deployment fails with "frontend directory not found"
**Solution:** Make sure "root directory" is set to `frontend` in Vercel settings, not `.`

**Issue:** Backend deployment fails with "Firebase credentials error"
**Solution:** Verify `FIREBASE_PROJECT_ID` and other env vars match your Firebase project

**Issue:** Frontend shows "Cannot reach backend"
**Solution:** Check `VITE_BACKEND_URL` in frontend env vars matches your Railway deployment URL

**Issue:** Image generation returns error
**Solution:** Verify `NANO_BANANA_API_KEY` is set correctly, or use mock service for testing

## Support Documentation
- 📖 Main guide: `DEPLOYMENT_STEPS.md`
- 📚 Architecture: `docs/ARCHITECTURE.md`
- 🔌 API reference: `docs/API.md`
- 🛠️ Setup guide: `docs/INSTRUCTION.txt`
- 🚀 Quick setup: `docs/SETUP.md`

---
**Last Updated:** $(date)
**Status:** Ready for deployment
