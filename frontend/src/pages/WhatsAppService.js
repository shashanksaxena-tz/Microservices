import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_WHATSAPP_SERVICE_URL || 'http://localhost:8005';

function WhatsAppService() {
  const [messages, setMessages] = useState([]);
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [messageType, setMessageType] = useState('text'); // 'text', 'template', 'media'
  
  const [textForm, setTextForm] = useState({
    to: '',
    message: ''
  });

  const [templateForm, setTemplateForm] = useState({
    to: '',
    template_name: '',
    language_code: 'en'
  });

  const [mediaForm, setMediaForm] = useState({
    to: '',
    media_type: 'image',
    media_url: '',
    caption: ''
  });

  useEffect(() => {
    loadConfig();
    loadMessages();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/whatsapp/config`);
      setConfig(response.data);
    } catch (err) {
      console.error('Failed to load config:', err);
    }
  };

  const loadMessages = async () => {
    try {
      const response = await axios.get(`${API_URL}/whatsapp/messages`);
      setMessages(response.data.messages || []);
    } catch (err) {
      console.error('Failed to load messages:', err);
    }
  };

  const sendTextMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_URL}/whatsapp/send/text`, textForm);
      setSuccess('Message sent successfully!');
      setTextForm({ to: '', message: '' });
      loadMessages();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const sendTemplateMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_URL}/whatsapp/send/template`, templateForm);
      setSuccess('Template message sent successfully!');
      setTemplateForm({ to: '', template_name: '', language_code: 'en' });
      loadMessages();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send template message');
    } finally {
      setLoading(false);
    }
  };

  const sendMediaMessage = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post(`${API_URL}/whatsapp/send/media`, mediaForm);
      setSuccess('Media message sent successfully!');
      setMediaForm({ to: '', media_type: 'image', media_url: '', caption: '' });
      loadMessages();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send media message');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">WhatsApp Integration</h1>

      {config && (
        <div className="card">
          <h2>Configuration Status</h2>
          <p>
            <strong>API Token:</strong>{' '}
            {config.api_token_configured ? (
              <span className="success">✓ Configured</span>
            ) : (
              <span className="error">✗ Not Configured</span>
            )}
          </p>
          <p>
            <strong>Phone Number ID:</strong>{' '}
            {config.phone_number_id_configured ? (
              <span className="success">✓ Configured</span>
            ) : (
              <span className="error">✗ Not Configured</span>
            )}
          </p>
          {!config.api_token_configured && (
            <p style={{ color: '#666', fontSize: '14px', marginTop: '10px' }}>
              To configure WhatsApp API, set WHATSAPP_API_TOKEN and WHATSAPP_PHONE_NUMBER_ID 
              environment variables in the docker-compose.yml file.
            </p>
          )}
        </div>
      )}

      <div className="card">
        <h2>Send Message</h2>
        
        <div style={{ marginBottom: '20px' }}>
          <label style={{ marginRight: '15px' }}>
            <input
              type="radio"
              value="text"
              checked={messageType === 'text'}
              onChange={() => setMessageType('text')}
            />
            {' '}Text
          </label>
          <label style={{ marginRight: '15px' }}>
            <input
              type="radio"
              value="template"
              checked={messageType === 'template'}
              onChange={() => setMessageType('template')}
            />
            {' '}Template
          </label>
          <label>
            <input
              type="radio"
              value="media"
              checked={messageType === 'media'}
              onChange={() => setMessageType('media')}
            />
            {' '}Media
          </label>
        </div>

        {messageType === 'text' && (
          <form onSubmit={sendTextMessage}>
            <input
              type="tel"
              className="input"
              placeholder="Recipient Phone (with country code, e.g., +1234567890)"
              value={textForm.to}
              onChange={(e) => setTextForm({ ...textForm, to: e.target.value })}
              required
            />
            <textarea
              className="textarea"
              placeholder="Message text"
              value={textForm.message}
              onChange={(e) => setTextForm({ ...textForm, message: e.target.value })}
              required
            />
            <button type="submit" className="button" disabled={loading}>
              {loading ? 'Sending...' : 'Send Text Message'}
            </button>
          </form>
        )}

        {messageType === 'template' && (
          <form onSubmit={sendTemplateMessage}>
            <input
              type="tel"
              className="input"
              placeholder="Recipient Phone (with country code)"
              value={templateForm.to}
              onChange={(e) => setTemplateForm({ ...templateForm, to: e.target.value })}
              required
            />
            <input
              type="text"
              className="input"
              placeholder="Template Name"
              value={templateForm.template_name}
              onChange={(e) => setTemplateForm({ ...templateForm, template_name: e.target.value })}
              required
            />
            <select
              className="input"
              value={templateForm.language_code}
              onChange={(e) => setTemplateForm({ ...templateForm, language_code: e.target.value })}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
            <button type="submit" className="button" disabled={loading}>
              {loading ? 'Sending...' : 'Send Template Message'}
            </button>
          </form>
        )}

        {messageType === 'media' && (
          <form onSubmit={sendMediaMessage}>
            <input
              type="tel"
              className="input"
              placeholder="Recipient Phone (with country code)"
              value={mediaForm.to}
              onChange={(e) => setMediaForm({ ...mediaForm, to: e.target.value })}
              required
            />
            <select
              className="input"
              value={mediaForm.media_type}
              onChange={(e) => setMediaForm({ ...mediaForm, media_type: e.target.value })}
            >
              <option value="image">Image</option>
              <option value="video">Video</option>
              <option value="audio">Audio</option>
              <option value="document">Document</option>
            </select>
            <input
              type="url"
              className="input"
              placeholder="Media URL (publicly accessible)"
              value={mediaForm.media_url}
              onChange={(e) => setMediaForm({ ...mediaForm, media_url: e.target.value })}
              required
            />
            <input
              type="text"
              className="input"
              placeholder="Caption (optional)"
              value={mediaForm.caption}
              onChange={(e) => setMediaForm({ ...mediaForm, caption: e.target.value })}
            />
            <button type="submit" className="button" disabled={loading}>
              {loading ? 'Sending...' : 'Send Media Message'}
            </button>
          </form>
        )}

        {error && <p className="error" style={{ marginTop: '15px' }}>{error}</p>}
        {success && <p className="success" style={{ marginTop: '15px' }}>{success}</p>}
      </div>

      <div className="card">
        <h2>Message Log ({messages.length})</h2>
        {messages.length === 0 ? (
          <p style={{ color: '#666' }}>No messages logged yet.</p>
        ) : (
          <div style={{ maxHeight: '400px', overflow: 'auto' }}>
            {messages.slice().reverse().map((msg, index) => (
              <div key={index} style={{ 
                padding: '10px', 
                border: '1px solid #ddd', 
                borderRadius: '5px',
                marginBottom: '10px',
                background: '#f9f9f9'
              }}>
                <p><strong>Type:</strong> {msg.type}</p>
                <p><strong>Time:</strong> {new Date(msg.timestamp).toLocaleString()}</p>
                <details>
                  <summary style={{ cursor: 'pointer', color: '#667eea' }}>View Details</summary>
                  <pre style={{ 
                    fontSize: '11px', 
                    marginTop: '10px',
                    overflow: 'auto',
                    maxHeight: '200px'
                  }}>
                    {JSON.stringify(msg.data, null, 2)}
                  </pre>
                </details>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default WhatsAppService;
