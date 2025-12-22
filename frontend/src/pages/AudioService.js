import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_AUDIO_SERVICE_URL || 'http://localhost:8002';

function AudioService() {
  const [file, setFile] = useState(null);
  const [keywords, setKeywords] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('transcribe'); // 'transcribe' or 'highlight'

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
    setResult(null);
  };

  const handleTranscribe = async () => {
    if (!file) {
      setError('Please select an audio file');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/audio/transcribe`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Transcription failed');
    } finally {
      setLoading(false);
    }
  };

  const handleHighlight = async () => {
    if (!file) {
      setError('Please select an audio file');
      return;
    }

    if (!keywords.trim()) {
      setError('Please enter keywords');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('keywords', keywords);

    try {
      const response = await axios.post(`${API_URL}/audio/highlight`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Processing failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Audio Transcription Service</h1>
      
      <div className="card">
        <h2>Upload Audio for Processing</h2>
        
        <div style={{ marginBottom: '20px' }}>
          <label>
            <input
              type="radio"
              value="transcribe"
              checked={mode === 'transcribe'}
              onChange={() => setMode('transcribe')}
            />
            {' '}Transcribe Audio
          </label>
          {' '}
          <label>
            <input
              type="radio"
              value="highlight"
              checked={mode === 'highlight'}
              onChange={() => setMode('highlight')}
            />
            {' '}Transcribe with Highlights
          </label>
        </div>

        <div className="file-input">
          <input 
            type="file" 
            accept=".mp3,.wav,.m4a,.ogg,.flac"
            onChange={handleFileChange}
          />
          <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
            Supported formats: MP3, WAV, M4A, OGG, FLAC
          </p>
        </div>

        {mode === 'highlight' && (
          <input
            type="text"
            className="input"
            placeholder="Enter keywords (comma separated)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
        )}

        <button 
          className="button"
          onClick={mode === 'transcribe' ? handleTranscribe : handleHighlight}
          disabled={loading}
        >
          {loading ? 'Processing...' : (mode === 'transcribe' ? 'Transcribe' : 'Transcribe & Highlight')}
        </button>

        {error && <p className="error" style={{ marginTop: '15px' }}>{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h2>Result</h2>
          <p><strong>File ID:</strong> {result.file_id}</p>
          <p><strong>Filename:</strong> {result.filename}</p>
          <p><strong>Language:</strong> {result.transcription?.language}</p>
          
          <div style={{ marginTop: '20px' }}>
            <h3>Full Transcription:</h3>
            <p style={{ 
              background: '#f5f5f5', 
              padding: '15px', 
              borderRadius: '5px',
              marginTop: '10px',
              lineHeight: '1.6'
            }}>
              {result.transcription?.text}
            </p>
          </div>

          {result.highlights && result.highlights.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <h3>Highlights ({result.highlights.length}):</h3>
              {result.highlights.map((highlight, index) => (
                <div key={index} style={{
                  background: '#fffacd',
                  padding: '10px',
                  borderRadius: '5px',
                  marginTop: '10px',
                  borderLeft: '3px solid #ffd700'
                }}>
                  <p><strong>Keyword:</strong> {highlight.keyword}</p>
                  <p><strong>Time:</strong> {highlight.start.toFixed(2)}s - {highlight.end.toFixed(2)}s</p>
                  <p><strong>Context:</strong> {highlight.context}</p>
                </div>
              ))}
            </div>
          )}

          <details style={{ marginTop: '20px' }}>
            <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
              View Detailed Segments
            </summary>
            <pre style={{ 
              background: '#f5f5f5', 
              padding: '15px', 
              borderRadius: '5px',
              overflow: 'auto',
              maxHeight: '400px',
              marginTop: '10px'
            }}>
              {JSON.stringify(result.transcription?.segments, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default AudioService;
