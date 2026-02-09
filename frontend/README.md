# Fashion Photoshoot Studio - Frontend

## Quick Start

### Prerequisites
- Node.js 16+ & npm/yarn
- Firebase project created

### Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Update `.env` with your Firebase credentials

4. Run development server:
   ```bash
   npm run dev
   ```

Server will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

### Deployment to Vercel

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

## Project Structure

```
frontend/
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # Landing page
│   │   ├── +layout.svelte        # Main layout
│   │   ├── auth/
│   │   │   ├── login/+page.svelte
│   │   │   └── register/+page.svelte
│   │   ├── dashboard/+page.svelte
│   │   ├── create-shoot/+page.svelte
│   │   └── buy-credits/+page.svelte
│   └── lib/
│       ├── firebase.js           # Firebase authentication
│       ├── api.js                # Backend API wrapper
│       ├── stores.js             # Svelte stores
│       └── components/
│           ├── UploadArea.svelte
│           ├── GenerationLoading.svelte
│           └── ResultGallery.svelte
├── package.json
├── svelte.config.js
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VITE_FIREBASE_API_KEY` | Firebase API key |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase auth domain |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase storage bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase sender ID |
| `VITE_FIREBASE_APP_ID` | Firebase app ID |
| `VITE_BACKEND_URL` | Backend API URL (default: http://localhost:8000) |

## Features

- 🔐 Firebase Authentication (Google + Email)
- 📸 Drag & drop image upload
- ✨ Real-time generation preview
- 💳 Credit-based system
- 📱 Mobile responsive
- 🎨 Modern UI with Tailwind CSS

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
