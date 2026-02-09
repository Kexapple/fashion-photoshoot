const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const REPO_PATH = 'c:\\Space\\python\\fashion-photoshoot';
const LOCAL_COMMIT = '80e2590a0ff9b2ee9c58a7c03a846a4dcf9f7bd6';
const GIT_PATH = 'C:\\Program Files\\Git\\cmd\\git.exe';

console.log('=== AUTONOMOUS DEPLOYMENT ===\n');

// Clean git state
const rebaseDir = path.join(REPO_PATH, '.git', 'rebase-merge');
if (fs.existsSync(rebaseDir)) {
    fs.rmSync(rebaseDir, { recursive: true, force: true });
    console.log('[✓] Cleaned rebase-merge');
}

// Reset main ref
const mainRef = path.join(REPO_PATH, '.git', 'refs', 'heads', 'main');
fs.writeFileSync(mainRef, LOCAL_COMMIT, 'ascii');
console.log('[✓] Reset main to local commit');

// Execute git push
console.log('[*] Pushing to GitHub...');
const pushResult = spawnSync(GIT_PATH, ['push', '-u', 'origin', 'main', '--force'], {
    cwd: REPO_PATH,
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe']
});

if (pushResult.status === 0) {
    console.log('[✓✓] GitHub push SUCCEEDED!');
    console.log(pushResult.stdout.substring(0, 500));
    
    // Try Vercel
    console.log('\n[*] Deploying frontend to Vercel...');
    const vercelResult = spawnSync('vercel', ['deploy', '--prod'], {
        cwd: path.join(REPO_PATH, 'frontend'),
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'pipe']
    });
    
    if (vercelResult.status === 0) {
        console.log('[✓] Vercel deploy succeeded');
    } else {
        console.log('[!] Vercel deploy failed:', vercelResult.stderr.substring(0, 200));
    }
    
    // Try Railway
    console.log('\n[*] Deploying backend to Railway...');
    const railwayResult = spawnSync('railway', ['up'], {
        cwd: path.join(REPO_PATH, 'backend'),
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'pipe']
    });
    
    if (railwayResult.status === 0) {
        console.log('[✓] Railway deploy succeeded');
    } else {
        console.log('[!] Railway deploy failed:', railwayResult.stderr.substring(0, 200));
    }
} else {
    console.log('[!] GitHub push FAILED');
    console.log('Error:', pushResult.stderr.substring(0, 500));
}

console.log('\n[+] Deployment completed');
