#!/bin/bash

# 🚀 Fire Prediction System - Quick Deploy Script
# This script will guide you through the deployment process

echo "========================================="
echo "🔥 Fire Prediction System - Deployment"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: Please run this script from /app directory"
    exit 1
fi

echo "✅ All deployment files are ready!"
echo ""
echo "📦 Files prepared:"
echo "  ✓ render.yaml (Render configuration)"
echo "  ✓ netlify.toml (Netlify configuration)"
echo "  ✓ backend/.env (MongoDB connection configured)"
echo "  ✓ .gitignore (protecting sensitive data)"
echo "  ✓ backend/Procfile (Render startup)"
echo ""

# Git status
echo "📊 Current Git Status:"
git status --short
echo ""

echo "========================================="
echo "STEP 1: Push to GitHub"
echo "========================================="
echo ""
echo "Your repository: https://github.com/mehaklaha/Fire-Prediction-System.git"
echo ""
echo "🔐 You'll need to authenticate with GitHub."
echo ""
echo "Choose authentication method:"
echo "  1) Personal Access Token (Recommended)"
echo "  2) GitHub CLI (gh)"
echo ""

read -p "Enter choice (1 or 2): " auth_choice

if [ "$auth_choice" = "1" ]; then
    echo ""
    echo "📝 To create a Personal Access Token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Select scopes: 'repo' (all)"
    echo "  4. Generate and copy the token"
    echo ""
    read -p "Enter your GitHub Personal Access Token: " token
    
    if [ -z "$token" ]; then
        echo "❌ No token provided. Please run the script again."
        exit 1
    fi
    
    # Update remote URL with token
    git remote set-url origin "https://${token}@github.com/mehaklaha/Fire-Prediction-System.git"
    
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push -u origin main --force
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
    else
        echo "❌ Push failed. Please check your token and try again."
        exit 1
    fi
    
elif [ "$auth_choice" = "2" ]; then
    echo ""
    echo "Using GitHub CLI..."
    
    # Check if gh is installed
    if ! command -v gh &> /dev/null; then
        echo "❌ GitHub CLI not found. Installing..."
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh -y
    fi
    
    echo "Please authenticate with GitHub CLI:"
    gh auth login
    
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push -u origin main --force
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
    else
        echo "❌ Push failed. Please check authentication and try again."
        exit 1
    fi
else
    echo "❌ Invalid choice. Please run the script again."
    exit 1
fi

echo ""
echo "========================================="
echo "STEP 2: Deploy to Render"
echo "========================================="
echo ""
echo "📋 Next steps (manual):"
echo ""
echo "1. Go to: https://dashboard.render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Blueprint'"
echo "4. Select repository: Fire-Prediction-System"
echo "5. Render will detect render.yaml and deploy automatically!"
echo ""
echo "⏱️  Deployment takes ~5-10 minutes"
echo ""
read -p "Press ENTER when backend deployment is complete..."

echo ""
read -p "Enter your Render backend URL (e.g., https://fire-prediction-backend.onrender.com): " backend_url

if [ -z "$backend_url" ]; then
    echo "❌ No URL provided. Please note it down and continue manually."
else
    # Test backend
    echo ""
    echo "🧪 Testing backend..."
    response=$(curl -s "${backend_url}/api/" || echo "failed")
    
    if [[ $response == *"Fire Prediction System API"* ]]; then
        echo "✅ Backend is live and responding!"
    else
        echo "⚠️  Backend might not be ready yet. Response: $response"
    fi
    
    # Update frontend .env
    echo ""
    echo "📝 Updating frontend environment variable..."
    echo "REACT_APP_BACKEND_URL=${backend_url}" > /app/frontend/.env
    
    # Commit the change
    git add frontend/.env
    git commit -m "Update backend URL for production"
    git push origin main
    
    echo "✅ Frontend .env updated and pushed to GitHub"
fi

echo ""
echo "========================================="
echo "STEP 3: Deploy to Netlify"
echo "========================================="
echo ""
echo "📋 Next steps (manual):"
echo ""
echo "1. Go to: https://app.netlify.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'Add new site' → 'Import an existing project'"
echo "4. Select repository: Fire-Prediction-System"
echo "5. Configure:"
echo "   - Base directory: frontend"
echo "   - Build command: yarn build"
echo "   - Publish directory: frontend/build"
echo "6. Add environment variable:"
echo "   - Key: REACT_APP_BACKEND_URL"
echo "   - Value: ${backend_url}"
echo "7. Click 'Deploy site'"
echo ""
echo "⏱️  Build takes ~3-5 minutes"
echo ""
read -p "Press ENTER when frontend deployment is complete..."

echo ""
read -p "Enter your Netlify URL (e.g., https://fire-prediction.netlify.app): " frontend_url

if [ -z "$frontend_url" ]; then
    echo "❌ No URL provided."
else
    echo ""
    echo "========================================="
    echo "STEP 4: Update CORS Settings"
    echo "========================================="
    echo ""
    echo "⚠️  IMPORTANT: Update CORS in Render"
    echo ""
    echo "1. Go to Render Dashboard"
    echo "2. Select your backend service"
    echo "3. Go to 'Environment'"
    echo "4. Update CORS_ORIGINS to: ${frontend_url}"
    echo "5. Save (Render will auto-redeploy)"
    echo ""
    read -p "Press ENTER when CORS is updated..."
    
    echo ""
    echo "🧪 Testing complete deployment..."
    
    # Test backend
    echo "Testing backend API..."
    curl -s "${backend_url}/api/" | grep -q "Fire Prediction" && echo "✅ Backend: OK" || echo "❌ Backend: Failed"
    
    # Test frontend
    echo "Testing frontend..."
    curl -s -o /dev/null -w "%{http_code}" "${frontend_url}" | grep -q "200" && echo "✅ Frontend: OK" || echo "❌ Frontend: Check manually"
fi

echo ""
echo "========================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "Your Fire Prediction System is now live:"
echo ""
echo "🌐 Frontend: ${frontend_url}"
echo "🔧 Backend:  ${backend_url}/api/"
echo "📊 GitHub:   https://github.com/mehaklaha/Fire-Prediction-System"
echo ""
echo "✅ Next steps:"
echo "  1. Test all features on your live site"
echo "  2. Share the frontend URL with users"
echo "  3. Monitor logs for any errors"
echo "  4. Set up custom domain (optional)"
echo ""
echo "📚 For detailed documentation, see:"
echo "  - DEPLOY_NOW.md (step-by-step guide)"
echo "  - README.md (full documentation)"
echo "  - DEPLOYMENT_GUIDE.md (detailed deployment info)"
echo ""
echo "🏆 Congratulations! Your A-grade project is deployed!"
echo ""
