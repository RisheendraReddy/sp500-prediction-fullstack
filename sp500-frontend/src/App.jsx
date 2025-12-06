import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Train from './pages/Train'
import Predict from './pages/Predict'
import Models from './pages/Models'
import './styles/App.css'

function NavLink({ to, children }) {
  const location = useLocation()
  const isActive = location.pathname === to
  
  const handleClick = (e) => {
    console.log('Navigating to:', to)
    // Let the Link handle navigation
  }
  
  return (
    <Link 
      to={to} 
      className={`nav-link ${isActive ? 'active' : ''}`}
      onClick={handleClick}
    >
      {children}
    </Link>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              📈 S&P 500 Predictor
            </Link>
            <div className="nav-menu">
              <NavLink to="/">Home</NavLink>
              <NavLink to="/train">Train Model</NavLink>
              <NavLink to="/predict">Predict</NavLink>
              <NavLink to="/models">Models</NavLink>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/train" element={<Train />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/models" element={<Models />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 S&P 500 Returns Prediction API</p>
        </footer>
      </div>
    </Router>
  )
}

export default App

