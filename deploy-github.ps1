function Push-ToGitHub {
    param(
        [string]$RepoPath = "c:\Space\python\fashion-photoshoot"
    )
    
    Push-Location $RepoPath
    try {
        # Clean up rebase state
        Write-Host "Cleaning rebase state..." -ForegroundColor Cyan
        if (Test-Path '.git\rebase-merge') {
            Remove-Item -Recurse -Force '.git\rebase-merge' -ErrorAction SilentlyContinue
        }
        if (Test-Path '.git\REBASE_HEAD') {
            Remove-Item -Force '.git\REBASE_HEAD' -ErrorAction SilentlyContinue
        }
        if (Test-Path '.git\MERGE_HEAD') {
            Remove-Item -Force '.git\MERGE_HEAD' -ErrorAction SilentlyContinue
        }
        
        # Reset to local commit
        Write-Host "Resetting to local commit..." -ForegroundColor Cyan
        $localCommit = '80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6'
        @"
ref: refs/heads/main
"@ | Set-Content -Path '.git\HEAD' -NoNewline -Encoding ASCII
        
        $localCommit | Set-Content -Path '.git\refs\heads\main' -NoNewline -Encoding ASCII
        
        # Push using Start-Process with credential helper
        Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
        
        $env:GIT_ASKPASS_OVERRIDE = 'true'
        $env:GIT_TRACE = '1'
        
        $gitPath = 'C:\Program Files\Git\cmd\git.exe'
        $args = @('push', '-u', 'origin', 'main', '--force', '-v')
        
        # Use git credential helper to avoid prompt
        $process = Start-Process -FilePath $gitPath `
            -ArgumentList $args `
            -WindowStyle Hidden `
            -Wait `
            -PassThru `
            -RedirectStandardOutput "$RepoPath\git_push_out.txt" `
            -RedirectStandardError "$RepoPath\git_push_err.txt" `
            -NoNewWindow
        
        # Display output
        Write-Host "Push exit code: $($process.ExitCode)" -ForegroundColor Yellow
        
        if (Test-Path "$RepoPath\git_push_out.txt") {
            Write-Host "=== STDOUT ===" -ForegroundColor Green
            Get-Content "$RepoPath\git_push_out.txt"
        }
        
        if (Test-Path "$RepoPath\git_push_err.txt") {
            Write-Host "=== STDERR ===" -ForegroundColor Red
            Get-Content "$RepoPath\git_push_err.txt"
        }
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Push succeeded!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "Push failed with exit code $($process.ExitCode)" -ForegroundColor Red
            return $false
        }
    }
    finally {
        Pop-Location
    }
}

# Execute
Push-ToGitHub
