# Deployment Guide - Fashion Photoshoot Studio

## Step 1: Install Required Tools (5 minutes)

### A. Install Git
```powershell
# Option 1: Using Chocolatey (if installed)
choco install git

# Option 2: Download from https://git-scm.com/download/win
# Run installer and use default settings
```

### B. Install Node.js (if not already installed)
```powershell
# Verify Node is installed
node --version
npm --version

# If not installed, download from https://nodejs.org (LTS version)
```

### C. Install Vercel CLI
```powershell
npm install -g vercel
```

---

## Step 2: Initialize Git Repository (2 minutes)

```powershell
cd c:\Space\python\fashion-photoshoot

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Fashion Photoshoot Studio"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/fashion-photoshoot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy Backend to Railway (5 minutes)

```powershell
# 1. Go to https://railway.app
# 2. Sign in with GitHub
# 3. Create new project
# 4. Select "Deploy from GitHub repo"
# 5. Select your fashion-photoshoot repo
# 6. Set these variables in Railway dashboard:

# Environment Variables to add:
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-email@appspot.gserviceaccount.com
FIREBASE_STORAGE_BUCKET=your-bucket.appspot.com
NANO_BANANA_API_KEY=your-api-key
NANO_BANANA_MODEL_ID=your-model-id
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

Copy the Railway URL when deployment succeeds.

---

## Step 4: Deploy Frontend to Vercel (3 minutes)

### Option A: Via Vercel CLI (Automated)

```powershell
cd c:\Space\python\fashion-photoshoot\frontend

# Login to Vercel
vercel login

# Deploy
vercel deploy --prod

# When prompted:
# - Link to existing project? "No"
# - Project name? "fashion-photoshoot"
# - Which directory? "./"
# - Override settings? "Yes"

# After deployment completes, set environment variables:
vercel env add VITE_FIREBASE_API_KEY
vercel env add VITE_FIREBASE_PROJECT_ID
vercel env add VITE_FIREBASE_STORAGE_BUCKET
vercel env add VITE_FIREBASE_MESSAGING_SENDER_ID
vercel env add VITE_FIREBASE_APP_ID
vercel env add VITE_BACKEND_URL (← use Railway URL)

# Redeploy with new env vars
vercel deploy --prod
```

### Option B: Via Vercel Web Dashboard (Simpler)

```
1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Select root directory: "frontend"
5. Set these environment variables:
   - VITE_FIREBASE_API_KEY
   - VITE_FIREBASE_PROJECT_ID
   - VITE_FIREBASE_STORAGE_BUCKET
   - VITE_FIREBASE_MESSAGING_SENDER_ID
   - VITE_FIREBASE_APP_ID
   - VITE_BACKEND_URL (add your Railway URL)
6. Click "Deploy"
```

---

## Step 5: Update Backend FRONTEND_URL

Once you have your Vercel URL:

```powershell
# Go to Railway dashboard
# Update FRONTEND_URL to your new Vercel URL
# Redeploy backend
```

---

## Quick Command Reference

### Push code to GitHub
```powershell
cd c:\Space\python\fashion-photoshoot
git add .
git commit -m "Your message"
git push
```

### Check deployment status
```powershell
# Railway
https://railway.app/dashboard

# Vercel
https://vercel.com/dashboard
```

---

## Firebase Credentials You'll Need

From Firebase Console, gather:
```
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL = "your-service-account@appspot.gserviceaccount.com"
FIREBASE_STORAGE_BUCKET = "your-project.appspot.com"
```

---

## Final Checklist

- [ ] Git installed
- [ ] Git repository initialized locally
- [ ] Code pushed to GitHub
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set in both services
- [ ] Firebase security rules configured
- [ ] Test app at your Vercel URL

---

## Test Your Deployment

```
1. Visit: https://your-vercel-app.com
2. Click "Try Free (3 Images)"
3. Upload images and generate
4. If successful, try logging in
5. Check backend logs for any errors
```

---

## Troubleshooting

### "Module not found" on Vercel
- Check package.json includes all dependencies
- Verify root directory is set to "frontend"

### "Firebase credentials error" on Railway
- Verify environment variables are correctly set
- Check FIREBASE_PRIVATE_KEY format (includes newlines)

### "CORS error" in browser
- Update ALLOWED_ORIGINS in backend config.py
- Add your Vercel domain

### Images not loading
- Check Firebase Storage security rules
- Verify bucket is public (or adjust rules)

---

That's it! Your app will auto-deploy on every push to GitHub 🚀
