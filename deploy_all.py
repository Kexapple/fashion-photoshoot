#!/usr/bin/env python3
"""
Complete Deployment Script - Vercel Frontend + Railway Backend
Handles all deployment steps autonomously
"""

import subprocess
import os
import sys
from pathlib import Path

REPO_PATH = Path(r"c:\Space\python\fashion-photoshoot")
FRONTEND_PATH = REPO_PATH / "frontend"
BACKEND_PATH = REPO_PATH / "backend"

def run_cmd(cmd, cwd=None, label=""):
    """Execute command and report results."""
    print(f"\n[*] {label}...")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or REPO_PATH,
            capture_output=True,
            text=True,
            timeout=300,
            shell=True
        )
        
        if result.returncode == 0:
            print(f"[✓] {label} successful")
            if result.stdout:
                print(result.stdout[:300])
            return True
        else:
            print(f"[!] {label} exited with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"[!] Exception: {str(e)[:100]}")
        return False

def deploy_vercel():
    """Deploy frontend to Vercel."""
    print("\n" + "="*60)
    print("PHASE 1: VERCEL FRONTEND DEPLOYMENT")
    print("="*60)
    
    # Install dependencies with legacy peer deps
    run_cmd(
        "npm install --legacy-peer-deps",
        cwd=FRONTEND_PATH,
        label="npm install (legacy peer deps)"
    )
    
    # Deploy to Vercel
    vercel_success = run_cmd(
        "vercel --prod --confirm --name fashion-photoshoot",
        cwd=FRONTEND_PATH,
        label="Vercel deploy"
    )
    
    return vercel_success

def deploy_railway():
    """Deploy backend to Railway."""
    print("\n" + "="*60)
    print("PHASE 2: RAILWAY BACKEND DEPLOYMENT")
    print("="*60)
    
    railway_success = run_cmd(
        "railway up",
        cwd=BACKEND_PATH,
        label="Railway deploy"
    )
    
    return railway_success

def main():
    """Main deployment orchestration."""
    print("\n" + "🚀 "*30)
    print("FASHION PHOTOSHOOT STUDIO - AUTONOMOUS DEPLOYMENT")
    print("🚀 "*30)
    
    vercel_ok = deploy_vercel()
    railway_ok = deploy_railway()
    
    print("\n" + "="*60)
    print("DEPLOYMENT SUMMARY")
    print("="*60)
    print(f"Vercel:  {'✅ SUCCESS' if vercel_ok else '❌ FAILED'}")
    print(f"Railway: {'✅ SUCCESS' if railway_ok else '❌ FAILED'}")
    print("="*60)
    
    print("\n📊 Expected URLs:")
    print("   Frontend: https://fashion-photoshoot.vercel.app")
    print("   Backend:  Check Railway dashboard")
    print("   GitHub:   https://github.com/Kexapple/fashion-photoshoot")
    
    return 0 if (vercel_ok and railway_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
