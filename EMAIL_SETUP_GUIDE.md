# Email Setup Guide for AnNi AI

## 📧 SMTP Email Configuration

The AnNi AI platform now supports real email sending for:
- Email verification during registration
- Password reset requests
- Account notifications

## 🔧 Environment Variables Required

Add these environment variables to your deployment:

### **For Gmail SMTP:**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

### **For SendGrid SMTP:**
```bash
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
```

### **For Other SMTP Providers:**
```bash
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
FROM_EMAIL=noreply@yourdomain.com
```

## 🔐 Gmail Setup Instructions

### **Step 1: Enable 2-Factor Authentication**
1. Go to your Google Account settings
2. Security → 2-Step Verification
3. Turn on 2-Step Verification

### **Step 2: Generate App Password**
1. Go to Google Account → Security
2. 2-Step Verification → App passwords
3. Select app: "Mail"
4. Select device: "Other (custom name)"
5. Enter: "AnNi AI HR Platform"
6. Copy the generated 16-character password

### **Step 3: Configure Environment Variables**
Use the app password (not your regular Gmail password):
```bash
SMTP_USERNAME=your-gmail@gmail.com
SMTP_PASSWORD=abcd-efgh-ijkl-mnop  # 16-character app password
```

## 🚀 Render Deployment Setup

### **Add Environment Variables in Render:**
1. Go to your Render service dashboard
2. Environment → Add Environment Variable
3. Add each variable:
   - `SMTP_SERVER` = `smtp.gmail.com`
   - `SMTP_PORT` = `587`
   - `SMTP_USERNAME` = `your-email@gmail.com`
   - `SMTP_PASSWORD` = `your-app-password`
   - `FROM_EMAIL` = `your-email@gmail.com`

## 📧 Email Templates

The system sends professional HTML emails with:

### **Verification Email:**
- AnNi AI branding
- Clear call-to-action button
- Fallback link
- 24-hour expiration notice

### **Password Reset Email:**
- Security warnings
- Red-themed reset button
- 1-hour expiration notice
- Professional formatting

## 🔍 Testing Email Functionality

### **Test Registration:**
1. Create new account
2. Check email inbox for verification email
3. Click verification link
4. Account should be activated

### **Test Password Reset:**
1. Click "Forgot Password" on login
2. Enter email address
3. Check email inbox for reset email
4. Click reset link
5. Enter new password

## 🚨 Security Features

- **Token Expiration:** Verification (24h), Reset (1h)
- **One-time Use:** Tokens are cleared after use
- **Secure Generation:** Cryptographically secure tokens
- **No Information Disclosure:** Same response for valid/invalid emails

## 📋 Troubleshooting

### **Common Issues:**

**"SMTP credentials not configured"**
- Check environment variables are set correctly
- Verify variable names match exactly

**"Authentication failed"**
- For Gmail: Use app password, not regular password
- Verify 2FA is enabled for Gmail
- Check username/password are correct

**"Connection refused"**
- Check SMTP server and port
- Verify firewall settings
- Try different SMTP provider

**Emails not received:**
- Check spam/junk folder
- Verify email address is correct
- Check email service logs

## 🎯 Production Recommendations

1. **Use dedicated email service** (SendGrid, AWS SES, Mailgun)
2. **Set up SPF/DKIM records** for better deliverability
3. **Monitor email delivery rates**
4. **Implement email bounce handling**
5. **Use professional from address** (noreply@yourdomain.com)

## 📞 Support

If you encounter issues with email setup:
1. Check the Render deployment logs
2. Verify environment variables
3. Test with a simple email service first
4. Contact support if issues persist

