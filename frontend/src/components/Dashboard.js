import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import { Flame, TrendingUp, AlertTriangle, Activity, MapPin, Wind, Leaf } from 'lucide-react';
import FireMap from './FireMap';
import PredictionForm from './PredictionForm';
import ReportIncidentForm from './ReportIncidentForm';
import LiveFeed from './LiveFeed';
import HistoricalChart from './HistoricalChart';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [stats, setStats] = useState({
    liveFires: 0,
    reportedFires: 0,
    highRiskAreas: 0,
    predictions: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const [liveRes, reportedRes] = await Promise.all([
        axios.get(`${API}/fires/live?limit=1000`, { timeout: 60000 }),
        axios.get(`${API}/fires/reported?limit=1000`, { timeout: 60000 })
      ]);

      setStats({
        liveFires: liveRes.data.length,
        reportedFires: reportedRes.data.length,
        highRiskAreas: Math.floor(liveRes.data.length * 0.3),
        predictions: reportedRes.data.length + liveRes.data.length
      });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: '#050505' }}>
      {/* Header */}
      <header className="border-b" style={{ borderColor: 'rgba(255, 255, 255, 0.1)', background: '#111111' }}>
        <div className="p-4 md:p-6">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded" style={{ background: 'rgba(255, 42, 42, 0.2)' }}>
              <Flame size={32} color="#FF2A2A" data-testid="dashboard-logo" />
            </div>
            <div>
              <h1 
                className="text-3xl md:text-4xl tracking-tighter font-black" 
                style={{ fontFamily: 'Chivo, sans-serif', color: '#FFFFFF' }}
                data-testid="dashboard-title"
              >
                FIRE PREDICTION SYSTEM
              </h1>
              <p className="text-xs tracking-[0.1em] uppercase font-semibold" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                Real-time monitoring & prediction for India
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="p-4 md:p-6" style={{ background: '#111111', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard 
            icon={<Activity size={20} />} 
            label="Live Fires" 
            value={loading ? "..." : stats.liveFires} 
            color="#FF2A2A"
            testId="stat-live-fires"
          />
          <StatCard 
            icon={<AlertTriangle size={20} />} 
            label="Reported Incidents" 
            value={loading ? "..." : stats.reportedFires} 
            color="#FF2A2A"
            testId="stat-reported"
          />
          <StatCard 
            icon={<MapPin size={20} />} 
            label="High Risk Areas" 
            value={loading ? "..." : stats.highRiskAreas} 
            color="#2A66FF"
            testId="stat-high-risk"
          />
          <StatCard 
            icon={<TrendingUp size={20} />} 
            label="Total Incidents" 
            value={loading ? "..." : stats.predictions} 
            color="#2A66FF"
            testId="stat-predictions"
          />
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className="p-4 md:p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 md:gap-6">
          {/* Map - Spans 2 columns and 2 rows */}
          <div className="md:col-span-2 md:row-span-2" data-testid="map-container">
            <FireMap />
          </div>

          {/* Prediction Form */}
          <div className="md:col-span-2" data-testid="prediction-form-container">
            <PredictionForm />
          </div>

          {/* Live Feed */}
          <div className="md:col-span-1 md:row-span-1" data-testid="live-feed-container">
            <LiveFeed />
          </div>

          {/* Report Incident Form */}
          <div className="md:col-span-1" data-testid="report-form-container">
            <ReportIncidentForm />
          </div>

          {/* Historical Chart - Full width */}
          <div className="md:col-span-4" data-testid="historical-chart-container">
            <HistoricalChart />
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color, testId }) => {
  return (
    <div 
      className="p-4 rounded-lg border transition-all duration-200 hover:border-white/20"
      style={{ 
        background: '#111111', 
        borderColor: 'rgba(255, 255, 255, 0.1)'
      }}
      data-testid={testId}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs tracking-[0.1em] uppercase font-semibold" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            {label}
          </p>
          <p className="text-2xl md:text-3xl font-black mt-1" style={{ fontFamily: 'Chivo, sans-serif', color }}>
            {value}
          </p>
        </div>
        <div style={{ color }}>
          {icon}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;