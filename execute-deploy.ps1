$script = @'
# Define paths
$repoPath = "c:\Space\python\fashion-photoshoot"
$localCommit = "80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6"
$gitPath = "C:\Program Files\Git\cmd\git.exe"

Set-Location $repoPath

# Clean git state
Write-Host "[*] Cleaning git rebase state..."
if (Test-Path ".git\rebase-merge") { Remove-Item -Recurse -Force ".git\rebase-merge" }
if (Test-Path ".git\REBASE_HEAD") { Remove-Item -Force ".git\REBASE_HEAD" }

# Reset main ref
Write-Host "[*] Resetting main to local commit..."
Set-Content ".git\refs\heads\main" $localCommit -NoNewline -Encoding ASCII

# Configure git
Write-Host "[*] Configuring git..."
& $gitPath config user.email "alpha99forgaming@gmail.com"
& $gitPath config user.name "Kexapple"

# Push
Write-Host "[*] Pushing to GitHub..."
$pushProcess = Start-Process -FilePath $gitPath `
    -ArgumentList @("push", "-u", "origin", "main", "--force", "-v") `
    -PassThru `
    -NoNewWindow `
    -Wait

if ($pushProcess.ExitCode -eq 0) {
    Write-Host "[+] GITHUB PUSH SUCCEEDED!"
    
    # Now deploy to Vercel
    Write-Host "[*] Deploying frontend to Vercel..."
    Set-Location "$repoPath\frontend"
    & npm install 2>&1 | Out-Null
    & vercel deploy --prod 2>&1
    
    # Deploy to Railway
    Write-Host "[*] Deploying backend to Railway..."
    Set-Location "$repoPath\backend"
    & railway up 2>&1
} else {
    Write-Host "[!] GITHUB PUSH FAILED (exit code: $($pushProcess.ExitCode))"
}

Write-Host "[+] Deployment script completed"
'@

# Save and execute
$scriptPath = "c:\Space\python\fashion-photoshoot\run-deploy.ps1"
Set-Content $scriptPath $script
Write-Host "Saved script to: $scriptPath"
Write-Host "Running deployment..."

# Execute synchronously
& powershell -ExecutionPolicy Bypass -File $scriptPath
