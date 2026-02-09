@echo off
REM Clean rebuild of frontend dependencies
cd /d "c:\Space\python\fashion-photoshoot\frontend"

echo [*] Cleaning npm cache and node_modules...
call npm cache clean --force
if exist node_modules rmdir /s /q node_modules

echo [*] Installing dependencies (clean)...
call npm install

echo [*] Auditing and fixing vulnerabilities...
call npm audit fix --force

echo [*] Building SvelteKit...
call npm run build

if errorlevel 1 (
    echo [!] Build failed
    pause
    exit /b 1
)

echo [+] Build successful!
echo [*] Ready to deploy
pause
