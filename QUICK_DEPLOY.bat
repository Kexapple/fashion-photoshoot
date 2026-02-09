 
@echo off
cd /d "c:\Space\python\fashion-photoshoot\frontend"

echo [*] Deploying to Vercel...
vercel --prod --confirm --name fashion-photoshoot

pause