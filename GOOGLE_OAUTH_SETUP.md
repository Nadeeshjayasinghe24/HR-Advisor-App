# Google OAuth Setup Instructions

To enable Google Sign-up functionality, you need to set up Google OAuth credentials.

## Step 1: Create Google OAuth Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create or Select a Project**
   - Click "Select a project" → "New Project"
   - Name: "HR Advisor App" (or any name you prefer)
   - Click "Create"

3. **Enable Google+ API**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click on it and press "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Name: "HR Advisor Web Client"

5. **Configure Authorized Origins**
   Add these to "Authorized JavaScript origins":
   - `http://localhost:5173` (for development)
   - `https://your-frontend-domain.com` (your deployed frontend URL)

6. **Configure Redirect URIs**
   Add these to "Authorized redirect URIs":
   - `http://localhost:5173` (for development)
   - `https://your-frontend-domain.com` (your deployed frontend URL)

7. **Get Your Client ID**
   - After creating, copy the "Client ID"
   - It will look like: `123456789-abcdefg.apps.googleusercontent.com`

## Step 2: Configure Frontend Environment

1. **Create .env file in frontend directory**
   ```bash
   cp frontend/.env.example frontend/.env
   ```

2. **Update the .env file**
   ```
   VITE_API_URL=https://hr-advisor-app.onrender.com
   VITE_GOOGLE_CLIENT_ID=your_actual_client_id_here.apps.googleusercontent.com
   ```

3. **Replace `your_actual_client_id_here` with your real Client ID**

## Step 3: Deploy Frontend

After setting up the environment variables:

1. **Redeploy your frontend** on Vercel/Netlify
2. **Add the environment variable** in your hosting platform:
   - Variable: `VITE_GOOGLE_CLIENT_ID`
   - Value: Your Google Client ID

## Step 4: Test Google Sign-up

1. Go to your deployed frontend
2. Click "Sign up"
3. Click "Sign up with Google"
4. Complete the Google OAuth flow
5. You should be automatically logged in

## Troubleshooting

### "Google OAuth not loaded" Error
- Make sure the Google script is loaded in index.html
- Check browser console for any script loading errors

### "Invalid Client ID" Error
- Verify your Client ID is correct in the .env file
- Make sure your domain is added to authorized origins

### "Redirect URI Mismatch" Error
- Add your exact frontend URL to authorized redirect URIs
- Include both HTTP and HTTPS if needed

### Backend Errors
- Check that the `/api/auth/google` endpoint is working
- Verify the backend can create users with Google data

## Security Notes

- ✅ **DO** keep your Client ID in environment variables
- ✅ **DO** restrict authorized origins to your actual domains
- ❌ **DON'T** commit .env files to version control
- ❌ **DON'T** use the same credentials for development and production

---

Once set up, users will be able to sign up with Google and automatically get logged into your HR Advisor platform! 🚀

