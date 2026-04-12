import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import { Flame } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');

// Custom fire icon
const fireIcon = new L.DivIcon({
  className: 'fire-marker',
  html: `<div style="background: #FF2A2A; width: 16px; height: 16px; border-radius: 50%; border: 2px solid #FFFFFF; box-shadow: 0 0 10px rgba(255, 42, 42, 0.8);"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8]
});

const reportedIcon = new L.DivIcon({
  className: 'reported-marker',
  html: `<div style="background: #FFA500; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #FFFFFF;"></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7]
});

const FireMap = () => {
  const [liveFires, setLiveFires] = useState([]);
  const [reportedFires, setReportedFires] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsRef = React.useRef(null);

  useEffect(() => {
    fetchFires();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchFires = async () => {
    try {
      const [liveRes, reportedRes] = await Promise.all([
        axios.get(`${API}/fires/live?limit=200`, { timeout: 60000 }),
        axios.get(`${API}/fires/reported?limit=100`, { timeout: 60000 })
      ]);

      setLiveFires(liveRes.data);
      setReportedFires(reportedRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching fires:', error);
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/fires`);

      ws.onopen = () => {
        console.log('WebSocket connected');
        ws.send(JSON.stringify({ type: 'ping' }));
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          
          if (message.type === 'live_fire') {
            setLiveFires(prev => [message.data, ...prev].slice(0, 200));
          } else if (message.type === 'reported_fire') {
            setReportedFires(prev => [message.data, ...prev].slice(0, 100));
          }
        } catch (error) {
          console.error('WebSocket message error:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected, reconnecting...');
        setTimeout(connectWebSocket, 3000);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  };

  return (
    <div 
      className="rounded-lg border overflow-hidden" 
      style={{ 
        background: '#111111', 
        borderColor: 'rgba(255, 255, 255, 0.1)',
        height: '600px'
      }}
      data-testid="fire-map"
    >
      <div className="p-4 border-b" style={{ borderColor: 'rgba(255, 255, 255, 0.1)' }}>
        <h2 className="text-xl md:text-2xl tracking-tight font-bold" style={{ fontFamily: 'Chivo, sans-serif' }}>
          Real-Time Fire Map - India
        </h2>
        <p className="text-xs mt-1" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
          <span style={{ color: '#FF2A2A' }}>●</span> Live Fires ({liveFires.length}) 
          <span className="ml-3" style={{ color: '#FFA500' }}>●</span> Reported ({reportedFires.length})
        </p>
      </div>

      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={5}
        style={{ height: 'calc(100% - 70px)', width: '100%' }}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {/* Live fires */}
        {liveFires.map((fire, index) => (
          <Marker
            key={`live-${fire.id}-${index}`}
            position={[fire.latitude, fire.longitude]}
            icon={fireIcon}
          >
            <Popup>
              <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }}>
                <h3 style={{ color: '#FF2A2A', fontWeight: 'bold', marginBottom: '8px' }}>LIVE FIRE DETECTION</h3>
                <p><strong>Satellite:</strong> {fire.satellite}</p>
                <p><strong>Date:</strong> {fire.acq_date}</p>
                <p><strong>Time:</strong> {fire.acq_time}</p>
                <p><strong>Brightness:</strong> {fire.brightness?.toFixed(1)}K</p>
                <p><strong>Confidence:</strong> {fire.confidence}</p>
                <p><strong>FRP:</strong> {fire.frp?.toFixed(1)} MW</p>
                <p><strong>Location:</strong> {fire.latitude.toFixed(4)}, {fire.longitude.toFixed(4)}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Reported fires */}
        {reportedFires.map((fire, index) => (
          <Marker
            key={`reported-${fire.id}-${index}`}
            position={[fire.latitude, fire.longitude]}
            icon={reportedIcon}
          >
            <Popup>
              <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }}>
                <h3 style={{ color: '#FFA500', fontWeight: 'bold', marginBottom: '8px' }}>REPORTED INCIDENT</h3>
                <p><strong>Intensity:</strong> {fire.intensity}</p>
                <p><strong>Description:</strong> {fire.description}</p>
                <p><strong>Reported by:</strong> {fire.reported_by}</p>
                <p><strong>Time:</strong> {new Date(fire.timestamp).toLocaleString()}</p>
                <p><strong>Location:</strong> {fire.latitude.toFixed(4)}, {fire.longitude.toFixed(4)}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {loading && (
        <div className="absolute inset-0 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.5)' }}>
          <p className="text-white">Loading fire data...</p>
        </div>
      )}
    </div>
  );
};

export default FireMap;