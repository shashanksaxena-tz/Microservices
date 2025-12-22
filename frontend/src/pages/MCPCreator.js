import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_MCP_CREATOR_URL || 'http://localhost:8004';

function MCPCreator() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [viewCode, setViewCode] = useState(null);
  
  const [formData, setFormData] = useState({
    project_name: '',
    description: '',
    base_path: '/api/v1',
  });

  const [resources, setResources] = useState([
    {
      name: '',
      description: '',
      fields: [{ name: 'name', type: 'string', required: true, description: '' }],
      enable_create: true,
      enable_read: true,
      enable_update: true,
      enable_delete: true,
      enable_list: true
    }
  ]);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await axios.get(`${API_URL}/mcp/list`);
      setProjects(response.data.projects || []);
    } catch (err) {
      console.error('Failed to load projects:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const addResource = () => {
    setResources([...resources, {
      name: '',
      description: '',
      fields: [{ name: '', type: 'string', required: true, description: '' }],
      enable_create: true,
      enable_read: true,
      enable_update: true,
      enable_delete: true,
      enable_list: true
    }]);
  };

  const updateResource = (index, field, value) => {
    const newResources = [...resources];
    newResources[index][field] = value;
    setResources(newResources);
  };

  const addField = (resourceIndex) => {
    const newResources = [...resources];
    newResources[resourceIndex].fields.push({
      name: '',
      type: 'string',
      required: true,
      description: ''
    });
    setResources(newResources);
  };

  const updateField = (resourceIndex, fieldIndex, field, value) => {
    const newResources = [...resources];
    newResources[resourceIndex].fields[fieldIndex][field] = value;
    setResources(newResources);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const projectData = {
      ...formData,
      resources: resources
    };

    try {
      const response = await axios.post(`${API_URL}/mcp/create`, projectData);
      setSuccess('MCP project created successfully!');
      setFormData({
        project_name: '',
        description: '',
        base_path: '/api/v1',
      });
      setResources([{
        name: '',
        description: '',
        fields: [{ name: 'name', type: 'string', required: true, description: '' }],
        enable_create: true,
        enable_read: true,
        enable_update: true,
        enable_delete: true,
        enable_list: true
      }]);
      loadProjects();
      setViewCode(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  const viewProjectCode = async (projectId) => {
    try {
      const response = await axios.get(`${API_URL}/mcp/${projectId}`);
      setViewCode(response.data);
    } catch (err) {
      setError('Failed to load project code');
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">MCP Creator</h1>

      <div className="card">
        <h2>Create CRUD API Project</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="project_name"
            className="input"
            placeholder="Project Name"
            value={formData.project_name}
            onChange={handleInputChange}
            required
          />

          <input
            type="text"
            name="description"
            className="input"
            placeholder="Project Description"
            value={formData.description}
            onChange={handleInputChange}
            required
          />

          <input
            type="text"
            name="base_path"
            className="input"
            placeholder="Base Path (e.g., /api/v1)"
            value={formData.base_path}
            onChange={handleInputChange}
          />

          <h3 style={{ marginTop: '20px', marginBottom: '10px' }}>Resources</h3>
          {resources.map((resource, rIndex) => (
            <div key={rIndex} style={{ 
              border: '1px solid #ddd', 
              padding: '15px', 
              borderRadius: '5px',
              marginBottom: '15px'
            }}>
              <h4>Resource {rIndex + 1}</h4>
              <input
                type="text"
                className="input"
                placeholder="Resource Name (e.g., user, product)"
                value={resource.name}
                onChange={(e) => updateResource(rIndex, 'name', e.target.value)}
                required
              />

              <input
                type="text"
                className="input"
                placeholder="Resource Description"
                value={resource.description}
                onChange={(e) => updateResource(rIndex, 'description', e.target.value)}
                required
              />

              <h5>Fields</h5>
              {resource.fields.map((field, fIndex) => (
                <div key={fIndex} style={{ 
                  display: 'grid', 
                  gridTemplateColumns: '2fr 1fr 1fr', 
                  gap: '10px',
                  marginBottom: '10px'
                }}>
                  <input
                    type="text"
                    className="input"
                    placeholder="Field Name"
                    value={field.name}
                    onChange={(e) => updateField(rIndex, fIndex, 'name', e.target.value)}
                    required
                  />
                  <select
                    className="input"
                    value={field.type}
                    onChange={(e) => updateField(rIndex, fIndex, 'type', e.target.value)}
                  >
                    <option value="string">String</option>
                    <option value="integer">Integer</option>
                    <option value="float">Float</option>
                    <option value="boolean">Boolean</option>
                    <option value="date">Date</option>
                  </select>
                  <label>
                    <input
                      type="checkbox"
                      checked={field.required}
                      onChange={(e) => updateField(rIndex, fIndex, 'required', e.target.checked)}
                    />
                    {' '}Required
                  </label>
                </div>
              ))}
              <button 
                type="button"
                className="button" 
                onClick={() => addField(rIndex)}
                style={{ fontSize: '12px', padding: '5px 10px' }}
              >
                + Add Field
              </button>
            </div>
          ))}

          <button 
            type="button"
            className="button" 
            onClick={addResource}
            style={{ marginBottom: '15px' }}
          >
            + Add Resource
          </button>

          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Creating...' : 'Generate API'}
          </button>

          {error && <p className="error" style={{ marginTop: '15px' }}>{error}</p>}
          {success && <p className="success" style={{ marginTop: '15px' }}>{success}</p>}
        </form>
      </div>

      {viewCode && (
        <div className="card">
          <h2>Generated Code</h2>
          <p><strong>Project ID:</strong> {viewCode.project_id}</p>
          {viewCode.files && (
            <details>
              <summary style={{ cursor: 'pointer', fontWeight: 'bold', marginBottom: '10px' }}>
                View main.py
              </summary>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: '15px', 
                borderRadius: '5px',
                overflow: 'auto',
                maxHeight: '500px',
                fontSize: '12px'
              }}>
                {viewCode.files['main.py']}
              </pre>
            </details>
          )}
        </div>
      )}

      <div className="card">
        <h2>Your Projects ({projects.length})</h2>
        {projects.length === 0 ? (
          <p style={{ color: '#666' }}>No projects created yet.</p>
        ) : (
          <div style={{ display: 'grid', gap: '15px' }}>
            {projects.map(project => (
              <div key={project.project_id} style={{ 
                padding: '15px', 
                border: '1px solid #ddd', 
                borderRadius: '5px',
                background: '#f9f9f9'
              }}>
                <h3>{project.project_name}</h3>
                <p style={{ color: '#666' }}>{project.description}</p>
                <button 
                  className="button" 
                  onClick={() => viewProjectCode(project.project_id)}
                  style={{ marginTop: '10px' }}
                >
                  View Code
                </button>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
                  Created: {new Date(project.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default MCPCreator;
