# Render Deployment Instructions

## 🚀 **Fix for "Application Exited Early" Error**

The current deployment is failing because Render is using the wrong start command. Here's how to fix it:

## ⚠️ **Current Issue:**

**Current Start Command:** `cd backend && python src/main.py`
**Problem:** This starts the Flask development server and then exits
**Result:** "Application exited early" error

## ✅ **Solution: Update Render Start Command**

### **Step 1: Go to Render Service Settings**
1. **Visit:** https://dashboard.render.com
2. **Find your HR backend service**
3. **Click on the service name**
4. **Go to "Settings" tab**

### **Step 2: Update Start Command**
1. **Find "Start Command" field**
2. **Replace current command with:**
   ```bash
   cd backend && gunicorn --config gunicorn_config.py src.main:app
   ```

### **Step 3: Save and Deploy**
1. **Click "Save Changes"**
2. **Render will automatically redeploy**
3. **Wait 3-5 minutes for deployment**

## 🔧 **Alternative Start Commands (if needed):**

### **Option 1: With explicit port binding**
```bash
cd backend && gunicorn --config gunicorn_config.py --bind 0.0.0.0:$PORT src.main:app
```

### **Option 2: Simple Gunicorn (no config file)**
```bash
cd backend && gunicorn --bind 0.0.0.0:$PORT --workers 2 src.main:app
```

### **Option 3: Fallback to Flask (temporary)**
```bash
cd backend && FLASK_ENV=production python src/main.py
```

## 📋 **Expected Results After Fix:**

### **✅ Successful Deployment:**
- **No "Application exited early" error**
- **Gunicorn starts properly**
- **Production-grade server running**
- **All API endpoints accessible**
- **No development server warnings**

### **🔍 Deployment Logs Should Show:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 1234
```

## 🚨 **Important Notes:**

### **Build Command (Keep Unchanged):**
```bash
cd backend && pip install -r requirements.txt
```

### **Environment Variables (Add if missing):**
```bash
FLASK_ENV=production
PORT=5000  # Render sets this automatically
```

### **File Structure (Verify):**
```
backend/
├── gunicorn_config.py  ← Must exist
├── requirements.txt    ← Must include gunicorn==21.2.0
├── src/
│   └── main.py        ← Flask app with 'app' variable
└── start.sh           ← Optional startup script
```

## 🔧 **Troubleshooting:**

### **If Gunicorn fails to start:**
1. **Check requirements.txt** includes `gunicorn==21.2.0`
2. **Verify gunicorn_config.py** exists in backend directory
3. **Check main.py** exports Flask app as `app` variable
4. **Try Option 2** (simple Gunicorn without config)

### **If still getting errors:**
1. **Check Render logs** for specific error messages
2. **Try Option 3** (Flask fallback) temporarily
3. **Verify all environment variables** are set correctly

## 🎯 **Why This Fixes the Issue:**

### **Before (Broken):**
- **Start Command:** `python src/main.py`
- **Result:** Flask dev server starts and exits
- **Status:** Application exited early

### **After (Fixed):**
- **Start Command:** `gunicorn --config gunicorn_config.py src.main:app`
- **Result:** Gunicorn production server starts and stays running
- **Status:** Production server running successfully

**Once you update the start command, your AnNi AI platform will be running on a production-grade server!** 🚀

