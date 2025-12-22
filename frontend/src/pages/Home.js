import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();
  
  const services = [
    {
      id: 'ocr',
      icon: '📄',
      title: 'OCR Service',
      description: 'Extract text from PDFs with highlighting. Upload a PDF and extract text with coordinates or highlight specific search terms.',
      path: '/ocr'
    },
    {
      id: 'audio',
      icon: '🎤',
      title: 'Audio Transcription',
      description: 'Transcribe audio files with timestamps and generate highlights for specific keywords.',
      path: '/audio'
    },
    {
      id: 'agent-creator',
      icon: '🤖',
      title: 'Agent Creator',
      description: 'Create and manage AI agents with custom capabilities, tools, and system prompts.',
      path: '/agent-creator'
    },
    {
      id: 'mcp-creator',
      icon: '⚙️',
      title: 'MCP Creator',
      description: 'Generate complete CRUD APIs using Model Context Protocol. Define resources and get a ready-to-use API.',
      path: '/mcp-creator'
    },
    {
      id: 'whatsapp',
      icon: '💬',
      title: 'WhatsApp Integration',
      description: 'Send messages, templates, and media via WhatsApp Business API. Handle webhooks and message logs.',
      path: '/whatsapp'
    }
  ];
  
  return (
    <div>
      <h1 className="page-title">AI-First Microservices Platform</h1>
      <div className="service-grid">
        {services.map(service => (
          <div 
            key={service.id}
            className="service-card"
            onClick={() => navigate(service.path)}
          >
            <div className="service-icon">{service.icon}</div>
            <h3>{service.title}</h3>
            <p>{service.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
