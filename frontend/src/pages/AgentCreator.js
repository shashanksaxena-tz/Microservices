import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_AGENT_CREATOR_URL || 'http://localhost:8003';

function AgentCreator() {
  const [agents, setAgents] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    system_prompt: '',
    model: 'gpt-4',
    temperature: 0.7,
    capabilities: ''
  });

  useEffect(() => {
    loadAgents();
    loadTemplates();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await axios.get(`${API_URL}/agents/list`);
      setAgents(response.data.agents || []);
    } catch (err) {
      console.error('Failed to load agents:', err);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await axios.get(`${API_URL}/agents/templates/list`);
      setTemplates(response.data.templates || []);
    } catch (err) {
      console.error('Failed to load templates:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const agentData = {
      ...formData,
      temperature: parseFloat(formData.temperature),
      capabilities: formData.capabilities.split(',').map(c => c.trim()).filter(c => c),
      tools: []
    };

    try {
      await axios.post(`${API_URL}/agents/create`, agentData);
      setSuccess('Agent created successfully!');
      setFormData({
        name: '',
        description: '',
        system_prompt: '',
        model: 'gpt-4',
        temperature: 0.7,
        capabilities: ''
      });
      loadAgents();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create agent');
    } finally {
      setLoading(false);
    }
  };

  const createFromTemplate = async (templateId) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_URL}/agents/templates/${templateId}`);
      setSuccess('Agent created from template!');
      loadAgents();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create agent from template');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Agent Creator</h1>

      <div className="card">
        <h2>Create New Agent</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            className="input"
            placeholder="Agent Name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <input
            type="text"
            name="description"
            className="input"
            placeholder="Agent Description"
            value={formData.description}
            onChange={handleInputChange}
            required
          />

          <textarea
            name="system_prompt"
            className="textarea"
            placeholder="System Prompt (e.g., 'You are a helpful assistant...')"
            value={formData.system_prompt}
            onChange={handleInputChange}
            required
          />

          <select
            name="model"
            className="input"
            value={formData.model}
            onChange={handleInputChange}
          >
            <option value="gpt-4">GPT-4</option>
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="claude-3">Claude 3</option>
          </select>

          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Temperature: {formData.temperature}
            </label>
            <input
              type="range"
              name="temperature"
              min="0"
              max="2"
              step="0.1"
              value={formData.temperature}
              onChange={handleInputChange}
              style={{ width: '100%' }}
            />
          </div>

          <input
            type="text"
            name="capabilities"
            className="input"
            placeholder="Capabilities (comma separated)"
            value={formData.capabilities}
            onChange={handleInputChange}
          />

          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Creating...' : 'Create Agent'}
          </button>

          {error && <p className="error" style={{ marginTop: '15px' }}>{error}</p>}
          {success && <p className="success" style={{ marginTop: '15px' }}>{success}</p>}
        </form>
      </div>

      <div className="card">
        <h2>Templates</h2>
        <div style={{ display: 'grid', gap: '15px' }}>
          {templates.map(template => (
            <div key={template.id} style={{ 
              padding: '15px', 
              border: '1px solid #ddd', 
              borderRadius: '5px' 
            }}>
              <h3>{template.name}</h3>
              <p style={{ color: '#666', marginBottom: '10px' }}>{template.description}</p>
              <button 
                className="button" 
                onClick={() => createFromTemplate(template.id)}
                disabled={loading}
              >
                Use Template
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>Your Agents ({agents.length})</h2>
        {agents.length === 0 ? (
          <p style={{ color: '#666' }}>No agents created yet.</p>
        ) : (
          <div style={{ display: 'grid', gap: '15px' }}>
            {agents.map(agent => (
              <div key={agent.agent_id} style={{ 
                padding: '15px', 
                border: '1px solid #ddd', 
                borderRadius: '5px',
                background: '#f9f9f9'
              }}>
                <h3>{agent.name}</h3>
                <p style={{ color: '#666' }}>{agent.description}</p>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
                  Created: {new Date(agent.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AgentCreator;
