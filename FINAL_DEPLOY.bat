@echo off
REM Fashion Photoshoot Studio - Complete Deployment
REM Fixes npm dependency issues and deploys to Vercel + Railway

setlocal enabledelayedexpansion

color 0A
echo.
echo ========================================
echo  DEPLOYMENT: Frontend (Vercel) + Backend (Railway)
echo ========================================
echo.

cd /d "c:\Space\python\fashion-photoshoot"

REM =========== VERCEL FRONTEND ===========
echo [*] PHASE 1: Deploying Frontend to Vercel
echo.

cd frontend

echo [*] Installing npm dependencies (with legacy peer deps)...
call npm install --legacy-peer-deps

if errorlevel 1 (
    echo [!] npm install failed
    goto RAILWAY_DEPLOY
)

echo [+] Dependencies installed
echo.
echo [*] Deploying to Vercel...
call vercel --prod --confirm --name fashion-photoshoot

echo.
echo [+] Vercel deployment triggered!
echo.

REM =========== RAILWAY BACKEND ===========
:RAILWAY_DEPLOY
echo [*] PHASE 2: Deploying Backend to Railway
echo.

cd ..\backend

echo [*] Deploying to Railway...
call railway up

if errorlevel 1 (
    echo [!] Railway deployment had issues
) else (
    echo [+] Railway deployment triggered!
)

cd ..
echo.
echo ========================================
echo  DEPLOYMENT SUMMARY
echo ========================================
echo [+] Frontend: Vercel deployment in progress
echo [+] Backend: Railway deployment in progress
echo.
echo Visit these URLs after deployment completes:
echo - Frontend: https://fashion-photoshoot.vercel.app
echo - Backend: Check Railway dashboard for URL
echo.
echo Press any key to exit...
pause >nul
