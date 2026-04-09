# 🚀 Deploy Backend to Render - Manual Setup (FREE)

## Step-by-Step Instructions for "New Web Service"

### 1️⃣ Open Render Dashboard
👉 https://dashboard.render.com
- Sign in with GitHub

### 2️⃣ Create New Web Service
1. Click **"New +"** (top right corner)
2. Select **"Web Service"** (not Blueprint)
3. You'll see "Create a new Web Service" page

### 3️⃣ Connect Repository
1. You'll see a list of your GitHub repositories
2. Find **"Fire-Prediction-System"**
3. Click **"Connect"** button next to it

### 4️⃣ Configure Web Service Settings

Fill in these details EXACTLY:

#### Basic Settings:
```
Name: fire-prediction-backend
```
(You can choose any name, but this is recommended)

```
Region: Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
```

```
Branch: main
```

#### Build Settings:

**Root Directory:**
```
backend
```
⚠️ IMPORTANT: Type exactly "backend" (this tells Render where your code is)

**Runtime:**
```
Python 3
```
(Select from dropdown)

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn server:app --host 0.0.0.0 --port $PORT
```

#### Instance Type:
```
Free
```
⚠️ Select "Free" - no credit card needed!

### 5️⃣ Add Environment Variables

Scroll down to **"Environment Variables"** section

Click **"Add Environment Variable"** and add these THREE variables:

**Variable 1:**
```
Key: MONGO_URL
Value: mongodb+srv://fire_admin:mehak%405304@fire-prediction-cluster.a5xulg0.mongodb.net/?appName=fire-prediction-cluster
```

**Variable 2:**
```
Key: DB_NAME
Value: fire_prediction_db
```

**Variable 3:**
```
Key: CORS_ORIGINS
Value: *
```
(We'll update this later with your Netlify URL)

### 6️⃣ Advanced Settings (Optional - Leave Default)

You can skip these, but if you see them:
- Auto-Deploy: Yes (enabled)
- Health Check Path: /api/

### 7️⃣ Create Web Service

1. Scroll to bottom
2. Click **"Create Web Service"** (blue button)

### 8️⃣ Wait for Deployment

- You'll see build logs appearing
- Status will show "Building..." then "Deploying..."
- Wait for green "Live" status (~5-10 minutes)
- Don't close the page!

### 9️⃣ Get Your Backend URL

Once it shows **"Live"**:
1. Look at the top of the page
2. You'll see your URL like: `https://fire-prediction-backend-xxxx.onrender.com`
3. **COPY THIS URL** - you'll need it for Netlify!

### 🧪 Test Your Backend

Click on your URL and add `/api/` at the end:
```
https://YOUR-BACKEND-URL.onrender.com/api/
```

You should see:
```json
{"message":"Fire Prediction System API","version":"1.0.0"}
```

If you see this ✅ - Backend is working perfectly!

---

## 📋 Quick Reference - Copy & Paste

Here are all the values you need (copy these):

```
Name: fire-prediction-backend
Region: (choose closest)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
Instance Type: Free

Environment Variables:
MONGO_URL = mongodb+srv://fire_admin:mehak%405304@fire-prediction-cluster.a5xulg0.mongodb.net/?appName=fire-prediction-cluster
DB_NAME = fire_prediction_db
CORS_ORIGINS = *
```

---

## 🆘 Common Issues

**Problem: Build fails**
- Check that "Root Directory" is set to "backend"
- Check build logs for specific error

**Problem: Can't find repository**
- Make sure you signed in with GitHub
- Click "Configure account" to grant Render access

**Problem: Environment variables not saving**
- Make sure you click "Add" after entering each variable
- All three variables must be added

---

## ✅ What's Next?

Once your backend shows "Live":
1. Copy your backend URL
2. Test it by visiting: `https://YOUR-URL.onrender.com/api/`
3. Come back here with your URL
4. I'll help you deploy the frontend to Netlify!

---

**Need help? Just let me know what screen you're on!** 🙋‍♂️
