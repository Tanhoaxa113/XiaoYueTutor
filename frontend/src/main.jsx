import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Note: StrictMode causes double-renders in development
// Removed to prevent duplicate WebSocket message processing
ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)
