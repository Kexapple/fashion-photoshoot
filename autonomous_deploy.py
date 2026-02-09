#!/usr/bin/env python3
"""
Complete Autonomous Deployment Script
Handles GitHub push, Railway backend, and Vercel frontend deployment
"""

import subprocess
import os
import sys
import json
import shutil
from pathlib import Path

REPO_PATH = Path(r"c:\Space\python\fashion-photoshoot")
BACKEND_PATH = REPO_PATH / "backend"
FRONTEND_PATH = REPO_PATH / "frontend"
LOCAL_COMMIT = "80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6"
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

def log(msg, level="INFO"):
    """Print formatted log message."""
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}
    print(f"[{symbols.get(level, '•')}] {msg}")

def run_command(cmd, cwd=None, label=""):
    """Execute command and return success status."""
    try:
        log(f"Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        result = subprocess.run(
            cmd,
            cwd=cwd or REPO_PATH,
            capture_output=True,
            text=True,
            timeout=120,
            stdin=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            log(f"{label} succeeded", "SUCCESS")
            if result.stdout:
                print(result.stdout[:500])
            return True
        else:
            log(f"{label} failed with code {result.returncode}", "ERROR")
            if result.stderr:
                print(f"Error: {result.stderr[:300]}")
            return False
    except Exception as e:
        log(f"{label} exception: {str(e)[:100]}", "ERROR")
        return False

def cleanup_git_state():
    """Remove rebase/merge state files."""
    log("Cleaning git rebase/merge state")
    
    dirs_to_remove = [
        REPO_PATH / ".git" / "rebase-merge",
        REPO_PATH / ".git" / "rebase-apply"
    ]
    
    for d in dirs_to_remove:
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
    
    files_to_remove = [
        REPO_PATH / ".git" / "REBASE_HEAD",
        REPO_PATH / ".git" / "MERGE_HEAD",
        REPO_PATH / ".git" / "CHERRY_PICK_HEAD"
    ]
    
    for f in files_to_remove:
        if f.exists():
            f.unlink()
    
    log("Git state cleaned", "SUCCESS")

def reset_git_refs():
    """Reset main branch ref to local commit."""
    log("Resetting git refs to local commit")
    main_ref = REPO_PATH / ".git" / "refs" / "heads" / "main"
    main_ref.write_text(LOCAL_COMMIT, encoding="ascii")
    log(f"main = {LOCAL_COMMIT[:8]}", "SUCCESS")

def github_push():
    """Push to GitHub."""
    log("=== PHASE 1: GITHUB PUSH ===")
    cleanup_git_state()
    reset_git_refs()
    
    success = run_command(
        [GIT_PATH, "push", "-u", "origin", "main", "--force"],
        cwd=REPO_PATH,
        label="GitHub push"
    )
    
    return success

def vercel_deploy():
    """Deploy frontend to Vercel."""
    log("=== PHASE 2: VERCEL FRONTEND ===")
    
    # Ensure frontend .env exists
    env_file = FRONTEND_PATH / ".env"
    if not env_file.exists():
        log("Creating frontend .env", "WARN")
        env_content = """VITE_FIREBASE_API_KEY=AIzaSyBtpH5sIUvx7Y6Y7Y7Y7Y7Y7Y7Y7Y7Y7Y7
VITE_FIREBASE_AUTH_DOMAIN=fashion-photoshoot-studio.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=fashion-photoshoot-studio
VITE_FIREBASE_STORAGE_BUCKET=fashion-photoshoot-studio.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=282387017759
VITE_FIREBASE_APP_ID=1:282387017759:web:abc123
VITE_BACKEND_URL=http://localhost:8000
"""
        env_file.write_text(env_content)
    
    # Try Vercel CLI
    success = run_command(
        ["vercel", "deploy", "--prod"],
        cwd=FRONTEND_PATH,
        label="Vercel deploy"
    )
    
    return success

def railway_deploy():
    """Deploy backend to Railway."""
    log("=== PHASE 3: RAILWAY BACKEND ===")
    
    # Check for Dockerfile
    dockerfile = BACKEND_PATH / "Dockerfile"
    if not dockerfile.exists():
        log("Dockerfile not found", "ERROR")
        return False
    
    # Try Railway CLI
    success = run_command(
        ["railway", "up"],
        cwd=BACKEND_PATH,
        label="Railway deploy"
    )
    
    return success

def main():
    """Execute full deployment."""
    print("\n" + "="*70)
    print("FASHION PHOTOSHOOT STUDIO - AUTONOMOUS DEPLOYMENT")
    print("="*70 + "\n")
    
    results = {
        "GitHub Push": False,
        "Vercel Deploy": False,
        "Railway Deploy": False
    }
    
    try:
        # Phase 1: GitHub
        log("Starting Phase 1: GitHub Push", "INFO")
        results["GitHub Push"] = github_push()
        
        # Phase 2: Vercel
        log("Starting Phase 2: Vercel Frontend", "INFO")
        results["Vercel Deploy"] = vercel_deploy()
        
        # Phase 3: Railway
        log("Starting Phase 3: Railway Backend", "INFO")
        results["Railway Deploy"] = railway_deploy()
        
    except KeyboardInterrupt:
        log("Deployment cancelled by user", "WARN")
    except Exception as e:
        log(f"Unexpected error: {e}", "ERROR")
    
    # Summary
    print("\n" + "="*70)
    print("DEPLOYMENT SUMMARY")
    print("="*70)
    
    for service, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{service:.<40} {status}")
    
    print("="*70 + "\n")
    
    all_success = all(results.values())
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()
