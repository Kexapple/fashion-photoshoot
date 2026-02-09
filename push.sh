#!/bin/bash
set -e

cd "$(dirname "$0")"

# Clean rebase state
rm -rf .git/rebase-merge
rm -f .git/REBASE_HEAD

# Reset to local commit
LOCAL_COMMIT="80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6"
echo "$LOCAL_COMMIT" > .git/refs/heads/main

# Configure git to not use editor
export GIT_EDITOR=true
export VISUAL=true
export EDITOR=true

# Push to origin
git push -u origin main --force

echo "Push completed successfully"
