import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Flame, Clock } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const WS_URL = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');

const LiveFeed = () => {
  const [fires, setFires] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsRef = React.useRef(null);

  useEffect(() => {
    fetchLiveFires();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const fetchLiveFires = async () => {
    try {
      const response = await axios.get(`${API}/fires/live?limit=50`);
      setFires(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching live fires:', error);
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/fires`);

      ws.onopen = () => {
        console.log('LiveFeed WebSocket connected');
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          
          if (message.type === 'live_fire') {
            setFires(prev => [message.data, ...prev].slice(0, 50));
          }
        } catch (error) {
          console.error('WebSocket message error:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        setTimeout(connectWebSocket, 3000);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  };

  const formatTime = (dateStr, timeStr) => {
    try {
      const time = timeStr.length === 4 ? `${timeStr.slice(0, 2)}:${timeStr.slice(2)}` : timeStr;
      return `${dateStr} ${time}`;
    } catch {
      return `${dateStr} ${timeStr}`;
    }
  };

  return (
    <div 
      className="rounded-lg border p-4 md:p-6"
      style={{ background: '#111111', borderColor: 'rgba(255, 255, 255, 0.1)' }}
      data-testid="live-feed"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl md:text-2xl tracking-tight font-bold" style={{ fontFamily: 'Chivo, sans-serif' }}>
          <Activity className="inline mr-2" size={24} style={{ color: '#FF2A2A' }} />
          Live Feed
        </h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: '#FF2A2A' }}></div>
          <span className="text-xs" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>LIVE</span>
        </div>
      </div>

      <div className="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
        {loading ? (
          <p className="text-sm text-center py-4" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Loading...</p>
        ) : fires.length === 0 ? (
          <p className="text-sm text-center py-4" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>No live fires detected</p>
        ) : (
          fires.map((fire, index) => (
            <div
              key={`${fire.id}-${index}`}
              className="p-3 rounded border transition-all duration-200 hover:border-white/20"
              style={{ 
                background: 'rgba(255, 255, 255, 0.05)',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderLeft: '2px solid #FF2A2A'
              }}
              data-testid={`live-fire-item-${index}`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Flame size={16} style={{ color: '#FF2A2A' }} />
                  <span className="text-xs font-bold" style={{ color: '#FF2A2A' }}>
                    {fire.satellite || 'SATELLITE'}
                  </span>
                </div>
                <span 
                  className="text-xs px-2 py-1 rounded" 
                  style={{ 
                    background: fire.confidence === 'high' ? 'rgba(255, 42, 42, 0.2)' : 'rgba(255, 165, 0, 0.2)',
                    color: fire.confidence === 'high' ? '#FF2A2A' : '#FFA500'
                  }}
                >
                  {fire.confidence?.toUpperCase() || 'N/A'}
                </span>
              </div>

              <div className="text-xs space-y-1" style={{ fontFamily: 'JetBrains Mono, monospace' }}>
                <p>
                  <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Location:</span> 
                  <span className="ml-1">{fire.latitude.toFixed(3)}, {fire.longitude.toFixed(3)}</span>
                </p>
                <p>
                  <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Brightness:</span> 
                  <span className="ml-1">{fire.brightness?.toFixed(1) || 'N/A'}K</span>
                </p>
                <p className="flex items-center gap-1">
                  <Clock size={10} style={{ color: 'rgba(255, 255, 255, 0.6)' }} />
                  <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                    {formatTime(fire.acq_date, fire.acq_time)}
                  </span>
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LiveFeed;