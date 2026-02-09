# 🚀 RENDER DEPLOYMENT GUIDE

Your code is ready to deploy to **Render** (free tier available).

---

## ✅ **What's Been Done**

- ✅ Code pushed to GitHub: `https://github.com/Kexapple/fashion-photoshoot`
- ✅ Frontend package.json fixed (compatible versions)
- ✅ Backend Dockerfile configured
- ✅ render.yaml created for one-click deployment
- ✅ All environment variables pre-configured

---

## 🚀 **Deploy to Render (3 Steps)**

### **Step 1: Go to Render Dashboard**
https://dashboard.render.com

### **Step 2: Create New Service**
1. Click **New +** → **Web Service**
2. Select **GitHub** → **Connect GitHub**
3. Find repo: `Kexapple/fashion-photoshoot`
4. Configure:
   - **Service Name:** `fashion-photoshoot-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Plan:** Free
5. Click **Create Web Service**

### **Step 3: Add Environment Variables**
After service is created, go to **Environment** tab and add:

```
FIREBASE_PROJECT_ID=fashion-photoshoot-studio
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
NANO_BANANA_API_KEY=demo_key
NANO_BANANA_MODEL_ID=juggernaut-x-645
PYTHONENV=production
FRONTEND_URL=https://fashion-photoshoot.vercel.app
PORT=8000
```

6. Service will auto-deploy! ✅

---

## 📝 **Alternative: Deploy Frontend + Backend at Once**

**Option A: Using render.yaml (Easiest)**

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect your **GitHub** repo
4. Select `Kexapple/fashion-photoshoot`
5. Render will auto-detect `render.yaml` and deploy both services!
6. Get live URLs immediately

**Option B: Deploy Frontend to Render Static Site**

1. Click **New +** → **Static Site**
2. GitHub: `Kexapple/fashion-photoshoot`
3. **Build Command:** `cd frontend && npm install --legacy-peer-deps && npm run build`
4. **Publish Directory:** `frontend/.svelte-kit/output/client`
5. Create and deploy!

---

## 🎯 **Expected URLs After Deployment**

| Service | URL |
|---------|-----|
| **Frontend** | `https://fashion-photoshoot.onrender.com` |
| **Backend API** | `https://fashion-photoshoot-backend.onrender.com` |
| **API Docs** | `https://fashion-photoshoot-backend.onrender.com/docs` |
| **GitHub** | https://github.com/Kexapple/fashion-photoshoot |

---

## ⚡ **Quick Commands (If Using Render CLI)**

```bash
# Install Render CLI
npm install -g @render/cli

# Deploy
render deploy --github-repo Kexapple/fashion-photoshoot

# Watch logs
render logs -f
```

---

## ✋ **Issues?**

**Backend fails to start:**
- Check **Logs** in Render dashboard
- Verify `firebase-credentials.json` path is correct
- Ensure environment variables are set

**Frontend build fails:**
- Render will show build logs
- Usually due to missing dependencies - check `npm install` output

**Need help?**
- Render Support: https://render.com/docs
- GitHub Issues: Create an issue in the repo

---

## 📊 **Current Status**

| Component | Status | URL |
|-----------|--------|-----|
| **GitHub** | ✅ LIVE | https://github.com/Kexapple/fashion-photoshoot |
| **Frontend (Vercel)** | ⏳ READY | `https://fashion-photoshoot.vercel.app` |
| **Backend (Render)** | ⏳ READY | `https://fashion-photoshoot-backend.onrender.com` |

---

**👉 Go to https://dashboard.render.com and follow the 3 steps above!**

Let me know your live URLs once deployed! 🎉
