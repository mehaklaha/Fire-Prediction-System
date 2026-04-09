# 🚀 Deployment Guide - Fire Prediction System

Complete step-by-step guide to deploy your Fire Prediction System to Render (Backend) and Netlify (Frontend).

## 📋 Prerequisites

- GitHub account
- Render account (https://render.com)
- Netlify account (https://netlify.com)
- MongoDB Atlas account (free tier available)

## 🗄️ Step 1: Setup MongoDB Atlas (Database)

1. **Create MongoDB Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up for free tier

2. **Create a Cluster**
   - Click "Build a Database"
   - Choose FREE tier (M0)
   - Select your preferred region (choose closest to your users)
   - Name your cluster (e.g., "fire-prediction-cluster")

3. **Create Database User**
   - Go to "Database Access"
   - Add new database user
   - Username: `fire_admin`
   - Password: Generate secure password (save it!)
   - Database User Privileges: Read and write to any database

4. **Configure Network Access**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Select "Allow Access from Anywhere" (0.0.0.0/0)
   - This is needed for Render to connect

5. **Get Connection String**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Format: `mongodb+srv://fire_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`
   - Replace `<password>` with your actual password
   - Save this for Render deployment

## 🔧 Step 2: Prepare Your Code for Deployment

1. **Update requirements.txt** (if needed)
   ```bash
   cd /app/backend
   pip freeze > requirements.txt
   ```

2. **Create Procfile for Render** (in `/app/backend/`)
   ```
   web: uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

3. **Ensure all environment variables are used** (already done)
   - Backend uses `MONGO_URL` and `DB_NAME`
   - Frontend uses `REACT_APP_BACKEND_URL`

## 🖥️ Step 3: Deploy Backend to Render

1. **Push Code to GitHub**
   - Create a new repository on GitHub
   - Push your code:
   ```bash
   cd /app
   git init
   git add .
   git commit -m "Initial commit - Fire Prediction System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/fire-prediction-system.git
   git push -u origin main
   ```

2. **Create New Web Service on Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository you just created

3. **Configure Web Service**
   - **Name**: `fire-prediction-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable"
   
   ```
   MONGO_URL = mongodb+srv://fire_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   DB_NAME = fire_prediction_db
   CORS_ORIGINS = *
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Once deployed, copy your backend URL
   - Format: `https://fire-prediction-backend.onrender.com`

6. **Test Backend**
   ```bash
   curl https://fire-prediction-backend.onrender.com/api/
   # Should return: {"message":"Fire Prediction System API","version":"1.0.0"}
   ```

## 🌐 Step 4: Deploy Frontend to Netlify

1. **Update Frontend Environment Variable**
   - Edit `/app/frontend/.env`
   ```
   REACT_APP_BACKEND_URL=https://fire-prediction-backend.onrender.com
   ```
   - Commit and push changes

2. **Create New Site on Netlify**
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Select your repository

3. **Configure Build Settings**
   - **Base directory**: `frontend`
   - **Build command**: `yarn build`
   - **Publish directory**: `frontend/build`
   
4. **Add Environment Variables**
   - Go to "Site settings" → "Build & deploy" → "Environment"
   - Add variable:
   ```
   REACT_APP_BACKEND_URL = https://fire-prediction-backend.onrender.com
   ```

5. **Deploy**
   - Click "Deploy site"
   - Wait for build (3-5 minutes)
   - Once deployed, you'll get a URL like: `https://YOUR-SITE-NAME.netlify.app`

6. **Update CORS on Backend**
   - Go back to Render dashboard
   - Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS = https://YOUR-SITE-NAME.netlify.app
   ```
   - Render will automatically redeploy

## ✅ Step 5: Verification

1. **Test Backend APIs**
   ```bash
   # Health check
   curl https://fire-prediction-backend.onrender.com/api/
   
   # Fire prediction
   curl -X POST https://fire-prediction-backend.onrender.com/api/predict \
     -H "Content-Type: application/json" \
     -d '{
       "latitude": 28.6139,
       "longitude": 77.2090,
       "wind_speed": 25.5,
       "vegetation_index": 0.25
     }'
   ```

2. **Test Frontend**
   - Visit `https://YOUR-SITE-NAME.netlify.app`
   - Should see the Fire Prediction Dashboard
   - Test fire prediction form
   - Check if map loads
   - Verify real-time updates in live feed

3. **Test WebSocket Connection**
   - Open browser DevTools → Console
   - Check for WebSocket connection messages
   - Should see "WebSocket connected" in console

## 🔍 Troubleshooting

### Backend Issues

**Problem**: Deployment fails on Render
- **Solution**: Check build logs, ensure all dependencies in requirements.txt

**Problem**: Database connection fails
- **Solution**: Verify MongoDB connection string, check Network Access settings in Atlas

**Problem**: API returns 500 errors
- **Solution**: Check Render logs: Dashboard → Logs

### Frontend Issues

**Problem**: Build fails on Netlify
- **Solution**: Check build logs, ensure all npm packages installed

**Problem**: "Failed to fetch" errors
- **Solution**: Verify `REACT_APP_BACKEND_URL` is correct, check CORS settings

**Problem**: Map doesn't load
- **Solution**: Check console for errors, verify Leaflet CSS is imported

## 🎯 Post-Deployment Optimization

1. **Custom Domain** (Optional)
   - Netlify: Site settings → Domain management → Add custom domain
   - Render: Settings → Custom Domains

2. **HTTPS/SSL**
   - Both Render and Netlify provide free SSL automatically

3. **Environment-Specific Settings**
   - Use different MongoDB databases for production/staging
   - Consider using environment-specific API keys

4. **Monitoring**
   - Render provides basic monitoring in dashboard
   - Netlify Analytics available (paid feature)

5. **CI/CD**
   - Both platforms auto-deploy on git push to main branch
   - Configure branch-specific deployments if needed

## 🔐 Security Best Practices

1. **Never commit sensitive data**
   - Keep `.env` files in `.gitignore`
   - Use environment variables on hosting platforms

2. **Rotate credentials periodically**
   - MongoDB passwords
   - API keys (when using real NASA FIRMS API)

3. **Monitor access**
   - Review MongoDB Atlas access logs
   - Monitor Render deployment logs

4. **Backup data**
   - MongoDB Atlas automatic backups (paid feature)
   - Export important prediction data regularly

## 📊 Monitoring & Logs

### Render Logs
```
Dashboard → Your Service → Logs
- View real-time application logs
- Check for errors and warnings
```

### MongoDB Atlas Monitoring
```
Atlas Dashboard → Metrics
- Database operations
- Connection statistics
- Performance metrics
```

### Netlify Deploy Logs
```
Site → Deploys → Deploy log
- Build process output
- Deployment status
```

## 🚨 Important Notes

1. **Free Tier Limitations**
   - Render free tier: Service may sleep after inactivity
   - MongoDB Atlas free tier: 512 MB storage
   - Netlify free tier: 100 GB bandwidth/month

2. **NASA FIRMS API Integration**
   - Currently using synthetic data
   - To use real data:
     - Register at https://firms.modaps.eosdis.nasa.gov/api/map_key
     - Add `FIRMS_MAP_KEY` to Render environment variables
     - Update `fetch_nasa_firms_data()` function in server.py

3. **Scaling Considerations**
   - For production: Consider paid tiers
   - Render: Upgrade to Standard instance for no sleep
   - MongoDB: Upgrade for more storage
   - Implement caching (Redis) for better performance

## ✨ Success Checklist

- [ ] MongoDB Atlas cluster created and accessible
- [ ] Backend deployed on Render successfully
- [ ] Backend API endpoints responding
- [ ] Frontend deployed on Netlify successfully
- [ ] Frontend loads and displays dashboard
- [ ] Fire prediction form working
- [ ] Map displaying India region correctly
- [ ] Live feed showing fire incidents
- [ ] Historical chart rendering data
- [ ] WebSocket connection established
- [ ] Report incident form working

## 🎉 You're Live!

Your Fire Prediction System is now deployed and accessible worldwide!

**Share your links:**
- Backend API: `https://fire-prediction-backend.onrender.com`
- Frontend App: `https://YOUR-SITE-NAME.netlify.app`

**Next Steps:**
- Share with friends and colleagues
- Gather user feedback
- Consider additional features (see README.md)
- Monitor usage and performance

---

Need help? Check the logs or consult the documentation for Render, Netlify, and MongoDB Atlas.
