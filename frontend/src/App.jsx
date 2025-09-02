// src/App.jsx

import React, { useState, useEffect } from 'react';
import './App.css';

// --- SVG Icon Components (No changes here) ---
const GenerateIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="generate-icon"><path d="M12 3c-1.1 0-2 .9-2 2v2h4V5c0-1.1-.9-2-2-2z" /><path d="M18.8 9.2c.5-.5.8-1.2.8-2s-.3-1.5-.8-2l-1.6-1.6c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L12 5.2 10.8 4c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L5.2 5.6c-.5-.5-.8 1.2-.8 2s.3 1.5.8 2L4 10.8c-.5-.5-.8 1.2-.8 2s.3 1.5.8 2l1.6 1.6c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.2-1.2 1.2 1.2c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.6-1.6c.5-.5.8-1.2-.8-2s-.3-1.5-.8-2L18.8 9.2z" /><path d="m12 15-1.5 3L12 21l1.5-3L12 15z" /></svg>);
const ImageIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="placeholder-icon"><path d="M12 3c-1.1 0-2 .9-2 2v2h4V5c0-1.1-.9-2-2-2z" /><path d="M18.8 9.2c.5-.5.8-1.2.8-2s-.3-1.5-.8-2l-1.6-1.6c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L12 5.2 10.8 4c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L5.2 5.6c-.5-.5-.8 1.2-.8 2s.3 1.5.8 2L4 10.8c-.5-.5-.8 1.2-.8 2s.3 1.5.8 2l1.6 1.6c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.2-1.2 1.2 1.2c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.6-1.6c.5-.5.8-1.2-.8-2s-.3-1.5-.8-2L18.8 9.2z" /><path d="m12 15-1.5 3L12 21l1.5-3L12 15z" /></svg>);
const SpinnerIcon = () => (<svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>);

// --- Helper for fetching models ---
const fetchModels = async (endpoint, setModels, setError) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/${endpoint}`);
    if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
    const data = await response.json();
    setModels(data.models || []);
  } catch (e) {
    console.error(e);
    setError(`Could not load ${endpoint}. Ensure backend is running.`);
  }
};

// --- Main App Component ---
export default function App() {
  // State for form inputs
  const [prompt, setPrompt] = useState('A pixelated knight with sword, 16-bit style');
  const [negativePrompt, setNegativePrompt] = useState('blurry, low quality, modern, realistic');
  const [checkpointModel, setCheckpointModel] = useState('');
  const [loraModel, setLoraModel] = useState(''); // NEW: state for LoRA model

  // State for image generation
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState([]);
  const [error, setError] = useState(null);

  // State for the lists of models
  const [availableCheckpoints, setAvailableCheckpoints] = useState([]);
  const [availableLoras, setAvailableLoras] = useState([]); // NEW: state for LoRAs
  const [modelsLoading, setModelsLoading] = useState(true);
  const [modelsError, setModelsError] = useState(null);

  // useEffect to fetch all models on component load
  useEffect(() => {
    const loadAllModels = async () => {
      setModelsLoading(true);
      setModelsError(null);
      await Promise.all([
        fetchModels('checkpoints', setAvailableCheckpoints, setModelsError),
        fetchModels('loras', setAvailableLoras, setModelsError)
      ]);
      setModelsLoading(false);
    };
    loadAllModels();
  }, []);

  // Handler for generate button click
  const handleGenerateClick = async () => {
    if (!prompt || !checkpointModel) return;
    setIsGenerating(true);
    setGeneratedImages([]);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, negativePrompt, checkpointModel, loraModel }), // Send both models
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGeneratedImages(data.images.map((url, id) => ({ id, url })));

    } catch (e) {
      console.error("Failed to generate image:", e);
      setError(e.message);
    } finally {
      setIsGenerating(false);
    }
  };

  // --- Render ---
  return (
    <div className="app-container">
      <div className="content-wrapper">
        <header className="app-header">
          <h1 className="title">Pixel Art Generator</h1>
          <p className="subtitle">Transform your ideas into stunning pixel art for indie games</p>
        </header>

        <main className="main-content">
          <div className="settings-panel">
            <h2 className="panel-title"><span className="panel-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.9 5.8-5.8 1.9 5.8 1.9L12 18l1.9-5.8 5.8-1.9-5.8-1.9L12 3zM5 3l3.8 3.8M3 19l3.8-3.8M19 3l-3.8 3.8M21 19l-3.8-3.8" /></svg></span>Generation Settings</h2>

            <div className="form-group"><label htmlFor="prompt" className="form-label">Prompt</label><textarea id="prompt" rows="4" className="form-textarea" value={prompt} onChange={(e) => setPrompt(e.target.value)}></textarea></div>
            <div className="form-group"><label htmlFor="negative-prompt" className="form-label">Negative Prompt</label><textarea id="negative-prompt" rows="3" className="form-textarea" value={negativePrompt} onChange={(e) => setNegativePrompt(e.target.value)}></textarea></div>

            {/* Checkpoint Dropdown */}
            <div className="form-group">
              <label htmlFor="checkpoint-model" className="form-label">Checkpoint Model</label>
              <select id="checkpoint-model" className="form-select" value={checkpointModel} onChange={(e) => setCheckpointModel(e.target.value)} disabled={modelsLoading}>
                <option value="" disabled>{modelsLoading ? "Loading..." : "Select a checkpoint"}</option>
                {availableCheckpoints.map(model => <option key={model} value={model}>{model}</option>)}
              </select>
            </div>

            {/* NEW: LoRA Dropdown */}
            <div className="form-group">
              <label htmlFor="lora-model" className="form-label">LoRA Model (Optional)</label>
              <select id="lora-model" className="form-select" value={loraModel} onChange={(e) => setLoraModel(e.target.value)} disabled={modelsLoading}>
                <option value="">{modelsLoading ? "Loading..." : "None"}</option>
                {availableLoras.map(model => <option key={model} value={model}>{model}</option>)}
              </select>
            </div>

            {modelsError && <p className="error-text">{modelsError}</p>}
            <button onClick={handleGenerateClick} disabled={isGenerating || !checkpointModel} className="generate-button">{isGenerating ? (<><SpinnerIcon />Generating...</>) : (<><GenerateIcon />Generate Pixel Art</>)}</button>
          </div>

          <div className="image-panel">
            <h2 className="panel-title">Generated Images</h2><div className="image-display-area">{isGenerating ? (<div className="loading-state"><SpinnerIcon /><p>Generating your masterpiece...</p></div>) : error ? (<div className="placeholder-state" style={{ color: '#ef4444' }}><h3>Generation Failed</h3><p>{error}</p></div>) : generatedImages.length > 0 ? (<div className="image-grid">{generatedImages.map(image => (<div key={image.id} className="image-wrapper"><img src={image.url} alt={`Generated art ${image.id}`} className="generated-image" /></div>))}</div>) : (<div className="placeholder-state"><ImageIcon /><h3>No images generated yet</h3><p>Select a checkpoint and generate your first image!</p></div>)}</div>
          </div>
        </main>
      </div>
    </div>
  );
}

