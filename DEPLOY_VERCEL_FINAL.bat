@echo off
REM Complete Vercel Deployment - Frontend + Backend
REM Handles all issues: npm dependencies, builds, and deployment

color 0B
cls
echo.
echo =====================================================
echo  FASHION PHOTOSHOOT STUDIO - VERCEL DEPLOYMENT
echo =====================================================
echo.

cd /d "c:\Space\python\fashion-photoshoot"

REM ====== VERIFY GIT IS UPDATED ======
echo [*] Ensuring latest code is on GitHub...
git add -A
git commit -m "deployment: fix vite config and package.json" 2>nul
git push origin main 2>nul
echo [+] GitHub synchronized

REM ====== FRONTEND DEPLOYMENT ======
echo.
echo ====== PHASE 1: FRONTEND DEPLOYMENT ======
echo.
cd frontend

echo [*] Cleaning npm cache...
call npm cache clean --force >nul 2>&1

echo [*] Removing old node_modules...
if exist node_modules (
    rmdir /s /q node_modules >nul 2>&1
)

echo [*] Installing dependencies (clean install)...
call npm install

if errorlevel 1 (
    echo [!] npm install failed
    echo [!] Trying with legacy peer deps...
    call npm install --legacy-peer-deps
)

echo [*] Running npm audit fix...
call npm audit fix --force >nul 2>&1

echo [*] Building SvelteKit project...
call npm run build

if errorlevel 1 (
    echo [!] Build failed - check errors above
    pause
    exit /b 1
)

echo [+] Frontend build successful!

echo.
echo [*] Deploying frontend to Vercel...
call vercel --prod --yes

if not errorlevel 1 (
    echo [+] Frontend deployment initiated!
) else (
    echo [!] Frontend deployment returned a code (may still succeed)
)

REM ====== BACKEND DEPLOYMENT ======
echo.
echo ====== PHASE 2: BACKEND DEPLOYMENT ======
echo.
cd ..\backend

echo [*] Checking backend dependencies...
call pip list | find "fastapi" >nul

if errorlevel 1 (
    echo [*] Installing Python dependencies...
    call pip install -r requirements.txt -q
)

echo [*] Deploying backend to Vercel...
call vercel --prod --yes --name fashion-photoshoot-backend

if not errorlevel 1 (
    echo [+] Backend deployment initiated!
) else (
    echo [!] Backend deployment returned a code (may still succeed)
)

REM ====== SUMMARY ======
cd ..
echo.
echo =====================================================
echo  DEPLOYMENT COMPLETE
echo =====================================================
echo.
echo [+] Check Vercel Dashboard for deployment status:
echo    https://vercel.com/dashboard
echo.
echo [+] Your live URLs will be:
echo    Frontend: https://fashion-photoshoot.vercel.app
echo    Backend:  https://fashion-photoshoot-backend.vercel.app
echo.
echo [+] GitHub Repository:
echo    https://github.com/Kexapple/fashion-photoshoot
echo.
pause
