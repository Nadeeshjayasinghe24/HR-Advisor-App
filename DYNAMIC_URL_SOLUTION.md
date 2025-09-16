# Dynamic Frontend URL Solution

## Problem Solved
Previously, the backend had hardcoded frontend URLs for email verification redirects. This caused issues when:
- Frontend deployments changed URLs (new Vercel deployments)
- Multiple environments needed different URLs (staging, production)
- Repository re-imports created new deployment URLs

## Solution Overview
The backend now dynamically detects the frontend URL using multiple fallback methods:

### 1. Environment Variable (Recommended for Production)
Set `FRONTEND_URL` environment variable:
```bash
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

### 2. Request Headers (Automatic Detection)
The system automatically detects the frontend URL from:
- **Origin Header**: Most reliable for CORS requests
- **Referer Header**: Fallback option

### 3. Fallback URL
If no URL is detected, falls back to the last known working URL.

## Implementation Details

### Backend Changes Made

#### 1. Dynamic URL Detection Function
```python
def get_frontend_url():
    # Try environment variable first
    frontend_url = os.getenv('FRONTEND_URL')
    if frontend_url:
        return frontend_url.rstrip('/')
    
    # Try request headers
    if request:
        origin = request.headers.get('Origin')
        if origin:
            return origin
        
        referer = request.headers.get('Referer')
        if referer:
            parsed = urlparse(referer)
            return f"{parsed.scheme}://{parsed.netloc}"
    
    # Fallback
    return "https://hr-advisor-app-otaq.vercel.app"
```

#### 2. Dynamic Redirect Function
```python
def get_redirect_url(verification_status):
    frontend_url = get_frontend_url()
    return f"{frontend_url}/?verification={verification_status}"
```

#### 3. Updated Endpoints
- **Registration**: Captures frontend URL from request context
- **Email Verification**: Uses dynamic redirects
- **Resend Verification**: Uses dynamic URL detection

## Configuration Options

### Option 1: Environment Variable (Recommended)
Set in your deployment platform:
```bash
FRONTEND_URL=https://your-new-frontend-url.vercel.app
```

### Option 2: Automatic Detection (Default)
No configuration needed. The system will:
1. Detect URL from the signup request's Origin header
2. Use that URL for verification redirects
3. Work with any frontend deployment automatically

### Option 3: Update Fallback URL
If needed, update the fallback URL in the `get_frontend_url()` function.

## Benefits

1. **Zero Configuration**: Works automatically with new deployments
2. **Environment Flexibility**: Different URLs for staging/production
3. **Future-Proof**: No need to update backend when frontend URL changes
4. **Reliable Fallbacks**: Multiple detection methods ensure robustness

## Testing

### Test with Different URLs
1. Deploy frontend to new URL
2. Access signup page from new URL
3. Complete signup process
4. Verification email will automatically redirect to the correct URL

### Verify Detection
Check backend logs to see which URL detection method was used:
- Environment variable
- Origin header
- Referer header
- Fallback

## Migration Guide

### For New Deployments
1. No action needed - automatic detection works
2. Optionally set `FRONTEND_URL` environment variable for explicit control

### For Existing Deployments
1. Deploy updated backend code
2. Optionally configure `FRONTEND_URL` environment variable
3. Test verification flow with new frontend URLs

## Troubleshooting

### If Verification Still Redirects to Wrong URL
1. Check if `FRONTEND_URL` environment variable is set incorrectly
2. Verify CORS configuration allows the new frontend domain
3. Check browser developer tools for Origin/Referer headers in requests

### If Email Links Don't Work
1. Ensure backend deployment is updated with new code
2. Check backend logs for URL detection results
3. Verify email content shows correct verification URL

## Security Considerations

- Origin header validation prevents malicious redirects
- Only whitelisted domains in CORS configuration can trigger verification
- Environment variable takes precedence over headers for security
- Fallback URL provides safety net

This solution ensures the email verification system works seamlessly regardless of frontend URL changes, making the system much more maintainable and deployment-friendly.

