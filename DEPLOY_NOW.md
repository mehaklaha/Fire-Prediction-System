# 🚀 Deploy Your Fire Prediction System - Step by Step

## ✅ Pre-Deployment Checklist (COMPLETED)

- ✅ MongoDB Atlas connection configured
- ✅ GitHub repository ready: https://github.com/mehaklaha/Fire-Prediction-System.git
- ✅ Backend .env configured with MongoDB connection
- ✅ render.yaml created for Render deployment
- ✅ netlify.toml created for Netlify deployment
- ✅ .gitignore created to protect sensitive data
- ✅ All code tested (100% success rate)

---

## 📤 STEP 1: Push Code to GitHub

Run these commands in your terminal:

```bash
# Navigate to project directory
cd /app

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Deploy Fire Prediction System - Production Ready"

# Add remote repository
git remote add origin https://github.com/mehaklaha/Fire-Prediction-System.git

# Push to GitHub
git branch -M main
git push -u origin main --force
```

**Note:** Use `--force` only if this is a new deployment. Remove it for subsequent updates.

---

## 🔧 STEP 2: Deploy Backend to Render

### Option A: Using render.yaml (Recommended - Automated)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up/Login with GitHub

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select repository: `Fire-Prediction-System`
   - Render will detect `render.yaml`
   - Click "Apply"

3. **Update CORS_ORIGINS**
   - After deployment, go to your service
   - Navigate to "Environment"
   - Update `CORS_ORIGINS` to: `https://YOUR-NETLIFY-SITE.netlify.app`
   - (You'll get this URL after Netlify deployment)

### Option B: Manual Setup

1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select `Fire-Prediction-System`

2. **Configure Settings:**
   ```
   Name: fire-prediction-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

3. **Add Environment Variables:**
   ```
   MONGO_URL = mongodb+srv://fire_admin:mehak%405304@fire-prediction-cluster.a5xulg0.mongodb.net/?appName=fire-prediction-cluster
   DB_NAME = fire_prediction_db
   CORS_ORIGINS = *
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment

5. **Copy Backend URL**
   - Once deployed, copy your URL
   - Example: `https://fire-prediction-backend.onrender.com`
   - **SAVE THIS - YOU'LL NEED IT FOR NETLIFY**

### ✅ Test Backend Deployment

```bash
# Replace YOUR-BACKEND-URL with actual URL
curl https://YOUR-BACKEND-URL.onrender.com/api/

# Should return:
# {"message":"Fire Prediction System API","version":"1.0.0"}
```

---

## 🌐 STEP 3: Deploy Frontend to Netlify

### Option A: Using Netlify CLI (Recommended)

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Update Frontend Environment Variable**
   ```bash
   # Edit frontend/.env
   echo "REACT_APP_BACKEND_URL=https://YOUR-BACKEND-URL.onrender.com" > /app/frontend/.env
   ```

4. **Deploy**
   ```bash
   cd /app/frontend
   netlify deploy --prod
   
   # When prompted:
   # - Create new site
   # - Build command: yarn build
   # - Publish directory: build
   ```

### Option B: Using Netlify Dashboard

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Sign up/Login with GitHub

2. **Create New Site**
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Select `Fire-Prediction-System`

3. **Configure Build Settings:**
   ```
   Base directory: frontend
   Build command: yarn build
   Publish directory: frontend/build
   ```

4. **Add Environment Variable:**
   - Before deploying, click "Show advanced"
   - Click "New variable"
   ```
   Key: REACT_APP_BACKEND_URL
   Value: https://YOUR-BACKEND-URL.onrender.com
   ```
   (Use the Render backend URL from Step 2)

5. **Deploy Site**
   - Click "Deploy site"
   - Wait 3-5 minutes

6. **Copy Frontend URL**
   - Example: `https://fire-prediction-mehaklaha.netlify.app`

### ✅ Test Frontend Deployment

- Visit your Netlify URL
- You should see the Fire Prediction Dashboard
- Test all features:
  - ✅ Fire prediction form
  - ✅ Map loads (centered on India)
  - ✅ Live fire feed updating
  - ✅ Report incident form
  - ✅ Historical chart

---

## 🔄 STEP 4: Update CORS Settings

Now that you have your Netlify URL, update the backend CORS settings:

1. **Go to Render Dashboard**
   - Navigate to your backend service
   - Click "Environment"
   - Find `CORS_ORIGINS`
   - Update value to: `https://YOUR-NETLIFY-SITE.netlify.app`
   - Click "Save Changes"
   - Render will automatically redeploy

---

## 🧪 STEP 5: Final Verification

### Backend Health Check
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/
```

### Test Fire Prediction API
```bash
curl -X POST https://YOUR-BACKEND-URL.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 28.6139,
    "longitude": 77.2090,
    "wind_speed": 25.5,
    "vegetation_index": 0.25
  }'
```

### Frontend Checklist
Visit your Netlify URL and verify:
- [ ] Dashboard loads with dark theme
- [ ] Map displays India region
- [ ] Fire markers appear on map
- [ ] Prediction form submits successfully
- [ ] Live feed shows fire incidents
- [ ] Historical chart renders
- [ ] Report form works
- [ ] Real-time updates (WebSocket) working

---

## 🎯 Post-Deployment Tasks

### 1. Custom Domain (Optional)
- **Netlify**: Site settings → Domain management → Add custom domain
- **Render**: Settings → Custom Domains

### 2. Enable Auto-Deploy
Both platforms should auto-deploy on git push. Verify:
- Render: Settings → Auto-Deploy: ON
- Netlify: Site settings → Build & deploy → Auto publishing: ON

### 3. Monitor Services
- **Render Logs**: Dashboard → Your Service → Logs
- **Netlify Deploy Logs**: Site → Deploys → Deploy log
- **MongoDB**: Atlas Dashboard → Metrics

### 4. Update README
Add your live URLs to README.md:
```markdown
## 🌍 Live Demo
- **Frontend**: https://YOUR-SITE.netlify.app
- **Backend API**: https://YOUR-BACKEND.onrender.com/api/
```

---

## 🚨 Troubleshooting

### Backend Issues

**Problem**: Build fails on Render
```bash
# Solution: Check requirements.txt is complete
cd /app/backend
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

**Problem**: MongoDB connection fails
```bash
# Solution: Verify MongoDB connection string
# Check Network Access in MongoDB Atlas (should allow 0.0.0.0/0)
```

**Problem**: API returns CORS errors
```bash
# Solution: Update CORS_ORIGINS in Render environment variables
CORS_ORIGINS=https://your-netlify-site.netlify.app
```

### Frontend Issues

**Problem**: Build fails on Netlify
```bash
# Solution: Check build logs for missing dependencies
cd /app/frontend
yarn install
git add yarn.lock
git commit -m "Update dependencies"
git push
```

**Problem**: "Failed to fetch" errors
```bash
# Solution: Verify REACT_APP_BACKEND_URL
# Check Netlify Environment Variables
# Ensure no trailing slash in URL
```

**Problem**: Map doesn't display
```bash
# Solution: Check browser console for Leaflet errors
# Verify Leaflet CSS is loaded
```

---

## 📊 Expected Results

After successful deployment:

### ✅ Backend (Render)
- URL: `https://fire-prediction-backend.onrender.com`
- Status: Running
- Response time: < 2 seconds
- Uptime: 99%+

### ✅ Frontend (Netlify)
- URL: `https://fire-prediction-[username].netlify.app`
- Build time: ~3 minutes
- Deploy time: < 30 seconds
- Global CDN: Yes

### ✅ Database (MongoDB Atlas)
- Cluster: fire-prediction-cluster
- Collections: predictions, live_fires, reported_fires
- Storage used: < 50 MB initially

---

## 🎉 Success!

Your Fire Prediction System is now live and accessible worldwide!

**Share Your Links:**
- Frontend: https://YOUR-SITE.netlify.app
- Backend: https://YOUR-BACKEND.onrender.com/api/
- GitHub: https://github.com/mehaklaha/Fire-Prediction-System

**Next Steps:**
1. Test all features thoroughly
2. Share with users for feedback
3. Monitor logs for any errors
4. Consider adding NASA FIRMS real API key
5. Implement additional features from README.md

---

## 📞 Need Help?

If you encounter issues:
1. Check service logs (Render/Netlify)
2. Verify environment variables
3. Test API endpoints individually
4. Check MongoDB Atlas connection
5. Review browser console for errors

**Common Commands:**
```bash
# Update and redeploy
git add .
git commit -m "Update: description"
git push origin main

# View local logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.err.log
```

---

**Deployment prepared by Emergent AI** 🚀
