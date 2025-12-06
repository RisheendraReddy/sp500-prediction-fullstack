import React, { useState } from 'react'
import { predictSingle, predictBatch, predictFromFile } from '../services/api'
import './Predict.css'

function Predict() {
  const [mode, setMode] = useState('single')
  const [dateId, setDateId] = useState(1)
  const [features, setFeatures] = useState('{"M1": 0.5, "M2": 0.3}')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [file, setFile] = useState(null)

  const handleSinglePredict = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const featuresObj = JSON.parse(features)
      const data = await predictSingle(dateId, featuresObj)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const handleFilePredict = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const blob = await predictFromFile(file)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'predictions.csv'
      a.click()
      setResult({ message: 'Predictions downloaded successfully!' })
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="predict-page">
      <h1>Make Predictions</h1>

      <div className="mode-selector">
        <button
          className={mode === 'single' ? 'active' : ''}
          onClick={() => setMode('single')}
        >
          Single Prediction
        </button>
        <button
          className={mode === 'file' ? 'active' : ''}
          onClick={() => setMode('file')}
        >
          From CSV File
        </button>
      </div>

      {mode === 'single' ? (
        <form onSubmit={handleSinglePredict} className="predict-form">
          <div className="form-group">
            <label htmlFor="dateId">Date ID</label>
            <input
              type="number"
              id="dateId"
              value={dateId}
              onChange={(e) => setDateId(parseInt(e.target.value))}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="features">Features (JSON)</label>
            <textarea
              id="features"
              value={features}
              onChange={(e) => setFeatures(e.target.value)}
              rows="5"
              placeholder='{"M1": 0.5, "M2": 0.3, "E1": 0.2}'
              required
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading && <span className="loading-spinner"></span>}
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>
      ) : (
        <form onSubmit={handleFilePredict} className="predict-form">
          <div className="form-group">
            <label htmlFor="file">CSV File</label>
            <input
              type="file"
              id="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
            <small>Upload a CSV file with date_id and feature columns</small>
          </div>

          <button type="submit" disabled={loading || !file} className="btn-primary">
            {loading && <span className="loading-spinner"></span>}
            {loading ? 'Processing...' : 'Predict from File'}
          </button>
        </form>
      )}

      {error && (
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="result-card">
          <h3>Prediction Result</h3>
          {result.forward_returns !== undefined ? (
            <div className="prediction-result">
              <p><strong>Date ID:</strong> {result.date_id}</p>
              <p><strong>Forward Returns:</strong> 
                <span className="prediction-value">{result.forward_returns.toFixed(6)}</span>
              </p>
            </div>
          ) : (
            <p>{result.message || 'Success!'}</p>
          )}
        </div>
      )}
    </div>
  )
}

export default Predict

