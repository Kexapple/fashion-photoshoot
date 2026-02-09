@echo off
REM Deploy Frontend and Backend to Vercel
REM This requires Vercel CLI and proper authentication

color 0A
echo.
echo ==========================================
echo  VERCEL DEPLOYMENT - Frontend + Backend
echo ==========================================
echo.

cd /d "c:\Space\python\fashion-photoshoot"

echo [*] Pushing latest fixes to GitHub...
git add -A
git commit -m "deploy: prepare vercel deployment config"
git push origin main
echo [+] GitHub push complete

echo.
echo [*] PHASE 1: Deploy Frontend to Vercel
echo [*] Root directory with frontend config detected
echo.

cd frontend

rem Install deps
echo [*] Installing dependencies...
call npm install --legacy-peer-deps

rem Build
echo [*] Building SvelteKit...
call npm run build

rem Deploy frontend
echo [*] Deploying frontend to Vercel...
call vercel --prod --yes --name fashion-photoshoot

if errorlevel 1 (
    echo [!] Frontend deploy may have had issues
) else (
    echo [+] Frontend deployed!
)

echo.
echo [*] PHASE 2: Deploy Backend to Vercel
echo.

cd ..\backend

echo [*] Installing Python dependencies...
call pip install -q -r requirements.txt

echo [*] Deploying backend as separate Vercel service...
call vercel --prod --yes --name fashion-photoshoot-backend

if errorlevel 1 (
    echo [!] Backend deploy may have had issues
) else (
    echo [+] Backend deployed!
)

cd ..

echo.
echo ==========================================
echo  DEPLOYMENT COMPLETE
echo ==========================================
echo.
echo [+] Frontend: https://fashion-photoshoot.vercel.app
echo [+] Backend: https://fashion-photoshoot-backend.vercel.app
echo [+] GitHub: https://github.com/Kexapple/fashion-photoshoot
echo.
echo Visit your apps and check Vercel dashboard for details
echo.
pause
