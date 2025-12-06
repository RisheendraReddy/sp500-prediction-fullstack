import React, { useState, useEffect } from 'react'
import { listModels } from '../services/api'
import './Models.css'

function Models() {
  const [models, setModels] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadModels()
  }, [])

  const loadModels = async () => {
    try {
      const data = await listModels()
      setModels(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load models')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="models-page">
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <span className="loading-spinner" style={{ borderTopColor: 'var(--primary)', width: '32px', height: '32px', margin: '0 auto 1rem' }}></span>
          <p>Loading models...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="models-page">
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="models-page">
      <h1>Available Models</h1>
      
      {models.length === 0 ? (
        <div className="no-models">
          <p>No models found. Train a model first!</p>
        </div>
      ) : (
        <div className="models-grid">
          {models.map((model, index) => (
            <div key={index} className="model-card">
              <h3>{model.model_type.toUpperCase()}</h3>
              <div className="model-details">
                <p><strong>Path:</strong> {model.model_path}</p>
                <p><strong>Features:</strong> {model.features?.length || 0} features</p>
                {model.created_at && (
                  <p><strong>Created:</strong> {new Date(model.created_at).toLocaleString()}</p>
                )}
              </div>
              {model.features && model.features.length > 0 && (
                <details className="features-list">
                  <summary>View Features ({model.features.length})</summary>
                  <ul>
                    {model.features.slice(0, 10).map((feat, i) => (
                      <li key={i}>{feat}</li>
                    ))}
                    {model.features.length > 10 && (
                      <li>... and {model.features.length - 10} more</li>
                    )}
                  </ul>
                </details>
              )}
            </div>
          ))}
        </div>
      )}

      <button onClick={loadModels} className="btn-secondary">
        Refresh
      </button>
    </div>
  )
}

export default Models

