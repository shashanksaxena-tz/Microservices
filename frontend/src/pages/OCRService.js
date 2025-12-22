import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_OCR_SERVICE_URL || 'http://localhost:8001';

function OCRService() {
  const [file, setFile] = useState(null);
  const [searchTerms, setSearchTerms] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('extract'); // 'extract' or 'highlight'

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
    setResult(null);
  };

  const handleExtract = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/ocr/extract`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleHighlight = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    if (!searchTerms.trim()) {
      setError('Please enter search terms');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('search_terms', searchTerms);

    try {
      const response = await axios.post(`${API_URL}/ocr/highlight`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Highlighting failed');
    } finally {
      setLoading(false);
    }
  };

  const downloadHighlighted = () => {
    if (result?.download_url) {
      window.open(`${API_URL}${result.download_url}`, '_blank');
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">OCR Service</h1>
      
      <div className="card">
        <h2>Upload PDF for Processing</h2>
        
        <div style={{ marginBottom: '20px' }}>
          <label>
            <input
              type="radio"
              value="extract"
              checked={mode === 'extract'}
              onChange={() => setMode('extract')}
            />
            {' '}Extract Text with Coordinates
          </label>
          {' '}
          <label>
            <input
              type="radio"
              value="highlight"
              checked={mode === 'highlight'}
              onChange={() => setMode('highlight')}
            />
            {' '}Highlight Search Terms
          </label>
        </div>

        <div className="file-input">
          <input 
            type="file" 
            accept=".pdf"
            onChange={handleFileChange}
          />
        </div>

        {mode === 'highlight' && (
          <input
            type="text"
            className="input"
            placeholder="Enter search terms (comma separated)"
            value={searchTerms}
            onChange={(e) => setSearchTerms(e.target.value)}
          />
        )}

        <button 
          className="button"
          onClick={mode === 'extract' ? handleExtract : handleHighlight}
          disabled={loading}
        >
          {loading ? 'Processing...' : (mode === 'extract' ? 'Extract Text' : 'Highlight PDF')}
        </button>

        {error && <p className="error" style={{ marginTop: '15px' }}>{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h2>Result</h2>
          {mode === 'extract' ? (
            <div>
              <p><strong>File ID:</strong> {result.file_id}</p>
              <p><strong>Filename:</strong> {result.filename}</p>
              <p><strong>Total Pages:</strong> {result.extraction?.total_pages}</p>
              <details style={{ marginTop: '15px' }}>
                <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
                  View Extracted Text
                </summary>
                <pre style={{ 
                  background: '#f5f5f5', 
                  padding: '15px', 
                  borderRadius: '5px',
                  overflow: 'auto',
                  maxHeight: '400px',
                  marginTop: '10px'
                }}>
                  {JSON.stringify(result.extraction, null, 2)}
                </pre>
              </details>
            </div>
          ) : (
            <div>
              <p className="success">✓ PDF highlighted successfully!</p>
              <p><strong>File ID:</strong> {result.file_id}</p>
              <p><strong>Search Terms:</strong> {result.search_terms?.join(', ')}</p>
              <button 
                className="button" 
                style={{ marginTop: '15px' }}
                onClick={downloadHighlighted}
              >
                Download Highlighted PDF
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default OCRService;
