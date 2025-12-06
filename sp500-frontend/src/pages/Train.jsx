import React, { useState } from 'react'
import { trainModel } from '../services/api'
import './Train.css'

function Train() {
  const [modelType, setModelType] = useState('lightgbm')
  const [valSize, setValSize] = useState(0.2)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleTrain = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await trainModel(modelType, valSize)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Training failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="train-page">
      <h1>Train Model</h1>
      
      <form onSubmit={handleTrain} className="train-form">
        <div className="form-group">
          <label htmlFor="modelType">Model Type</label>
          <select
            id="modelType"
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            required
          >
            <option value="lightgbm">LightGBM</option>
            <option value="xgboost">XGBoost</option>
            <option value="rf">Random Forest</option>
            <option value="gbm">Gradient Boosting</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="valSize">Validation Size: {valSize}</label>
          <input
            type="range"
            id="valSize"
            min="0.1"
            max="0.5"
            step="0.05"
            value={valSize}
            onChange={(e) => setValSize(parseFloat(e.target.value))}
          />
          <span className="range-value">{Math.round(valSize * 100)}%</span>
        </div>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading && <span className="loading-spinner"></span>}
          {loading ? 'Training...' : 'Train Model'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="result-card">
          <h3>Training Complete! ✅</h3>
          <div className="result-details">
            <p><strong>Status:</strong> {result.status}</p>
            <p><strong>Model Type:</strong> {result.model_type}</p>
            {result.model_path && (
              <p><strong>Model Path:</strong> {result.model_path}</p>
            )}
            {result.metrics && (
              <div className="metrics">
                <h4>Validation Metrics</h4>
                <div className="metrics-grid">
                  <div className="metric">
                    <span className="metric-label">RMSE</span>
                    <span className="metric-value">{result.metrics.rmse?.toFixed(6)}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">MAE</span>
                    <span className="metric-value">{result.metrics.mae?.toFixed(6)}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-label">R²</span>
                    <span className="metric-value">{result.metrics.r2?.toFixed(6)}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Train

