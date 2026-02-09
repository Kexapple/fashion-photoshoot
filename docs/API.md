# API Endpoints Reference

## Base URL
- **Development:** `http://localhost:8000`
- **Production:** `https://your-backend-domain.railway.app`

---

## Authentication Routes

### POST /api/auth/verify
Verify Firebase ID token

**Request:**
```json
{
  "idToken": "firebase-id-token-string"
}
```

**Response (200):**
```json
{
  "valid": true,
  "uid": "user-id",
  "email": "user@example.com",
  "displayName": "User Name"
}
```

**Errors:**
- `401` Invalid or expired token

---

### POST /api/auth/register
Register new user after Firebase authentication (gets first-login bonus)

**Request:**
```json
{
  "idToken": "firebase-id-token",
  "email": "user@example.com",
  "displayName": "User Name",
  "ipAddress": "192.168.1.1" (optional)
}
```

**Response (200):**
```json
{
  "status": "registered",
  "uid": "user-id",
  "email": "user@example.com",
  "displayName": "User Name",
  "credits": 5,
  "firstLoginBonusUsed": true,
  "message": "Welcome! You received 5 free credits."
}
```

**Or if user exists:**
```json
{
  "status": "user_exists",
  "credits": 5,
  "firstLoginBonusUsed": true
}
```

**Errors:**
- `401` Invalid token
- `500` Registration failed

---

### GET /api/auth/user/profile
Get user profile information

**Query Parameters:**
- `id_token` (string) - Firebase ID token

**Response (200):**
```json
{
  "uid": "user-id",
  "email": "user@example.com",
  "displayName": "User Name",
  "credits": 5,
  "plan": "free",
  "firstLoginBonusUsed": true,
  "createdAt": "2026-02-09T10:30:00Z"
}
```

**Errors:**
- `401` Invalid token
- `404` User not found

---

## Generation Routes

### POST /api/photoshoots/create
Generate photoshoot images

**Request:**
```json
{
  "idToken": "firebase-id-token OR empty for anonymous",
  "articleType": "shirt",
  "styleNotes": "casual, vibrant",
  "imageSize": "medium",
  "uploadedImageUrls": ["url1", "url2", "url3"],
  "clientIp": "192.168.1.1"
}
```

**Response (200):**
```json
{
  "shoot_id": "uuid",
  "status": "completed",
  "generatedImages": [
    "https://...",
    "https://...",
    "https://..."
  ],
  "creditsCost": 1,
  "creditsRemaining": 4
}
```

**Errors:**
- `400` Bad request (missing fields)
- `401` Invalid token
- `402` Insufficient credits (authenticated) or trial exhausted (anonymous)
- `500` Generation failed

---

## Credits Routes

### GET /api/user/credits
Get user's current credit balance

**Query Parameters:**
- `id_token` (string) - Firebase ID token

**Response (200):**
```json
{
  "credits": 5,
  "plan": "free",
  "firstLoginBonusUsed": true,
  "anonTrialRemaining": null
}
```

**Errors:**
- `401` Invalid token
- `404` User not found

---

### GET /api/anon/trial-status
Get anonymous user's free trial status

**Response (200):**
```json
{
  "eligible": true,
  "generationCount": 1,
  "remaining": 2,
  "totalLimit": 3,
  "status": "eligible"
}
```

**Note:** No authentication required. Uses client IP.

---

### POST /api/credits/purchase
Purchase credits via JazzCash or EasyPaisa

**Request:**
```json
{
  "idToken": "firebase-id-token",
  "amount": 50,
  "paymentMethod": "jazzcash", // or "easypaisa"
  "phoneNumber": "+92xxxxxxxxxx",
  "transactionId": "payment-provider-tx-id"
}
```

**Response (200):**
```json
{
  "status": "success",
  "creditsAdded": 50,
  "newBalance": 55,
  "transactionId": "tx-123",
  "message": "Successfully added 50 credits to your account"
}
```

**Errors:**
- `401` Invalid token
- `400` Invalid payment method
- `402` Payment verification failed
- `500` Failed to process credits

---

### GET /api/credits/packages
Get available credit purchase packages

**Response (200):**
```json
{
  "packages": [
    {
      "id": "pkg_10",
      "credits": 10,
      "priceInPkr": 50,
      "savings": 0,
      "featured": false
    },
    {
      "id": "pkg_25",
      "credits": 25,
      "priceInPkr": 125,
      "savings": 0,
      "featured": true
    },
    {
      "id": "pkg_50",
      "credits": 50,
      "priceInPkr": 250,
      "savings": 0,
      "featured": false
    },
    {
      "id": "pkg_100",
      "credits": 100,
      "priceInPkr": 500,
      "savings": 0,
      "featured": false
    }
  ]
}
```

---

## Health Check

### GET /health
Check API status

**Response (200):**
```json
{
  "status": "ok",
  "service": "fashion-photoshoot-api"
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message",
  "code": "ERROR_CODE",
  "status_code": 400
}
```

---

## Authentication

All endpoints requiring authentication use Firebase ID tokens.

**How to get token (Frontend):**
```javascript
const token = await currentUser.getIdToken();
```

**Pass token in request:**
- Via request body: `{"idToken": "token"}`
- Via query parameter: `?id_token=token`

---

## Rate Limiting

- **Per User:** 10 requests/minute
- **Anonymous:** 3 generations per IP (lifetime)
- **Authenticated Generation:** No limit (controlled by credits)

---

## Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Bad request (missing/invalid fields) |
| `401` | Unauthorized (invalid/expired token) |
| `402` | Insufficient credits or trial exhausted |
| `404` | Resource not found |
| `429` | Rate limit exceeded |
| `500` | Server error |

---

## Examples

### Example: Complete Generation Flow

```bash
# 1. User logs in (Firebase handles this)
# Token obtained: "eyJ..."

# 2. Register/check user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "idToken": "eyJ...",
    "email": "user@example.com",
    "displayName": "User"
  }'

# Response: User created with 5 credits

# 3. Check credit balance
curl -X GET "http://localhost:8000/api/user/credits?id_token=eyJ..."

# Response: {"credits": 5, ...}

# 4. Generate photoshoot
curl -X POST http://localhost:8000/api/photoshoots/create \
  -H "Content-Type: application/json" \
  -d '{
    "idToken": "eyJ...",
    "articleType": "shirt",
    "styleNotes": "casual",
    "imageSize": "medium",
    "uploadedImageUrls": ["https://..."]
  }'

# Response: Generated images with creditsRemaining: 4

# 5. Buy more credits
curl -X POST http://localhost:8000/api/credits/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "idToken": "eyJ...",
    "amount": 50,
    "paymentMethod": "jazzcash",
    "phoneNumber": "+92xxxxxxxxxx",
    "transactionId": "JZ123456"
  }'

# Response: Credits added, newBalance: 54
```

---

## Testing Endpoints

For local testing without full Firebase setup, use:

```bash
# Health check
curl http://localhost:8000/health

# Get credit packages (no auth needed)
curl http://localhost:8000/api/credits/packages

# Check anon trial status (no auth needed)
curl http://localhost:8000/api/anon/trial-status
```
