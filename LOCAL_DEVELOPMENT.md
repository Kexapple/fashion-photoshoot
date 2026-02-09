# 💻 Local Development & Testing Guide

This guide helps you test the application locally before deploying to production.

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- Git installed
- Firebase project created
- Internet connection (for Firebase)

## Quick Start: Local Development

### 1️⃣ Install Dependencies

**Frontend:**
```powershell
cd frontend
npm install
```

**Backend:**
```powershell
cd backend
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

**Copy example files:**
```powershell
copy frontend\.env.example frontend\.env
copy backend\.env.example backend\.env
```

**Edit `frontend/.env`:**
```
VITE_FIREBASE_API_KEY=your_key_here
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_BACKEND_URL=http://localhost:8000
```

**Edit `backend/.env`:**
```
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
# Or use individual FIREBASE_* env vars

NANO_BANANA_API_KEY=your_key  # Optional - uses mock if not set
NANO_BANANA_MODEL_ID=model_id

PYTHONENV=development
FRONTEND_URL=http://localhost:5173
```

### 3️⃣ Start Backend Server

**Terminal 1:**
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

**Test backend health:**
```powershell
# In another terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**View API docs:**
Visit http://localhost:8000/docs in your browser

### 4️⃣ Start Frontend Dev Server

**Terminal 2:**
```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v4.x.x  build 0.00s

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Visit http://localhost:5173 in your browser

## Testing Flows

### Test 1: Anonymous Free Trial (No Login)

1. **Open** http://localhost:5173
2. **Click** "Try Free" button
3. **Upload** an image (any JPG/PNG, < 5MB)
4. **Select** article type (e.g., "Shirt")
5. **Click** "Continue"
6. **Optional:** Add style notes
7. **Select** image size
8. **Review** and click "Generate"
9. **Wait** ~30-40 seconds for image generation
10. **Verify:**
    - Backend receives request: Check terminal for logs
    - Image loads in gallery (or placeholder if mock service)
    - "Create Another" button appears

**Expected Behavior:**
- First 3 generations are free (per IP)
- 4th attempt shows "Trial limit reached"
- Can still see previous generations

### Test 2: User Registration & First Login Bonus

1. **Click** "Sign Up" button
2. **Fill form:**
   - Name: "Test User"
   - Email: "test@example.com"
   - Password: "password123"
3. **Click** "Create Account"
4. **Verify:**
   - Redirected to dashboard
   - Credit balance shows **5 credits** (first-login bonus)
   - Firestore shows new user in `users/{uid}` collection

### Test 3: Generate with Credits (Authenticated)

1. **From dashboard,** click "Create New Photoshoot"
2. **Upload** an image
3. **Fill** all form fields
4. **Click** "Generate"
5. **Verify:**
   - Backend receives auth token in request
   - Credit balance decreases by 1
   - Image generates (or shows placeholder)
   - Transaction logged in Firestore `transactions/{tx_id}`

### Test 4: Buy Credits

1. **From dashboard,** click "Buy Credits"
2. **Select** a package (e.g., 10 credits)
3. **Choose** payment method (JazzCash or EasyPaisa)
4. **Enter** phone number
5. **Click** "Proceed to Payment"
6. **Verify:**
   - Request sent to backend (/credits/purchase)
   - In production: Payment gateway validation
   - In test: Mock payment accepted
   - Credits immediately added to balance
   - Transaction logged with payment method

### Test 5: Authentication Persistence

1. **Logout** from dashboard
2. **Close** browser tab
3. **Reopen** http://localhost:5173
4. **Verify:**
   - Automatically logged back in (Firebase persistence)
   - Dashboard shows same balance

## Debugging Tips

### Backend Issues

**Check logs in terminal:**
```
INFO:     Application startup complete [uvicorn]
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started server process [1234]
```

**Test specific endpoint:**
```powershell
# Health check
curl http://localhost:8000/health

# With authentication (get token from browser first)
$token = "firebase_id_token_here"
curl -H "Authorization: Bearer $token" `
     http://localhost:8000/user/credits
```

**View FastAPI docs:**
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Issues

**Check browser console:**
- Press F12 to open Developer Tools
- Go to "Console" tab
- Look for errors (red text)

**Common issues:**
- "Cannot reach backend" → Check `VITE_BACKEND_URL` in frontend/.env
- "Firebase error" → Check Firebase credentials in frontend/.env
- "404 on image upload" → Ensure backend is running

**HMR (Hot Module Reload):**
- Frontend auto-refreshes when you edit files
- Check "Network" tab if hot reload fails

### Firebase Issues

**Verify connection:**
```powershell
# In browser console, paste:
firebase.auth().currentUser
# Should show user object if logged in, null if not
```

**Check Firestore data:**
1. Go to Firebase Console
2. Select your project
3. Navigate to Firestore Database
4. Look for collections: `users`, `anonUsers`, `transactions`, `photoshoots`

**Common errors:**
- "Permission denied" → Check Firestore security rules
- "Auth error" → Verify Firebase credentials match
- "Storage error" → Check Storage bucket exists

## Mock Services

When API keys are not configured, the app uses mocks:

### Nano Banana Mock
- Returns placeholder image URLs
- Useful for testing without API key
- Add real API key to `backend/.env` to use real service

### Payment Methods Mock
- Accepts any phone number
- Always returns success
- Real validation added by setting merchant credentials

## Database Inspection

### With Firebase Console
1. Go to https://console.firebase.google.com
2. Select your project
3. Navigate to Firestore Database
4. Browse collections in real-time

### With Backend Logs
```powershell
# Add this to backend code for detailed logging:
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"User data: {user_data}")
```

## Performance Testing

### Load Testing (Optional)
```powershell
# Install hey tool: https://github.com/rakyll/hey
hey -n 100 -c 10 http://localhost:8000/health
```

### Memory Usage
```powershell
# Python memory
Get-Process python | Select-Object ProcessName, WorkingSet

# Node.js memory  
Get-Process node | Select-Object ProcessName, WorkingSet
```

## Stopping Services

**Stop Backend:**
```
Press CTRL+C in backend terminal
```

**Stop Frontend:**
```
Press CTRL+C in frontend terminal
```

## Deployment Readiness Checklist

Before deploying to production:

- [ ] All tests pass locally
- [ ] Nano Banana API key configured (if using real images)
- [ ] Firebase security rules configured (see docs/INSTRUCTION.txt Part 7)
- [ ] Environment variables validated (run `.\validate-env.ps1`)
- [ ] No database errors in logs
- [ ] Anonymous free trial working correctly
- [ ] Paid credits system tested
- [ ] Google OAuth tested
- [ ] Email signup tested
- [ ] Payment flow stub tested

## Next Steps

Once tested locally:
1. Run `.\deploy-setup.ps1` to prepare for deployment
2. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for production deployment
3. Deploy backend to Railway
4. Deploy frontend to Vercel
5. Update environment variables in production
6. Run same tests against production URLs

## Troubleshooting Resources

- **Backend errors:** Check `docs/API.md` for endpoint specs
- **Firebase issues:** See `docs/INSTRUCTION.txt` Part 1
- **Nano Banana setup:** See `docs/INSTRUCTION.txt` Part 2
- **Complete setup guide:** See `docs/INSTRUCTION.txt` (all parts)
- **Architecture details:** See `docs/ARCHITECTURE.md`

## Quick Reference: Port Mappings

| Service | URL | Port |
|---------|-----|------|
| Frontend Dev | http://localhost:5173 | 5173 |
| Backend API | http://localhost:8000 | 8000 |
| FastAPI Docs | http://localhost:8000/docs | 8000 |
| Firebase | N/A (cloud) | N/A |

## Getting Help

If something isn't working:

1. **Check the logs** - First place to look
2. **Validate environment variables** - Run `.\validate-env.ps1`
3. **Check Firebase Console** - Verify project setup
4. **Review docs** - INSTRUCTION.txt has detailed troubleshooting
5. **Check example files** - Reference .env.example for correct format

---

**Last Updated:** 2024
**Ready for Development:** Yes ✅
