@echo off
REM Fashion Photoshoot Studio - One-Click Deployment
REM This batch file can be double-clicked to run deployments
REM It will open a new window and execute commands there

setlocal enabledelayedexpansion

cd /d "c:\Space\python\fashion-photoshoot"

REM Clean git state
echo [*] Cleaning git rebase state...
if exist ".git\rebase-merge" (
    rmdir /s /q ".git\rebase-merge" 2>nul
    echo [+] Removed rebase-merge
)
if exist ".git\REBASE_HEAD" (
    del ".git\REBASE_HEAD" 2>nul
    echo [+] Removed REBASE_HEAD
)

REM Reset main ref using git plumbing
echo [*] Resetting main branch...
echo 80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6 > ".git\refs\heads\main"
echo [+] main reset to local commit

REM Push to GitHub
echo [*] Pushing to GitHub...
call "C:\Program Files\Git\cmd\git.exe" push -u origin main --force

if errorlevel 1 (
    echo [!] GitHub push failed!
    pause
    exit /b 1
)

echo [+] GitHub push successful!

REM Deploy to Vercel  
echo [*] Deploying frontend to Vercel...
cd frontend
call vercel deploy --prod
if errorlevel 1 echo [!] Vercel deploy had warnings or failed
cd ..

REM Deploy to Railway
echo [*] Deploying backend to Railway...
cd backend
call railway up
if errorlevel 1 echo [!] Railway deploy had warnings or failed
cd ..

echo.
echo [+] Deployment script completed!
echo [*] Check the above output for success/failure messages
pause
