# Test Credentials

## API Endpoints

### Fire Prediction API
- **URL**: `/api/predict`
- **Method**: POST
- **Sample Payload**:
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "wind_speed": 25.5,
  "vegetation_index": 0.25
}
```

### Report Fire Incident API
- **URL**: `/api/report-fire`
- **Method**: POST
- **Sample Payload**:
```json
{
  "latitude": 19.0760,
  "longitude": 72.8777,
  "description": "Forest fire near Mumbai",
  "intensity": "High",
  "reported_by": "Test User"
}
```

### Live Fires API
- **URL**: `/api/fires/live?limit=50`
- **Method**: GET

### Reported Fires API
- **URL**: `/api/fires/reported?limit=50`
- **Method**: GET

### Historical Data API
- **URL**: `/api/fires/historical?days=7`
- **Method**: GET

## WebSocket Connection
- **URL**: `ws://[BACKEND_URL]/api/ws/fires`
- Receives real-time updates for live fires and reported incidents

## Test Scenarios

### 1. High Risk Fire Prediction
- Latitude: 28.6139
- Longitude: 77.2090
- Wind Speed: 30 km/h
- Vegetation Index: 0.2
- Expected: High risk prediction

### 2. Low Risk Fire Prediction
- Latitude: 20.5
- Longitude: 78.9
- Wind Speed: 10 km/h
- Vegetation Index: 0.8
- Expected: Low risk prediction

### 3. Report Fire Incident
- Any valid coordinates within India
- Description: Any text
- Intensity: Low/Medium/High
- Expected: Success message and fire appears in live feed

## Notes
- No authentication required for testing
- Backend generates synthetic live fire data every 30 seconds
- Random Forest model is pre-trained with synthetic data
- WebSocket automatically reconnects on disconnect
