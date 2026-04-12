# Fire Prediction System - PRD

## Original Problem Statement
Build a fire prediction system where we give the coordinates of longitude, latitude, wind speed and vegetation index and it predicts fire from a dataset. The backend should be a FastAPI backend on swagger deployed on Render and the frontend should be a React build deployed on Netlify. The frontend dashboard should look creative with real-time geospatial map of India, fire incident reporting, and live fire incidents display.

## Architecture
- **Backend**: FastAPI (Python) on Render - https://fire-prediction-system.onrender.com
- **Frontend**: React on Netlify - https://69db5f9e4488279471f2d254--infernoforecastpro.netlify.app
- **Database**: MongoDB Atlas (fire-prediction-cluster)
- **ML Model**: Random Forest Classifier (scikit-learn)
- **Map**: React-Leaflet with CartoDB Dark Matter tiles
- **Charts**: Recharts
- **Real-time**: WebSocket

## User Personas
- **Fire Department Officers**: Monitor live fire incidents, report new fires
- **Environmental Researchers**: Predict fire risks based on environmental data
- **Emergency Responders**: View real-time fire data on geospatial map
- **Government Officials**: Track historical fire trends

## Core Requirements (Static)
1. Fire risk prediction using ML model (latitude, longitude, wind speed, vegetation index)
2. Real-time geospatial map of India with live fire markers
3. Fire incident reporting system
4. Live fire incidents feed with WebSocket updates
5. Historical fire data visualization
6. Dark theme dashboard (Red/Blue/Black)

## What's Been Implemented (April 2026)
- [x] FastAPI backend with Random Forest fire prediction model
- [x] MongoDB Atlas integration with SSL/TLS
- [x] Fire prediction API endpoint (/api/predict)
- [x] Report fire incident API (/api/report-fire)
- [x] Live fires API (/api/fires/live)
- [x] Historical data API (/api/fires/historical)
- [x] WebSocket real-time updates (/api/ws/fires)
- [x] Background task for synthetic fire data generation
- [x] React dashboard with bento grid layout
- [x] Interactive Leaflet map centered on India
- [x] Fire prediction form with result display
- [x] Report incident form
- [x] Live feed with real-time updates
- [x] Historical chart with bar/line toggle
- [x] Dark command center theme (Chivo + JetBrains Mono fonts)
- [x] Deployed to Render (backend) and Netlify (frontend)
- [x] MongoDB Atlas with 0.0.0.0/0 network access
- [x] CORS configured for Netlify domain

## Live URLs
- Frontend: https://69db5f9e4488279471f2d254--infernoforecastpro.netlify.app
- Backend: https://fire-prediction-system.onrender.com
- GitHub: https://github.com/mehaklaha/Fire-Prediction-System

## Prioritized Backlog
### P0 (Critical)
- [x] All core features implemented and deployed

### P1 (High)
- [ ] Integrate real NASA FIRMS API (requires MAP_KEY)
- [ ] Train ML model with actual Kaggle fire dataset
- [ ] Add user authentication

### P2 (Medium)
- [ ] Email/SMS alerts for high-risk predictions
- [ ] Custom domain setup (Netlify + Render)
- [ ] Advanced ML models (XGBoost, Neural Network)
- [ ] User prediction history

### P3 (Low)
- [ ] Mobile responsive improvements
- [ ] Multi-region support (beyond India)
- [ ] Weather data integration
- [ ] Satellite imagery overlay
- [ ] Export reports as PDF

## Next Tasks
1. Register NASA FIRMS API key and integrate real satellite data
2. Download Kaggle wildfire dataset and retrain Random Forest model
3. Add user authentication (login/signup)
4. Set up custom domains on Netlify and Render
5. Implement email alerts for high-risk predictions
