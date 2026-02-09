#!/usr/bin/env python3
"""
Direct Git Push Script - Bypasses terminal TTY interception
Uses subprocess to invoke git without TTY
"""

import subprocess
import os
import shutil
import sys

REPO_PATH = r"c:\Space\python\fashion-photoshoot"
LOCAL_COMMIT = "80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6"
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

def cleanup_rebase_state():
    """Remove rebase-merge and REBASE_HEAD to clear rebase state."""
    print("[*] Cleaning up rebase state...")
    rebase_dir = os.path.join(REPO_PATH, ".git", "rebase-merge")
    rebase_head = os.path.join(REPO_PATH, ".git", "REBASE_HEAD")
    merge_head = os.path.join(REPO_PATH, ".git", "MERGE_HEAD")
    
    if os.path.exists(rebase_dir):
        shutil.rmtree(rebase_dir, ignore_errors=True)
        print(f"[+] Removed {rebase_dir}")
    
    for f in [rebase_head, merge_head]:
        if os.path.exists(f):
            os.remove(f)
            print(f"[+] Removed {f}")

def reset_to_local_commit():
    """Reset main branch to local commit."""
    print(f"[*] Resetting to local commit {LOCAL_COMMIT}...")
    main_ref = os.path.join(REPO_PATH, ".git", "refs", "heads", "main")
    with open(main_ref, "w") as f:
        f.write(LOCAL_COMMIT)
    print(f"[+] main → {LOCAL_COMMIT}")

def push_to_github():
    """Push to GitHub using subprocess without TTY."""
    os.chdir(REPO_PATH)
    
    print("[*] Pushing to GitHub with --force...")
    
    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    env.pop("GIT_SSH_COMMAND", None)
    
    cmd = [GIT_PATH, "push", "-u", "origin", "main", "--force", "-v"]
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            stdin=subprocess.DEVNULL,
        )
        
        print("[=== STDOUT ===]")
        print(result.stdout)
        
        if result.stderr:
            print("[=== STDERR ===]")
            print(result.stderr)
        
        print(f"[*] Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("[+] Push succeeded!")
            return True
        else:
            print("[-] Push failed!")
            return False
    
    except subprocess.TimeoutExpired:
        print("[-] Push command timed out!")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Fashion Photoshoot - Git Push Script")
    print("=" * 60)
    
    cleanup_rebase_state()
    reset_to_local_commit()
    success = push_to_github()
    
    print("=" * 60)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
