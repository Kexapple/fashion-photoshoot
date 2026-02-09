# Robust deployment script for Fashion Photoshoot Studio
# Usage: Run PowerShell as Administrator, then:
# cd c:\Space\python\fashion-photoshoot
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# .\DEPLOY.ps1

$ErrorActionPreference = 'Stop'
$projectPath = "c:\Space\python\fashion-photoshoot"
Set-Location $projectPath

Write-Host "=== FASHION PHOTOSHOOT - DEPLOY BEGIN ===" -ForegroundColor Cyan

# Helper: find git
function Get-GitPath {
    $paths = @(
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles(x86)\Git\cmd\git.exe",
        "C:\\Program Files\\Git\\cmd\\git.exe",
        "C:\\Program Files (x86)\\Git\\cmd\\git.exe"
    )
    foreach ($p in $paths) { if (Test-Path $p) { return $p } }
    # fallback to PATH
    try { & git --version > $null 2>&1; return 'git' } catch { return $null }
}

$git = Get-GitPath
if (-not $git) {
    Write-Host "Git not found in standard locations or PATH." -ForegroundColor Yellow
    Write-Host "Please install Git (https://git-scm.com/download/win) or open Git Bash and run the manual commands." -ForegroundColor Yellow
    exit 1
}
Write-Host "Using git: $git" -ForegroundColor Green

# 1) Initialize repo and push to GitHub
Write-Host "\n[1/4] Preparing Git repository..." -ForegroundColor Cyan
if (-not (Test-Path "$projectPath\.git")) {
    & $git init
    & $git config user.email "alpha99forgaming@gmail.com"
    & $git config user.name "Kexapple"
    Write-Host "Initialized git repository." -ForegroundColor Green
} else { Write-Host "Git repository already initialized." -ForegroundColor Green }

# Stage & commit
& $git add .
# commit only if there are changes
$changes = (& $git status --porcelain) -join "`n"
if ($changes) { & $git commit -m "Initial commit: Fashion Photoshoot Studio" } else { Write-Host "No changes to commit." -ForegroundColor Yellow }

# Set remote
$remote = "https://github.com/Kexapple/fashion-photoshoot.git"
try { & $git remote add origin $remote } catch { & $git remote set-url origin $remote }
& $git branch -M main

Write-Host "Pushing to GitHub (this may prompt for credentials/token)..." -ForegroundColor Cyan
try {
    & $git push -u origin main
    Write-Host "Pushed to GitHub." -ForegroundColor Green
} catch {
    Write-Host "Git push failed. If credentials are required, open Git Bash and run the push there or configure a PAT credential helper." -ForegroundColor Red
}

# 2) Deploy backend: provide Railway instructions or attempt via CLI if installed
Write-Host "\n[2/4] Deploying backend to Railway..." -ForegroundColor Cyan
# If Railway CLI is available, attempt quick deploy; otherwise provide manual instructions
try {
    & railway status > $null 2>&1
    Write-Host "Railway CLI found — attempting quick deploy..." -ForegroundColor Gray
    # link project if not linked
    & railway up --detach
    Write-Host "Railway: deployment triggered." -ForegroundColor Green
} catch {
    Write-Host "Railway CLI not available or automated deploy failed." -ForegroundColor Yellow
    Write-Host "Manual steps: go to https://railway.app → New Project → Import from GitHub → select repo → set root=backend → add env vars and deploy." -ForegroundColor Gray
}

# 3) Deploy frontend to Vercel
Write-Host "\n[3/4] Deploying frontend to Vercel..." -ForegroundColor Cyan
# Install vercel CLI locally if not present
$vercelExists = $false
try { & vercel --version > $null 2>&1; $vercelExists = $true } catch { $vercelExists = $false }
if (-not $vercelExists) {
    Write-Host "Vercel CLI not found — installing globally (requires npm & admin rights)..." -ForegroundColor Gray
    try { npm install -g vercel --silent; Write-Host "Vercel CLI installed." -ForegroundColor Green; $vercelExists = $true } catch { Write-Host "Global install failed — please install Vercel CLI manually: npm i -g vercel" -ForegroundColor Yellow }
}

if ($vercelExists) {
    Push-Location "$projectPath\frontend"
    Write-Host "Running: vercel deploy --prod --confirm" -ForegroundColor Gray
    try {
        # Pass environment vars through Vercel interactive deploy will prompt for login if needed
        vercel deploy --prod --confirm
        Write-Host "Vercel deployment triggered." -ForegroundColor Green
    } catch {
        Write-Host "Vercel deploy failed. Check Vercel login or run 'vercel login' and retry." -ForegroundColor Red
    }
    Pop-Location
} else {
    Write-Host "Skipping Vercel automated deploy. Follow manual steps: https://vercel.com → Import GitHub repo → set root to 'frontend' → add VITE_* env vars → Deploy." -ForegroundColor Yellow
}

# 4) Final instructions
Write-Host "\n[4/4] Final steps and verification" -ForegroundColor Cyan
Write-Host " - If Railway/Vercel deploys succeeded, copy their URLs and update backend FRONTEND_URL env var in Railway." -ForegroundColor Gray
Write-Host " - Test the frontend URL in browser." -ForegroundColor Gray

Write-Host "\n=== DEPLOY COMPLETE (or manual steps provided where automation failed) ===" -ForegroundColor Cyan
