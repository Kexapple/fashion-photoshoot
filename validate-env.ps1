# Environment Configuration Validator
# Checks if all required environment variables are properly set

param(
    [string]$Environment = "development"
)

Write-Host "🔍 Environment Configuration Validator" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

function Test-EnvVar {
    param(
        [string]$VarName,
        [string]$Description,
        [bool]$Required = $true,
        [string]$Location = "backend/.env"
    )
    
    $value = [Environment]::GetEnvironmentVariable($VarName)
    
    if ([string]::IsNullOrWhiteSpace($value)) {
        if ($Required) {
            Write-Host "❌ MISSING: $VarName" -ForegroundColor Red
            Write-Host "   Location: $Location" -ForegroundColor Gray
            Write-Host "   Purpose: $Description" -ForegroundColor Gray
            return $false
        } else {
            Write-Host "⚠️  OPTIONAL: $VarName" -ForegroundColor Yellow
            Write-Host "   Purpose: $Description" -ForegroundColor Gray
            return $true
        }
    } else {
        $masked = if ($value.Length -gt 4) { "*" * ($value.Length - 4) + $value.Substring($value.Length - 4) } else { "****" }
        Write-Host "✅ SET: $VarName" -ForegroundColor Green
        Write-Host "   Value: $masked" -ForegroundColor Gray
        return $true
    }
}

function Test-EnvFile {
    param(
        [string]$FilePath,
        [string]$Label
    )
    
    Write-Host "`n$Label" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────" -ForegroundColor Cyan
    
    if (Test-Path $FilePath) {
        Write-Host "✅ File exists: $FilePath`n" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ File missing: $FilePath" -ForegroundColor Red
        Write-Host "   Create from example: Copy-Item $FilePath.example $FilePath`n" -ForegroundColor Gray
        return $false
    }
}

# Load .env files for testing
function Load-EnvFile {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        return
    }
    
    $content = Get-Content $FilePath
    foreach ($line in $content) {
        if ($line -match '^([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

# Load environment files
Load-EnvFile "frontend\.env"
Load-EnvFile "backend\.env"

# Test frontend configuration
$frontendOk = Test-EnvFile "frontend\.env" "📁 Frontend Configuration"

if ($frontendOk) {
    Write-Host "Required Firebase variables:" -ForegroundColor Yellow
    $fb1 = Test-EnvVar "VITE_FIREBASE_API_KEY" "Firebase API key" $true "frontend/.env"
    $fb2 = Test-EnvVar "VITE_FIREBASE_AUTH_DOMAIN" "Firebase auth domain" $true "frontend/.env"
    $fb3 = Test-EnvVar "VITE_FIREBASE_PROJECT_ID" "Firebase project ID" $true "frontend/.env"
    $fb4 = Test-EnvVar "VITE_FIREBASE_STORAGE_BUCKET" "Firebase storage bucket" $true "frontend/.env"
    $fb5 = Test-EnvVar "VITE_FIREBASE_MESSAGING_SENDER_ID" "Firebase messaging sender ID" $true "frontend/.env"
    $fb6 = Test-EnvVar "VITE_FIREBASE_APP_ID" "Firebase app ID" $true "frontend/.env"
    
    Write-Host "`nBackend connectivity:" -ForegroundColor Yellow
    $backend = Test-EnvVar "VITE_BACKEND_URL" "Backend API URL (http://localhost:8000 for dev)" $true "frontend/.env"
}

# Test backend configuration
$backendOk = Test-EnvFile "backend\.env" "⚙️  Backend Configuration"

if ($backendOk) {
    Write-Host "Required Firebase variables (choose one option):" -ForegroundColor Yellow
    Write-Host "`nOption 1: JSON credentials file" -ForegroundColor Gray
    $fcreds = Test-EnvVar "FIREBASE_CREDENTIALS_PATH" "Path to Firebase service account JSON" $false "backend/.env"
    
    Write-Host "`nOption 2: Individual environment variables" -ForegroundColor Gray
    $f1 = Test-EnvVar "FIREBASE_PROJECT_ID" "Firebase project ID" $false "backend/.env"
    $f2 = Test-EnvVar "FIREBASE_PRIVATE_KEY_ID" "Firebase private key ID" $false "backend/.env"
    $f3 = Test-EnvVar "FIREBASE_PRIVATE_KEY" "Firebase private key" $false "backend/.env"
    $f4 = Test-EnvVar "FIREBASE_CLIENT_EMAIL" "Firebase client email" $false "backend/.env"
    
    Write-Host "`nNano Banana API (Image Generation):" -ForegroundColor Yellow
    $nb1 = Test-EnvVar "NANO_BANANA_API_KEY" "Nano Banana API key" $false "backend/.env"
    $nb2 = Test-EnvVar "NANO_BANANA_MODEL_ID" "Nano Banana model ID" $false "backend/.env"
    
    Write-Host "`nPayment Methods (Optional):" -ForegroundColor Yellow
    $jc1 = Test-EnvVar "JAZZCASH_MERCHANT_ID" "JazzCash merchant ID" $false "backend/.env"
    $jc2 = Test-EnvVar "JAZZCASH_API_KEY" "JazzCash API key" $false "backend/.env"
    $ep1 = Test-EnvVar "EASYPAISA_MERCHANT_ID" "EasyPaisa merchant ID" $false "backend/.env"
    $ep2 = Test-EnvVar "EASYPAISA_API_KEY" "EasyPaisa API key" $false "backend/.env"
    
    Write-Host "`nApplication Settings:" -ForegroundColor Yellow
    $appenv = Test-EnvVar "PYTHONENV" "Python environment (development/production)" $false "backend/.env"
    $frontend_url = Test-EnvVar "FRONTEND_URL" "Frontend URL for CORS" $false "backend/.env"
}

# Summary
Write-Host "`n" -ForegroundColor Cyan
Write-Host "📊 Validation Summary" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan

$summary = @"

MINIMUM REQUIRED FOR LOCAL TESTING:
- ✅ frontend/.env with all Firebase config
- ✅ backend/.env with Firebase credentials
- ⚪ Nano Banana API key (optional, uses mock if missing)
- ⚪ Payment keys (optional for testing)

MINIMUM REQUIRED FOR PRODUCTION:
- ✅ All frontend variables
- ✅ All backend variables
- ✅ Nano Banana API key
- ⚪ Payment gateway keys (if using real payments)

HOW TO GET CREDENTIALS:

1. Firebase:
   - Go to https://console.firebase.google.com
   - Create project
   - Download service account JSON from Project Settings → Service Accounts
   - Use values to populate backend/.env

2. Nano Banana:
   - Sign up at https://www.nanobana.com
   - Create API key
   - Add to backend/.env

3. JazzCash/EasyPaisa:
   - Contact merchant support for credentials
   - Add to backend/.env

NEXT STEPS:
1. Run this validator again after updating .env files
2. Follow DEPLOYMENT_CHECKLIST.md for deployment steps
3. See docs/INSTRUCTION.txt Part 1-2 for detailed credential setup

"@

Write-Host $summary -ForegroundColor White

# Quick test
Write-Host "`n🧪 Running Quick Configuration Test..." -ForegroundColor Yellow

$allVarsSet = ($frontendOk -and $backendOk -and $fb1 -and $fb2 -and $fb3 -and $fb4 -and $fb5 -and $fb6 -and ($fcreds -or $f1))

if ($allVarsSet) {
    Write-Host "✅ Configuration looks good! Ready for testing." -ForegroundColor Green
} else {
    Write-Host "⚠️  Some required variables are missing. See above for details." -ForegroundColor Yellow
}

Write-Host "`nFor help, see: DEPLOYMENT_CHECKLIST.md or docs/INSTRUCTION.txt`n" -ForegroundColor Cyan
