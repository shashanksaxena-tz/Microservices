import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import OCRService from './pages/OCRService';
import AudioService from './pages/AudioService';
import AgentCreator from './pages/AgentCreator';
import MCPCreator from './pages/MCPCreator';
import WhatsAppService from './pages/WhatsAppService';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">AI Microservices</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/ocr" className="nav-link">OCR</Link>
              <Link to="/audio" className="nav-link">Audio</Link>
              <Link to="/agent-creator" className="nav-link">Agents</Link>
              <Link to="/mcp-creator" className="nav-link">MCP</Link>
              <Link to="/whatsapp" className="nav-link">WhatsApp</Link>
            </div>
          </div>
        </nav>
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/ocr" element={<OCRService />} />
            <Route path="/audio" element={<AudioService />} />
            <Route path="/agent-creator" element={<AgentCreator />} />
            <Route path="/mcp-creator" element={<MCPCreator />} />
            <Route path="/whatsapp" element={<WhatsAppService />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
