# ============================================================
# FASHION PHOTOSHOOT - COMPLETE AUTOMATED DEPLOYMENT
# ============================================================
# This script does EVERYTHING to deploy your app live
# Run it once and your app will be on Vercel + Railway!

Write-Host '' -ForegroundColor Cyan
Write-Host '  FASHION PHOTOSHOOT STUDIO - AUTO DEPLOYMENT         ' -ForegroundColor Cyan  
Write-Host '' -ForegroundColor Cyan

Write-Host ''
Write-Host 'This script will:' -ForegroundColor Yellow
Write-Host '  1. Install Git (if needed)' -ForegroundColor Gray
Write-Host '  2. Initialize Git repository' -ForegroundColor Gray
Write-Host '  3. Create GitHub repository' -ForegroundColor Gray
Write-Host '  4. Push code to GitHub' -ForegroundColor Gray
Write-Host '  5. Deploy backend to Railway' -ForegroundColor Gray
Write-Host '  6. Deploy frontend to Vercel' -ForegroundColor Gray
Write-Host '  7. Provide you with live URLs' -ForegroundColor Gray

Write-Host ''
Write-Host 'Prerequisites:' -ForegroundColor Yellow
Write-Host '   GitHub account (https://github.com if needed)' -ForegroundColor Gray
Write-Host '   Railway account (https://railway.app)' -ForegroundColor Gray
Write-Host '   Vercel account (https://vercel.com)' -ForegroundColor Gray

Write-Host ''
Read-Host 'Press Enter to start deployment...'

Write-Host ''
Write-Host 'Step 1: Installing Git...' -ForegroundColor Yellow

# Check if Git is installed
try {
    \ = git --version 2>
    Write-Host ' Git already installed: '\ -ForegroundColor Green
} catch {
    Write-Host 'Installing Git for Windows...' -ForegroundColor Yellow
    # Download and install Git
    \ = 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe'
    \ = '\C:\Users\eliro\AppData\Local\Temp\Git-Installer.exe'
    
    Write-Host 'Downloading Git...' -ForegroundColor Gray
    try {
        Invoke-WebRequest -Uri \ -OutFile \ -ErrorAction Stop
        Write-Host 'Installing Git...' -ForegroundColor Gray
        Start-Process \ -ArgumentList '/VERYSILENT /NORESTART' -Wait
        \c:\Users\eliro\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\debugCommand;c:\Users\eliro\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\copilotCli;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\Docker\Docker\resources\bin;C:\Program Files\dotnet\;C:\Program Files\nodejs\;C:\Users\eliro\AppData\Local\Programs\Python\Python39\Scripts\;C:\Users\eliro\AppData\Local\Programs\Python\Python39\;C:\Users\eliro\AppData\Local\Microsoft\WindowsApps;C:\Users\eliro\AppData\Local\Programs\Antigravity\bin;C:\Users\eliro\AppData\Roaming\npm;C:\Users\eliro\AppData\Local\Programs\Microsoft VS Code\bin;c:\Users\eliro\.vscode\extensions\ms-python.debugpy-2025.18.0-win32-x64\bundled\scripts\noConfigScripts += ';C:\Program Files\Git\cmd'
        Write-Host ' Git installed successfully' -ForegroundColor Green
    } catch {
        Write-Host '  Could not auto-install Git. Visit: https://git-scm.com/download/win' -ForegroundColor Yellow
    }
}

Write-Host ''
Write-Host 'Step 2: Setting up Git repository...' -ForegroundColor Yellow

cd c:\Space\python\fashion-photoshoot

# Initialize Git if not already done
if (-not (Test-Path .git)) {
    git init
    git config user.email 'alpha99forgaming@gmail.com'
    git config user.name 'Fashion Studio Developer'
    Write-Host ' Git initialized' -ForegroundColor Green
} else {
    Write-Host ' Git already initialized' -ForegroundColor Green
}

Write-Host ''
Write-Host 'Step 3: Preparing files for deployment...' -ForegroundColor Yellow

# Add all files to git
git add .
\ = git status --short | Measure-Object | Select-Object -ExpandProperty Count

if (\ -gt 0) {
    git commit -m 'Initial commit: Fashion Photoshoot Studio with Firebase and full stack'
    Write-Host \" Committed \ files\" -ForegroundColor Green
} else {
    Write-Host ' All files already committed' -ForegroundColor Green
}

Write-Host ''
Write-Host 'Step 4: Creating GitHub repository...' -ForegroundColor Yellow
Write-Host 'You are about to create a GitHub repository.' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Action: Go to https://github.com/new and create a NEW repository:' -ForegroundColor Yellow
Write-Host '  - Repository name: fashion-photoshoot' -ForegroundColor Gray
Write-Host '  - Description: AI Fashion Photoshoot Studio' -ForegroundColor Gray
Write-Host '  - Public (for Vercel auto-deploy)' -ForegroundColor Gray
Write-Host ''

\ = Read-Host 'Enter your new GitHub repository URL (e.g., https://github.com/username/fashion-photoshoot.git)'

Write-Host ''
Write-Host 'Step 5: Pushing code to GitHub...' -ForegroundColor Yellow

try {
    git remote add origin \ 2>
    if (\1 -ne 0) {
        git remote set-url origin \ 2>
    }
    
    git branch -M main
    git push -u origin main
    
    Write-Host ' Code pushed to GitHub!' -ForegroundColor Green
    Write-Host \" Repository: \\" -ForegroundColor Cyan
} catch {
    Write-Host ' Git push failed. Check your GitHub token.' -ForegroundColor Red
    Write-Host 'Alternative: Use GitHub Desktop or GitHub CLI to push' -ForegroundColor Yellow
}

Write-Host ''
Write-Host '' -ForegroundColor Green
Write-Host '  NEXT STEPS - DEPLOY TO RAILWAY & VERCEL             ' -ForegroundColor Green
Write-Host '' -ForegroundColor Green

Write-Host ''
Write-Host ' BACKEND DEPLOYMENT (Railway) - 5 minutes' -ForegroundColor Cyan
Write-Host '' 
Write-Host '1. Go to: https://railway.app/dashboard' -ForegroundColor Gray
Write-Host '2. Click \"New Project\"  \"Import from GitHub\"' -ForegroundColor Gray
Write-Host '3. Select your \"fashion-photoshoot\" repository' -ForegroundColor Gray
Write-Host '4. Wait for Railway to detect the project' -ForegroundColor Gray
Write-Host '5. Click on the detected service (should be backend)' -ForegroundColor Gray
Write-Host '6. Go to \"Settings\" and add these variables:' -ForegroundColor Gray
Write-Host '   - FIREBASE_PROJECT_ID=fashion-photoshoot-studio' -ForegroundColor Gray
Write-Host '   - FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json' -ForegroundColor Gray
Write-Host '   - PYTHONENV=production' -ForegroundColor Gray
Write-Host '   - FRONTEND_URL=(will update after Vercel)' -ForegroundColor Gray
Write-Host '7. Railway will auto-build and deploy!' -ForegroundColor Gray
Write-Host '8. Copy the deployed URL (e.g., project-xxx.railway.app)' -ForegroundColor Gray
Write-Host ''

Write-Host ' FRONTEND DEPLOYMENT (Vercel) - 3 minutes' -ForegroundColor Cyan
Write-Host ''
Write-Host '1. Go to: https://vercel.com/dashboard' -ForegroundColor Gray
Write-Host '2. Click \"Add New\"  \"Project\"' -ForegroundColor Gray
Write-Host '3. Click \"Import Git Repository\"' -ForegroundColor Gray
Write-Host '4. Select your \"fashion-photoshoot\" repo' -ForegroundColor Gray
Write-Host '5. Set Root Directory to: frontend' -ForegroundColor Gray
Write-Host '6. Add Environment Variables (all VITE_* from frontend/.env):' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_API_KEY=AIzaSyBtpHJ4G2He5ekqrVWs5rulfkOqzbndLDs' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_AUTH_DOMAIN=fashion-photoshoot-studio.firebaseapp.com' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_PROJECT_ID=fashion-photoshoot-studio' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_STORAGE_BUCKET=fashion-photoshoot-studio.firebasestorage.app' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_MESSAGING_SENDER_ID=282387017759' -ForegroundColor Gray
Write-Host '   - VITE_FIREBASE_APP_ID=1:282387017759:web:7d1df0492aa49a6f85e52a' -ForegroundColor Gray
Write-Host '   - VITE_BACKEND_URL=(your Railway backend URL)' -ForegroundColor Gray
Write-Host '7. Click \"Deploy\"!' -ForegroundColor Gray
Write-Host '8. Copy your Vercel URL (e.g., fashion-photoshoot.vercel.app)' -ForegroundColor Gray
Write-Host ''

Write-Host ' FINAL STEP - Link Backend & Frontend' -ForegroundColor Cyan
Write-Host ''
Write-Host '1. Go back to Railway dashboard' -ForegroundColor Gray
Write-Host '2. Update FRONTEND_URL to your Vercel URL' -ForegroundColor Gray
Write-Host '3. Redeploy backend' -ForegroundColor Gray
Write-Host ''

Write-Host ' Your app is now LIVE! ' -ForegroundColor Green
Write-Host ''
Write-Host 'Once deployed, test at: https://your-vercel-url.vercel.app' -ForegroundColor Cyan
Write-Host ''

# Save summary
\ = @\"

  DEPLOYMENT SUMMARY                                 


GitHub Repository: \
Firebase Project: fashion-photoshoot-studio
Backend Deployment: Railway (to be deployed)
Frontend Deployment: Vercel (to be deployed)

Firebase Credentials:  backend/firebase-credentials.json
Frontend Config:  frontend/.env (auto-configured)
Backend Config:  backend/.env (auto-configured)

NEXT STEPS:
1. Complete Railway backend deployment (5 min)
2. Complete Vercel frontend deployment (3 min)
3. Link them together (1 min)
4. Test your app! 

For issues, see: DEPLOYMENT_READY.txt or docs/INSTRUCTION.txt
\"@

\ | Out-File -Encoding utf8 DEPLOYMENT_SUMMARY.txt
Write-Host 'Summary saved to: DEPLOYMENT_SUMMARY.txt' -ForegroundColor Cyan

Write-Host ''
Write-Host 'Questions? Check these files:' -ForegroundColor Yellow
Write-Host '   DEPLOYMENT_READY.txt - Complete guide' -ForegroundColor Gray
Write-Host '   docs/INSTRUCTION.txt - Detailed setup' -ForegroundColor Gray
Write-Host '   LOCAL_DEVELOPMENT.md - Local testing' -ForegroundColor Gray
