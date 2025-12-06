import React, { useState, useEffect } from 'react'
import { healthCheck } from '../services/api'
import './Home.css'

function Home() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkHealth()
  }, [])

  const checkHealth = async () => {
    try {
      const data = await healthCheck()
      setHealth(data)
    } catch (error) {
      console.error('Health check failed:', error)
      setHealth({ status: 'error', message: 'API is not reachable' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home">
      <div className="hero">
        <h1>📈 S&P 500 Returns Prediction</h1>
        <p className="subtitle">Predict daily returns using Machine Learning</p>
      </div>

      <div className="status-card">
        <h2>API Status</h2>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="loading-spinner" style={{ borderTopColor: 'var(--primary)' }}></span>
            <p>Checking...</p>
          </div>
        ) : (
          <div className={`status ${health?.status === 'healthy' ? 'online' : 'offline'}`}>
            <span className="status-indicator"></span>
            <span>{health?.status === 'healthy' ? 'Online' : 'Offline'}</span>
            {health?.version && <span className="version">v{health.version}</span>}
          </div>
        )}
        {health?.models_available && health.models_available.length > 0 && (
          <div className="models-info">
            <p>Available Models: {health.models_available.join(', ')}</p>
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>🚀 Train Models</h3>
          <p>Train machine learning models using LightGBM, XGBoost, Random Forest, or Gradient Boosting</p>
        </div>
        <div className="feature-card">
          <h3>📊 Make Predictions</h3>
          <p>Predict S&P 500 daily returns using trained models with single or batch predictions</p>
        </div>
        <div className="feature-card">
          <h3>📈 View Models</h3>
          <p>View all available trained models and their details</p>
        </div>
      </div>
    </div>
  )
}

export default Home

