# Fashion Photoshoot Studio - Automated Deployment Script
# This script prepares your project for deployment

param(
    [string]$GitHubRepo = "",
    [string]$ProjectName = "fashion-photoshoot"
)

Write-Host "🚀 Fashion Photoshoot Studio - Deployment Setup" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

$nodeExists = node --version 2>$null
if (-not $nodeExists) {
    Write-Host "❌ Node.js not found. Please install from https://nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Node.js installed: $($nodeExists.Trim())" -ForegroundColor Green

$npmExists = npm --version 2>$null
if (-not $npmExists) {
    Write-Host "❌ npm not found" -ForegroundColor Red
    exit 1
}
Write-Host "✅ npm installed: $($npmExists.Trim())" -ForegroundColor Green

# Get GitHub repo URL
if (-not $GitHubRepo) {
    Write-Host "`n📌 GitHub Repository Setup" -ForegroundColor Yellow
    $GitHubRepo = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/fashion-photoshoot)"
}

# Initialize Git
Write-Host "`n📦 Initializing Git repository..." -ForegroundColor Yellow
if (-not (Test-Path .git)) {
    git init 2>$null
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Add and commit
Write-Host "`n💾 Creating initial commit..." -ForegroundColor Yellow
git add . 2>$null
$commitMessage = "Initial commit: Fashion Photoshoot Studio - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git commit -m $commitMessage 2>$null
Write-Host "✅ Committed: $commitMessage" -ForegroundColor Green

# Add remote
Write-Host "`n🔗 Adding GitHub remote..." -ForegroundColor Yellow
git remote add origin $GitHubRepo 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote set-url origin $GitHubRepo 2>$null
}
Write-Host "✅ GitHub remote configured: $GitHubRepo" -ForegroundColor Green

# Install Vercel CLI
Write-Host "`n⚙️  Installing Vercel CLI..." -ForegroundColor Yellow
npm install -g vercel 2>$null
Write-Host "✅ Vercel CLI installed" -ForegroundColor Green

# Navigate to frontend
Write-Host "`n📁 Setting up frontend..." -ForegroundColor Yellow
Push-Location frontend

# Install dependencies
Write-Host "📥 Installing frontend dependencies..." -ForegroundColor Yellow
npm install
Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green

Pop-Location

# Create .env files
Write-Host "`n🔐 Creating environment templates..." -ForegroundColor Yellow

if (-not (Test-Path frontend\.env)) {
    Copy-Item frontend\.env.example frontend\.env
    Write-Host "✅ Created frontend/.env" -ForegroundColor Green
}

if (-not (Test-Path backend\.env)) {
    Copy-Item backend\.env.example backend\.env
    Write-Host "✅ Created backend/.env" -ForegroundColor Green
}

# Summary
Write-Host "`n✨ Setup Complete! Next Steps:" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "1️⃣  Update your Firebase credentials:" -ForegroundColor Yellow
Write-Host "   - frontend/.env (add VITE_FIREBASE_* variables)" -ForegroundColor Gray
Write-Host "   - backend/.env (add Firebase service account credentials)" -ForegroundColor Gray

Write-Host "`n2️⃣  Push to GitHub:" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray

Write-Host "`n3️⃣  Deploy Backend to Railway:" -ForegroundColor Yellow
Write-Host "   - Go to https://railway.app" -ForegroundColor Gray
Write-Host "   - Connect GitHub repo" -ForegroundColor Gray
Write-Host "   - Set environment variables" -ForegroundColor Gray

Write-Host "`n4️⃣  Deploy Frontend to Vercel:" -ForegroundColor Yellow
Write-Host "   - Option A: vercel deploy --prod" -ForegroundColor Gray
Write-Host "   - Option B: https://vercel.com → Import repo → Set env vars" -ForegroundColor Gray

Write-Host "`n5️⃣  Update backend FRONTEND_URL:" -ForegroundColor Yellow
Write-Host "   - Set to your Vercel deployment URL" -ForegroundColor Gray

Write-Host "`n📚 Full guide: DEPLOYMENT_STEPS.md" -ForegroundColor Cyan
Write-Host "`n"
