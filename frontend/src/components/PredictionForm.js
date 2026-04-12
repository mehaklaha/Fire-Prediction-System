import React, { useState } from 'react';
import axios from 'axios';
import { TrendingUp, MapPin, Wind, Leaf, Flame } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    wind_speed: '',
    vegetation_index: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API}/predict`, {
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        wind_speed: parseFloat(formData.wind_speed),
        vegetation_index: parseFloat(formData.vegetation_index)
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const getRiskColor = (level) => {
    switch(level) {
      case 'High': return '#FF2A2A';
      case 'Medium': return '#FFA500';
      case 'Low': return '#2A66FF';
      default: return '#FFFFFF';
    }
  };

  return (
    <div 
      className="rounded-lg border p-4 md:p-6"
      style={{ background: '#111111', borderColor: 'rgba(255, 255, 255, 0.1)' }}
      data-testid="prediction-form"
    >
      <h2 className="text-xl md:text-2xl tracking-tight font-bold mb-4" style={{ fontFamily: 'Chivo, sans-serif' }}>
        <TrendingUp className="inline mr-2" size={24} style={{ color: '#2A66FF' }} />
        Fire Risk Prediction
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
              <MapPin size={12} className="inline mr-1" /> Latitude
            </label>
            <input
              type="number"
              name="latitude"
              step="0.0001"
              min="-90"
              max="90"
              value={formData.latitude}
              onChange={handleChange}
              required
              className="w-full p-2 rounded-md text-sm"
              style={{ 
                background: '#050505', 
                border: '1px solid rgba(255, 255, 255, 0.2)',
                color: '#FFFFFF'
              }}
              placeholder="e.g., 28.6139"
              data-testid="input-latitude"
            />
          </div>

          <div>
            <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
              <MapPin size={12} className="inline mr-1" /> Longitude
            </label>
            <input
              type="number"
              name="longitude"
              step="0.0001"
              min="-180"
              max="180"
              value={formData.longitude}
              onChange={handleChange}
              required
              className="w-full p-2 rounded-md text-sm"
              style={{ 
                background: '#050505', 
                border: '1px solid rgba(255, 255, 255, 0.2)',
                color: '#FFFFFF'
              }}
              placeholder="e.g., 77.2090"
              data-testid="input-longitude"
            />
          </div>
        </div>

        <div>
          <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            <Wind size={12} className="inline mr-1" /> Wind Speed (km/h)
          </label>
          <input
            type="number"
            name="wind_speed"
            step="0.1"
            min="0"
            value={formData.wind_speed}
            onChange={handleChange}
            required
            className="w-full p-2 rounded-md text-sm"
            style={{ 
              background: '#050505', 
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#FFFFFF'
            }}
            placeholder="e.g., 15.5"
            data-testid="input-wind-speed"
          />
        </div>

        <div>
          <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            <Leaf size={12} className="inline mr-1" /> Vegetation Index (0-1)
          </label>
          <input
            type="number"
            name="vegetation_index"
            step="0.01"
            min="0"
            max="1"
            value={formData.vegetation_index}
            onChange={handleChange}
            required
            className="w-full p-2 rounded-md text-sm"
            style={{ 
              background: '#050505', 
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#FFFFFF'
            }}
            placeholder="e.g., 0.35"
            data-testid="input-vegetation-index"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-3 rounded font-bold tracking-wide transition-all text-sm"
          style={{ 
            background: loading ? '#666' : '#2A66FF',
            color: '#FFFFFF'
          }}
          data-testid="predict-button"
        >
          {loading ? 'ANALYZING...' : 'PREDICT FIRE RISK'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 rounded" style={{ background: 'rgba(255, 42, 42, 0.2)', borderLeft: '3px solid #FF2A2A' }}>
          <p className="text-sm" style={{ color: '#FF2A2A' }}>{error}</p>
        </div>
      )}

      {result && (
        <div 
          className="mt-4 p-4 rounded border"
          style={{ 
            background: 'rgba(255, 255, 255, 0.05)',
            borderColor: getRiskColor(result.risk_level)
          }}
          data-testid="prediction-result"
        >
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-bold" style={{ fontFamily: 'Chivo, sans-serif' }}>PREDICTION RESULT</h3>
            <Flame size={24} style={{ color: getRiskColor(result.risk_level) }} />
          </div>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Risk Level:</span>
              <span className="font-bold" style={{ color: getRiskColor(result.risk_level) }}>
                {result.risk_level.toUpperCase()}
              </span>
            </div>
            <div className="flex justify-between">
              <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Probability:</span>
              <span className="font-bold">{(result.probability * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Prediction:</span>
              <span className="font-bold">{result.prediction === 1 ? 'FIRE RISK DETECTED' : 'NO FIRE RISK'}</span>
            </div>
            {result.email_sent && (
              <div className="flex justify-between">
                <span style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Email Alert:</span>
                <span className="font-bold" style={{ color: '#2A66FF' }}>SENT TO ADMIN</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionForm;