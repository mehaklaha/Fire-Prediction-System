from fastapi import FastAPI, APIRouter, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
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
import csv
import io
import resend

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url, tlsCAFile=certifi.where())
db = client[os.environ['DB_NAME']]

# Resend setup
resend.api_key = os.environ.get('RESEND_API_KEY', '')
ALERT_EMAIL = os.environ.get('ALERT_EMAIL', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')

# NASA FIRMS API
NASA_FIRMS_MAP_KEY = os.environ.get('NASA_FIRMS_MAP_KEY', '')

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
    np.random.seed(42)
    
    X_train = np.random.rand(1000, 4)
    X_train[:, 0] = X_train[:, 0] * 35 + 5
    X_train[:, 1] = X_train[:, 1] * 48 + 54
    X_train[:, 2] = X_train[:, 2] * 50
    X_train[:, 3] = X_train[:, 3]
    
    y_train = np.zeros(1000)
    for i in range(1000):
        if X_train[i, 2] > 25 and X_train[i, 3] < 0.3:
            y_train[i] = 1
        elif X_train[i, 2] > 15 and X_train[i, 3] < 0.5:
            y_train[i] = np.random.choice([0, 1], p=[0.6, 0.4])
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
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

# ==================== EMAIL ALERT ====================

async def send_fire_alert_email(prediction_data: dict):
    """Send email alert when high-risk fire is predicted"""
    if not resend.api_key or resend.api_key == 'placeholder_add_key' or not ALERT_EMAIL:
        logger.warning("Resend API key or alert email not configured. Skipping email alert.")
        return

    risk_color = "#FF2A2A" if prediction_data["risk_level"] == "High" else "#FFA500"
    
    html_content = f"""
    <div style="font-family: 'Courier New', monospace; background: #050505; color: #FFFFFF; padding: 30px; max-width: 600px; margin: 0 auto;">
        <div style="border-bottom: 2px solid {risk_color}; padding-bottom: 15px; margin-bottom: 20px;">
            <h1 style="color: {risk_color}; margin: 0; font-size: 24px;">FIRE RISK ALERT</h1>
            <p style="color: #888; margin: 5px 0 0 0; font-size: 12px;">Fire Prediction System - Automated Alert</p>
        </div>
        
        <div style="background: #111111; border: 1px solid #333; border-left: 4px solid {risk_color}; padding: 20px; margin-bottom: 20px;">
            <h2 style="color: {risk_color}; margin: 0 0 15px 0; font-size: 20px;">
                {prediction_data["risk_level"].upper()} RISK DETECTED
            </h2>
            <table style="width: 100%; color: #FFFFFF; font-size: 14px;">
                <tr>
                    <td style="padding: 8px 0; color: #888;">Risk Level:</td>
                    <td style="padding: 8px 0; font-weight: bold; color: {risk_color};">{prediction_data["risk_level"]}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Probability:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{prediction_data["probability"]*100:.1f}%</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Latitude:</td>
                    <td style="padding: 8px 0;">{prediction_data["latitude"]}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Longitude:</td>
                    <td style="padding: 8px 0;">{prediction_data["longitude"]}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Wind Speed:</td>
                    <td style="padding: 8px 0;">{prediction_data["wind_speed"]} km/h</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Vegetation Index:</td>
                    <td style="padding: 8px 0;">{prediction_data["vegetation_index"]}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #888;">Timestamp:</td>
                    <td style="padding: 8px 0;">{prediction_data["timestamp"]}</td>
                </tr>
            </table>
        </div>
        
        <div style="background: #111111; border: 1px solid #333; padding: 15px; margin-bottom: 20px;">
            <p style="color: #888; font-size: 12px; margin: 0;">
                Google Maps: 
                <a href="https://www.google.com/maps?q={prediction_data["latitude"]},{prediction_data["longitude"]}" 
                   style="color: #2A66FF;">View Location</a>
            </p>
        </div>
        
        <div style="border-top: 1px solid #333; padding-top: 15px;">
            <p style="color: #666; font-size: 11px; margin: 0;">
                This is an automated alert from the Fire Prediction System.
                Please take necessary precautions if this area is near your jurisdiction.
            </p>
        </div>
    </div>
    """

    try:
        params = {
            "from": SENDER_EMAIL,
            "to": [ALERT_EMAIL],
            "subject": f"[FIRE ALERT] {prediction_data['risk_level'].upper()} Risk at ({prediction_data['latitude']:.4f}, {prediction_data['longitude']:.4f})",
            "html": html_content
        }
        email = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Fire alert email sent to {ALERT_EMAIL}, email_id: {email.get('id', 'N/A')}")
        return True
    except Exception as e:
        logger.error(f"Failed to send fire alert email: {e}")
        return False

# ==================== PYDANTIC MODELS ====================

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
    email_sent: Optional[bool] = False

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

# ==================== API ENDPOINTS ====================

@api_router.get("/")
async def root():
    return {"message": "Fire Prediction System API", "version": "1.0.0"}

@api_router.post("/predict", response_model=FirePredictionResponse)
async def predict_fire(input_data: FirePredictionInput):
    """Predict fire risk based on input parameters"""
    try:
        features = np.array([[
            input_data.latitude,
            input_data.longitude,
            input_data.wind_speed,
            input_data.vegetation_index
        ]])
        
        prediction = fire_model.predict(features)[0]
        probability = fire_model.predict_proba(features)[0][1]
        
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        prediction_doc = {
            "latitude": input_data.latitude,
            "longitude": input_data.longitude,
            "wind_speed": input_data.wind_speed,
            "vegetation_index": input_data.vegetation_index,
            "prediction": int(prediction),
            "probability": float(probability),
            "risk_level": risk_level,
            "timestamp": timestamp
        }
        await db.predictions.insert_one({**prediction_doc})
        
        # Send email alert for Medium and High risk predictions
        email_sent = False
        if risk_level in ("Medium", "High"):
            email_sent = await send_fire_alert_email(prediction_doc)
        
        return FirePredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            wind_speed=input_data.wind_speed,
            vegetation_index=input_data.vegetation_index,
            timestamp=timestamp,
            email_sent=email_sent
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
        
        await db.reported_fires.insert_one({**fire_doc.model_dump()})
        
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

# ==================== WEBSOCKET ====================

@api_router.websocket("/ws/fires")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
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
    
    for conn in disconnected:
        if conn in active_connections:
            active_connections.remove(conn)

# ==================== NASA FIRMS REAL DATA ====================

async def fetch_nasa_firms_data():
    """Fetch live fire data from NASA FIRMS API for India"""
    while True:
        try:
            if NASA_FIRMS_MAP_KEY:
                # Fetch real data from NASA FIRMS API - VIIRS SNPP for India bounding box, last 1 day
                # India bounding box: West=68, South=6, East=97, North=36
                url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{NASA_FIRMS_MAP_KEY}/VIIRS_SNPP_NRT/68,6,97,36/2"
                logger.info(f"Fetching NASA FIRMS data for India...")
                
                response = await asyncio.to_thread(requests.get, url, timeout=30)
                
                if response.status_code == 200 and response.text and not response.text.startswith("Invalid"):
                    reader = csv.DictReader(io.StringIO(response.text))
                    new_fires = []
                    
                    satellite_map = {"N": "Suomi-NPP", "1": "NOAA-20", "2": "NOAA-21"}
                    
                    for row in reader:
                        try:
                            sat_code = row.get("satellite", "N")
                            fire = {
                                "id": str(uuid.uuid4()),
                                "latitude": float(row.get("latitude", 0)),
                                "longitude": float(row.get("longitude", 0)),
                                "brightness": float(row.get("bright_ti4", 0)),
                                "confidence": {"h": "high", "n": "nominal", "l": "low"}.get(row.get("confidence", "n"), "nominal"),
                                "acq_date": row.get("acq_date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                                "acq_time": row.get("acq_time", "0000"),
                                "satellite": satellite_map.get(sat_code, sat_code),
                                "frp": float(row.get("frp", 0))
                            }
                            new_fires.append(fire)
                        except (ValueError, KeyError) as e:
                            continue
                    
                    if new_fires:
                        # Clear old live fires and insert new batch
                        await db.live_fires.delete_many({})
                        # Insert copies to avoid _id mutation
                        docs_to_insert = [{**f} for f in new_fires]
                        await db.live_fires.insert_many(docs_to_insert)
                        
                        logger.info(f"Stored {len(new_fires)} real NASA FIRMS fires for India")
                        
                        # Broadcast latest fires to WebSocket clients
                        for fire in new_fires[:5]:
                            await broadcast_fire_update({
                                "type": "live_fire",
                                "data": fire
                            })
                    else:
                        logger.warning("NASA FIRMS returned no fire data, using fallback")
                        await generate_synthetic_fire()
                else:
                    logger.warning(f"NASA FIRMS API returned status {response.status_code}: {response.text[:200]}")
                    await generate_synthetic_fire()
            else:
                logger.info("No NASA FIRMS key, using synthetic data")
                await generate_synthetic_fire()
            
            # Fetch every 5 minutes (NASA updates ~every 3 hours, but we check more often)
            await asyncio.sleep(300)
            
        except Exception as e:
            logger.error(f"Error in NASA FIRMS fetch: {e}")
            await generate_synthetic_fire()
            await asyncio.sleep(120)

async def generate_synthetic_fire():
    """Fallback: Generate synthetic fire data for India"""
    synthetic_fire = {
        "id": str(uuid.uuid4()),
        "latitude": float(np.random.uniform(8, 35)),
        "longitude": float(np.random.uniform(68, 97)),
        "brightness": float(np.random.uniform(300, 400)),
        "confidence": np.random.choice(["low", "nominal", "high"]),
        "acq_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "acq_time": datetime.now(timezone.utc).strftime("%H%M"),
        "satellite": np.random.choice(["NOAA-20", "Suomi-NPP", "Terra"]),
        "frp": float(np.random.uniform(10, 100))
    }
    
    doc_to_insert = {**synthetic_fire}
    await db.live_fires.insert_one(doc_to_insert)
    await broadcast_fire_update({
        "type": "live_fire",
        "data": synthetic_fire
    })

# ==================== STARTUP / SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    logger.info("Starting Fire Prediction System API")
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
