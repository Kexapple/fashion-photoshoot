# Architecture Overview

## System Design

The Fashion Photoshoot Studio is built on a modern, scalable architecture designed for 10+ users with room to grow.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
│          (SvelteKit App, Vercel CDN)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FIREBASE (Auth & Data)                          │
│  ├─ Authentication (Google, Email/Password)                │
│  ├─ Firestore: users, photoshoots, transactions            │
│  └─ Storage: uploaded-images, generated-images             │
└────────────────────────┬────────────────────────────────────┘
          │
          │ Admin SDK
          ▼
┌─────────────────────────────────────────────────────────────┐
│        PYTHON FASTAPI BACKEND (Railway/Render)              │
│  ├─ Auth validation (Firebase tokens)                      │
│  ├─ Credit system enforcement                              │
│  ├─ Image generation orchestration                         │
│  └─ Payment verification                                   │
└────────────────────────┬────────────────────────────────────┘
          │
          │ API calls
          ▼
┌─────────────────────────────────────────────────────────────┐
│  EXTERNAL SERVICES                                          │
│  ├─ Nano Banana API (image generation)                     │
│  ├─ JazzCash / EasyPaisa (payments)                        │
│  └─ Firebase Admin SDK                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### Frontend (SvelteKit + Tailwind CSS)

**Responsibilities:**
- User authentication UI (Google OAuth, Email/Password)
- Image upload and preview
- Generation form completion
- Results display and download
- Credit purchase interface

**Key Features:**
- Server-side validation of all requests
- Never modifies credits on frontend
- Responsive mobile design
- Real-time user feedback

**Deployment:** Vercel (free tier)

---

### Backend (FastAPI + Python)

**Responsibilities:**
- Firebase token validation
- Credit system enforcement
- Image generation request handling
- Payment verification
- Atomic credit deductions
- Image storage management

**Key Features:**
- Async request handling
- Transaction-based credit system
- Rate limiting per user
- Comprehensive error handling
- Mock services for testing

**Deployment:** Railway or Render

---

### Database (Firestore)

**Collections:**

```
users/{uid}
├─ email: string
├─ displayName: string
├─ credits: number
├─ plan: string
├─ firstLoginBonusUsed: boolean
├─ lastLoginAt: timestamp
└─ createdAt: timestamp

users/{uid}/transactions/{tx_id}
├─ type: string ("generation", "purchase", "signup_bonus")
├─ amount: number
├─ status: string
├─ timestamp: timestamp
└─ details: object

anonUsers/{ipHash}
├─ ipAddress: string
├─ generationCount: number
├─ firstGenerationAt: timestamp
├─ lastGenerationAt: timestamp
└─ status: string

photoshoots/{uid}/{shoot_id}
├─ articleType: string
├─ styleNotes: string
├─ imageSize: string
├─ uploadedImages: array
├─ generatedImages: array
├─ creditsCost: number
├─ isFreeTrial: boolean
├─ status: string
└─ createdAt: timestamp
```

---

### Storage (Firebase Storage)

```
Bucket Structure:
├─ uploaded-images/{uid}/{shoot_id}/
│  ├─ image-1.jpg
│  ├─ image-2.jpg
│  └─ ...
│
└─ generated-images/{uid}/{shoot_id}/
   ├─ image-1.jpg
   ├─ image-2.jpg
   └─ ...
```

---

## Credit System (Critical)

### Rules

1. **Anonymous Users:** 3 free generations per IP (lifetime)
2. **First Login:** 5 free credits (one-time)
3. **Generation Cost:** 1 credit per image
4. **Payment:** PKR 5 per credit (Pakistani methods: JazzCash, EasyPaisa)

### Atomic Deduction

Credit deductions use **Firestore transactions** to prevent race conditions:

```python
def deduct_credits(uid, amount, shoot_id):
    transaction = db.transaction()
    
    @transaction.transactional
    def transfer(txn):
        user_ref = db.collection('users').document(uid)
        user_doc = txn.get(user_ref)
        
        current = user_doc.get('credits')
        if current < amount:
            raise ValueError("Insufficient credits")
        
        # Atomic update
        txn.update(user_ref, {'credits': current - amount})
        txn.set(
            user_ref.collection('transactions').document(),
            {'type': 'generation', 'amount': amount, ...}
        )
    
    transaction(transfer)
```

---

## Data Flow Examples

### Example 1: Anonymous User (Free Trial)

```
1. User visits landing page
   └─ Frontend checks localStorage for free trial status
   
2. User selects free trial option
   └─ Frontend checks: generationCount < 3?
   
3. User uploads images & generates
   └─ POST /api/photoshoots/create (no idToken)
   └─ Backend extracts client IP
   └─ Backend checks anonUsers/{ipHash}.generationCount
   └─ If < 3: allow generation
   └─ Increment counter
   
4. Results returned
   └─ Frontend shows: "2/3 remaining"
   
5. User generates 3rd image
   └─ Counter reaches 3
   └─ Backend returns 402 on next attempt
   └─ Frontend prompts: "Login to continue"
```

---

### Example 2: Authenticated User (Credits)

```
1. User logs in via Google
   └─ Firebase Auth creates session
   └─ Frontend stores ID token
   
2. Backend receives /auth/register
   └─ Verifies token with Firebase Admin SDK
   └─ Creates users/{uid} document
   └─ Adds 5 credits automatically
   └─ Logs signup_bonus transaction
   
3. User navigates to /create-shoot
   └─ Frontend GET /api/user/credits?idToken=...
   └─ Backend verifies token, returns credit balance
   └─ Frontend displays: "You have 5 credits"
   
4. User generates photoshoot
   └─ POST /api/photoshoots/create with idToken
   └─ Backend verifies token → extract uid
   └─ Backend checks users/{uid}.credits
   └─ If < 1: return 402
   └─ If ≥ 1: call Nano Banana API
   └─ If success: atomically deduct credit
   └─ Return results + new balance (4)
   
5. User buys credits
   └─ Frontend POST /api/credits/purchase with idToken + payment info
   └─ Backend verifies JazzCash/EasyPaisa payment
   └─ If verified: add credits atomically
   └─ Log purchase transaction
```

---

## Security Considerations

1. **Token Validation:** Every endpoint validates Firebase ID token
2. **Credit Enforcement:** Server-side only. Frontend cannot be trusted.
3. **IP Hashing:** PII protection for anonymous user tracking
4. **Payment Verification:** Never trust frontend for payment status
5. **CORS:** Whitelist only frontend domains
6. **Rate Limiting:** Prevent abuse per user
7. **Error Messages:** No sensitive data in responses

---

## Scalability

Current design supports:
- ✅ 10-1000 users easily
- ✅ 100 concurrent users without optimization
- ✅ Simple horizontal scaling (add more backend instances)
- ✅ Firestore auto-scales
- ✅ Firebase Storage auto-scales

Future optimizations (if needed):
- Add Redis for session caching
- Implement request queuing (Celery)
- Add CDN for generated images
- Implement image compression pipeline
- Add analytics tracking

---

## Cost Breakdown (Monthly, ~100 users)

| Service | Cost | Notes |
|---------|------|-------|
| Firebase | $0-10 | Free tier covers 100K ops |
| Vercel | $0 | Free tier frontend |
| Railway | $5-20 | $5 minimum, ~20/GB outbound |
| AI API (Nano Banana) | $10-50 | Pay-per-use image generation |
| Custom Domain | $10-15 | Optional DNS |
| **Total** | **$25-95** | Scales linearly with users |

---

## Deployment Checklist

- [ ] Firebase project created
- [ ] Service account key downloaded
- [ ] Nano Banana API key obtained
- [ ] JazzCash/EasyPaisa merchants registered (optional)
- [ ] Backend pushed to Railway/Render
- [ ] Frontend pushed to Vercel
- [ ] Environment variables configured
- [ ] Custom domain setup (optional)
- [ ] SSL/HTTPS enabled (auto on Vercel/Railway)
- [ ] Database security rules configured
- [ ] Storage CORS rules configured
