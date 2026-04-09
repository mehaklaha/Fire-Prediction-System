import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { TrendingUp } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HistoricalChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [chartType, setChartType] = useState('bar');

  useEffect(() => {
    fetchHistoricalData();
  }, []);

  const fetchHistoricalData = async () => {
    try {
      const response = await axios.get(`${API}/fires/historical?days=7`);
      
      // Format data for recharts
      const formattedData = response.data.dates.map((date, index) => ({
        date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        fires: response.data.counts[index]
      }));

      setData(formattedData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching historical data:', error);
      setLoading(false);
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-3 rounded border" style={{ background: '#111111', borderColor: 'rgba(255, 255, 255, 0.2)' }}>
          <p className="text-sm font-bold">{payload[0].payload.date}</p>
          <p className="text-sm" style={{ color: '#FF2A2A' }}>
            Fires: {payload[0].value}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div 
      className="rounded-lg border p-4 md:p-6"
      style={{ background: '#111111', borderColor: 'rgba(255, 255, 255, 0.1)' }}
      data-testid="historical-chart"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl md:text-2xl tracking-tight font-bold" style={{ fontFamily: 'Chivo, sans-serif' }}>
          <TrendingUp className="inline mr-2" size={24} style={{ color: '#2A66FF' }} />
          Historical Fire Data (7 Days)
        </h2>

        <div className="flex gap-2">
          <button
            onClick={() => setChartType('bar')}
            className="px-3 py-1 rounded text-xs font-bold transition-all"
            style={{ 
              background: chartType === 'bar' ? '#2A66FF' : 'rgba(255, 255, 255, 0.1)',
              color: '#FFFFFF'
            }}
            data-testid="chart-type-bar"
          >
            BAR
          </button>
          <button
            onClick={() => setChartType('line')}
            className="px-3 py-1 rounded text-xs font-bold transition-all"
            style={{ 
              background: chartType === 'line' ? '#2A66FF' : 'rgba(255, 255, 255, 0.1)',
              color: '#FFFFFF'
            }}
            data-testid="chart-type-line"
          >
            LINE
          </button>
        </div>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <p className="text-sm" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Loading chart data...</p>
        </div>
      ) : data.length === 0 ? (
        <div className="h-64 flex items-center justify-center">
          <p className="text-sm" style={{ color: 'rgba(255, 255, 255, 0.6)' }}>No historical data available</p>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          {chartType === 'bar' ? (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
              <XAxis 
                dataKey="date" 
                stroke="rgba(255, 255, 255, 0.6)"
                style={{ fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}
              />
              <YAxis 
                stroke="rgba(255, 255, 255, 0.6)"
                style={{ fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="fires" fill="#FF2A2A" radius={[4, 4, 0, 0]} />
            </BarChart>
          ) : (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
              <XAxis 
                dataKey="date" 
                stroke="rgba(255, 255, 255, 0.6)"
                style={{ fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}
              />
              <YAxis 
                stroke="rgba(255, 255, 255, 0.6)"
                style={{ fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="fires" 
                stroke="#FF2A2A" 
                strokeWidth={2}
                dot={{ fill: '#FF2A2A', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          )}
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default HistoricalChart;