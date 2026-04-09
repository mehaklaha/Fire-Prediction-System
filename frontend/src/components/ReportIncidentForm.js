import React, { useState } from 'react';
import axios from 'axios';
import { AlertTriangle, MapPin, User } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ReportIncidentForm = () => {
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    description: '',
    intensity: 'Medium',
    reported_by: ''
  });
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      await axios.post(`${API}/report-fire`, {
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        description: formData.description,
        intensity: formData.intensity,
        reported_by: formData.reported_by || 'Anonymous'
      });

      setSuccess(true);
      setFormData({
        latitude: '',
        longitude: '',
        description: '',
        intensity: 'Medium',
        reported_by: ''
      });

      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to report incident');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div 
      className="rounded-lg border p-4 md:p-6"
      style={{ background: '#111111', borderColor: 'rgba(255, 255, 255, 0.1)' }}
      data-testid="report-incident-form"
    >
      <h2 className="text-xl md:text-2xl tracking-tight font-bold mb-4" style={{ fontFamily: 'Chivo, sans-serif' }}>
        <AlertTriangle className="inline mr-2" size={24} style={{ color: '#FF2A2A' }} />
        Report Fire Incident
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
              data-testid="report-latitude"
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
              data-testid="report-longitude"
            />
          </div>
        </div>

        <div>
          <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            Description
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows="3"
            className="w-full p-2 rounded-md text-sm"
            style={{ 
              background: '#050505', 
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#FFFFFF',
              resize: 'vertical'
            }}
            placeholder="Describe the fire incident..."
            data-testid="report-description"
          />
        </div>

        <div>
          <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            Intensity Level
          </label>
          <select
            name="intensity"
            value={formData.intensity}
            onChange={handleChange}
            required
            className="w-full p-2 rounded-md text-sm"
            style={{ 
              background: '#050505', 
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#FFFFFF'
            }}
            data-testid="report-intensity"
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>

        <div>
          <label className="text-xs tracking-[0.1em] uppercase font-semibold block mb-2" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>
            <User size={12} className="inline mr-1" /> Your Name (Optional)
          </label>
          <input
            type="text"
            name="reported_by"
            value={formData.reported_by}
            onChange={handleChange}
            className="w-full p-2 rounded-md text-sm"
            style={{ 
              background: '#050505', 
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#FFFFFF'
            }}
            placeholder="Anonymous"
            data-testid="report-name"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-3 rounded font-bold tracking-wide transition-all text-sm"
          style={{ 
            background: loading ? '#666' : '#FF2A2A',
            color: '#FFFFFF'
          }}
          data-testid="report-submit-button"
        >
          {loading ? 'SUBMITTING...' : 'REPORT INCIDENT'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 rounded" style={{ background: 'rgba(255, 42, 42, 0.2)', borderLeft: '3px solid #FF2A2A' }}>
          <p className="text-sm" style={{ color: '#FF2A2A' }}>{error}</p>
        </div>
      )}

      {success && (
        <div className="mt-4 p-3 rounded" style={{ background: 'rgba(42, 102, 255, 0.2)', borderLeft: '3px solid #2A66FF' }} data-testid="report-success">
          <p className="text-sm" style={{ color: '#2A66FF' }}>✓ Incident reported successfully!</p>
        </div>
      )}
    </div>
  );
};

export default ReportIncidentForm;