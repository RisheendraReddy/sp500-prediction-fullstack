import React from 'react'
import './LoadingSpinner.css'

function LoadingSpinner({ size = 'medium', color = 'var(--primary)' }) {
  const sizeClass = `spinner-${size}`
  
  return (
    <div className={`loading-spinner-container ${sizeClass}`}>
      <div className="spinner" style={{ borderTopColor: color }}>
        <div className="spinner-inner"></div>
      </div>
    </div>
  )
}

export default LoadingSpinner

