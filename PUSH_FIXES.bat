@echo off
REM Quick push for fixed package.json
cd /d "c:\Space\python\fashion-photoshoot"

echo [*] Adding changes...
git add -A

echo [*] Committing fixes...
git commit -m "fix: update package.json with stable SvelteKit versions and add render.yaml"

echo [*] Pushing to GitHub...
git push origin main

echo [+] Push complete!
pause
