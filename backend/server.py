from fastapi import FastAPI, APIRouter, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import asyncio
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import requests
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Fire Prediction System API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables for WebSocket connections
active_connections: List[WebSocket] = []

# Train and save a simple Random Forest model
def create_fire_prediction_model():
    """Create and train a Random Forest model for fire prediction"""
    # Synthetic training data (latitude, longitude, wind_speed, vegetation_index)
    # Features: [lat, lon, wind_speed, veg_index]
    # Label: 1 = fire risk, 0 = no fire risk
    np.random.seed(42)
    
    # Generate synthetic training data
    X_train = np.random.rand(1000, 4)
    # Scale features to realistic ranges
    X_train[:, 0] = X_train[:, 0] * 35 + 5  # lat: 5-40
    X_train[:, 1] = X_train[:, 1] * 48 + 54  # lon: 54-102
    X_train[:, 2] = X_train[:, 2] * 50  # wind_speed: 0-50 km/h
    X_train[:, 3] = X_train[:, 3]  # veg_index: 0-1
    
    # Create labels based on some rules
    y_train = np.zeros(1000)
    for i in range(1000):
        # High wind speed, low vegetation index = higher fire risk
        if X_train[i, 2] > 25 and X_train[i, 3] < 0.3:
            y_train[i] = 1
        # Medium conditions
        elif X_train[i, 2] > 15 and X_train[i, 3] < 0.5:
            y_train[i] = np.random.choice([0, 1], p=[0.6, 0.4])
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    model_path = ROOT_DIR / 'fire_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info("Fire prediction model created and saved")
    return model

# Load or create model
try:
    model_path = ROOT_DIR / 'fire_model.pkl'
    if model_path.exists():
        with open(model_path, 'rb') as f:
            fire_model = pickle.load(f)
        logger.info("Loaded existing fire prediction model")
    else:
        fire_model = create_fire_prediction_model()
except Exception as e:
    logger.error(f"Error loading model: {e}")
    fire_model = create_fire_prediction_model()

# Pydantic Models
class FirePredictionInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    wind_speed: float = Field(..., ge=0, description="Wind speed in km/h")
    vegetation_index: float = Field(..., ge=0, le=1, description="Vegetation index (0-1)")

class FirePredictionResponse(BaseModel):
    prediction: int = Field(..., description="0: No Fire Risk, 1: Fire Risk")
    probability: float = Field(..., description="Probability of fire (0-1)")
    risk_level: str = Field(..., description="Low, Medium, or High")
    latitude: float
    longitude: float
    wind_speed: float
    vegetation_index: float
    timestamp: str

class ReportedFire(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    latitude: float
    longitude: float
    description: str
    intensity: str = Field(..., description="Low, Medium, or High")
    reported_by: str = "Anonymous"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ReportFireInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    description: str
    intensity: str = Field(..., pattern="^(Low|Medium|High)$")
    reported_by: Optional[str] = "Anonymous"

class LiveFire(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    latitude: float
    longitude: float
    brightness: Optional[float] = None
    confidence: Optional[str] = None
    acq_date: str
    acq_time: str
    satellite: Optional[str] = None
    frp: Optional[float] = None

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "Fire Prediction System API", "version": "1.0.0"}

@api_router.post("/predict", response_model=FirePredictionResponse)
async def predict_fire(input_data: FirePredictionInput):
    """Predict fire risk based on input parameters"""
    try:
        # Prepare features for prediction
        features = np.array([[
            input_data.latitude,
            input_data.longitude,
            input_data.wind_speed,
            input_data.vegetation_index
        ]])
        
        # Get prediction
        prediction = fire_model.predict(features)[0]
        probability = fire_model.predict_proba(features)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Store prediction in database
        prediction_doc = {
            "latitude": input_data.latitude,
            "longitude": input_data.longitude,
            "wind_speed": input_data.wind_speed,
            "vegetation_index": input_data.vegetation_index,
            "prediction": int(prediction),
            "probability": float(probability),
            "risk_level": risk_level,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.predictions.insert_one(prediction_doc)
        
        return FirePredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            wind_speed=input_data.wind_speed,
            vegetation_index=input_data.vegetation_index,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/report-fire", response_model=ReportedFire)
async def report_fire(fire_data: ReportFireInput):
    """Report a fire incident"""
    try:
        fire_doc = ReportedFire(
            latitude=fire_data.latitude,
            longitude=fire_data.longitude,
            description=fire_data.description,
            intensity=fire_data.intensity,
            reported_by=fire_data.reported_by or "Anonymous"
        )
        
        # Store in database
        await db.reported_fires.insert_one(fire_doc.model_dump())
        
        # Broadcast to WebSocket clients
        await broadcast_fire_update({
            "type": "reported_fire",
            "data": fire_doc.model_dump()
        })
        
        return fire_doc
    except Exception as e:
        logger.error(f"Error reporting fire: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/fires/live", response_model=List[LiveFire])
async def get_live_fires(limit: int = 100):
    """Get live fire incidents from NASA FIRMS data"""
    try:
        fires = await db.live_fires.find({}, {"_id": 0}).sort("acq_date", -1).limit(limit).to_list(limit)
        return fires
    except Exception as e:
        logger.error(f"Error fetching live fires: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/fires/reported", response_model=List[ReportedFire])
async def get_reported_fires(limit: int = 100):
    """Get reported fire incidents"""
    try:
        fires = await db.reported_fires.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
        return fires
    except Exception as e:
        logger.error(f"Error fetching reported fires: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/fires/historical")
async def get_historical_fires(days: int = 7):
    """Get historical fire data for charts"""
    try:
        cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        
        # Get counts by date
        pipeline = [
            {"$match": {"timestamp": {"$gte": cutoff_date}}},
            {"$group": {
                "_id": {"$substr": ["$timestamp", 0, 10]},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        result = await db.reported_fires.aggregate(pipeline).to_list(None)
        
        return {
            "dates": [item["_id"] for item in result],
            "counts": [item["count"] for item in result]
        }
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return {"dates": [], "counts": []}

# WebSocket endpoint
@api_router.websocket("/ws/fires")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Connection alive"})
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Remaining: {len(active_connections)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

async def broadcast_fire_update(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.error(f"Error broadcasting: {e}")
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)

# Background task to fetch NASA FIRMS data
async def fetch_nasa_firms_data():
    """Fetch live fire data from NASA FIRMS API"""
    # Note: NASA FIRMS requires API key registration
    # For demo purposes, we'll create synthetic live fire data
    while True:
        try:
            # Generate synthetic live fire for India region
            synthetic_fire = {
                "id": str(uuid.uuid4()),
                "latitude": np.random.uniform(8, 35),
                "longitude": np.random.uniform(68, 97),
                "brightness": np.random.uniform(300, 400),
                "confidence": np.random.choice(["low", "nominal", "high"]),
                "acq_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "acq_time": datetime.now(timezone.utc).strftime("%H:%M"),
                "satellite": np.random.choice(["NOAA-20", "Suomi-NPP", "Terra"]),
                "frp": np.random.uniform(10, 100)
            }
            
            # Store in database
            await db.live_fires.insert_one(synthetic_fire)
            
            # Broadcast to connected clients
            await broadcast_fire_update({
                "type": "live_fire",
                "data": synthetic_fire
            })
            
            logger.info(f"Added synthetic live fire at {synthetic_fire['latitude']}, {synthetic_fire['longitude']}")
            
            # Wait 30 seconds before next update
            await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Error in NASA FIRMS fetch: {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    logger.info("Starting Fire Prediction System API")
    # Start NASA FIRMS data fetching in background
    asyncio.create_task(fetch_nasa_firms_data())

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)