import React, { useState } from 'react';
import './App.css'; // Import the separated CSS file

// --- Helper Components (SVGs) ---
// These are kept in the JSX file as they are part of the component's structure.
const GenerateIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="generate-icon">
    <path d="M12 3c-1.1 0-2 .9-2 2v2h4V5c0-1.1-.9-2-2-2z" />
    <path d="M18.8 9.2c.5-.5.8-1.2.8-2s-.3-1.5-.8-2l-1.6-1.6c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L12 5.2 10.8 4c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L5.2 5.6c-.5.5-.8 1.2-.8 2s.3 1.5.8 2L4 10.8c-.5.5-.8 1.2-.8 2s.3 1.5.8 2l1.6 1.6c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.2-1.2 1.2 1.2c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.6-1.6c.5-.5.8-1.2.8-2s-.3-1.5-.8-2L18.8 9.2z" />
    <path d="m12 15-1.5 3L12 21l1.5-3L12 15z" />
  </svg>
);

const ImageIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="placeholder-icon">
    <path d="M12 3c-1.1 0-2 .9-2 2v2h4V5c0-1.1-.9-2-2-2z" />
    <path d="M18.8 9.2c.5-.5.8-1.2.8-2s-.3-1.5-.8-2l-1.6-1.6c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L12 5.2 10.8 4c-.5-.5-1.2-.8-2-.8s-1.5.3-2 .8L5.2 5.6c-.5.5-.8 1.2-.8 2s.3 1.5.8 2L4 10.8c-.5.5-.8 1.2-.8 2s.3 1.5.8 2l1.6 1.6c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.2-1.2 1.2 1.2c.5.5 1.2.8 2 .8s1.5-.3 2-.8l1.6-1.6c.5-.5.8-1.2.8-2s-.3-1.5-.8-2L18.8 9.2z" />
    <path d="m12 15-1.5 3L12 21l1.5-3L12 15z" />
  </svg>
);

const SpinnerIcon = () => (
  <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
);


// --- Main App Component ---
export default function App() {
  // State for form inputs
  const [prompt, setPrompt] = useState('A pixelated knight with sword, 16-bit style, fantasy game character...');
  const [negativePrompt, setNegativePrompt] = useState('blurry, low quality, modern, realistic...');
  const [checkpointModel, setCheckpointModel] = useState('');

  // State for image generation
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState([]);

  // Mock checkpoint models
  const checkpointModels = [
    { id: '1', name: 'PixelArt-V1.0' },
    { id: '2', name: 'RetroGame-V2.5' },
    { id: '3', name: 'FantasySprite-V3.1' },
  ];

  // --- Handlers ---
  const handleGenerateClick = () => {
    if (!prompt || !checkpointModel) {
      console.warn("Prompt and Checkpoint Model are required.");
      return;
    }

    setIsGenerating(true);
    setGeneratedImages([]);

    // Simulate an API call to generate images
    setTimeout(() => {
      const newImages = [
        { id: 1, url: 'https://placehold.co/512x512/2d3748/ffffff?text=Pixel+Knight+1' },
        { id: 2, url: 'https://placehold.co/512x512/2d3748/ffffff?text=Pixel+Knight+2' },
        { id: 3, url: 'https://placehold.co/512x512/2d3748/ffffff?text=Pixel+Knight+3' },
        { id: 4, url: 'https://placehold.co/512x512/2d3748/ffffff?text=Pixel+Knight+4' },
      ];
      setGeneratedImages(newImages);
      setIsGenerating(false);
    }, 2500); // Simulate a 2.5 second generation time
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
            <h2 className="panel-title">
              <span className="panel-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.9 5.8-5.8 1.9 5.8 1.9L12 18l1.9-5.8 5.8-1.9-5.8-1.9L12 3zM5 3l3.8 3.8M3 19l3.8-3.8M19 3l-3.8 3.8M21 19l-3.8-3.8" /></svg>
              </span>
              Generation Settings
            </h2>

            <div className="form-group">
              <label htmlFor="prompt" className="form-label">Prompt</label>
              <textarea
                id="prompt"
                rows="4"
                className="form-textarea"
                placeholder="e.g., A brave hero in a dark forest..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              ></textarea>
            </div>

            <div className="form-group">
              <label htmlFor="negative-prompt" className="form-label">Negative Prompt</label>
              <textarea
                id="negative-prompt"
                rows="3"
                className="form-textarea"
                placeholder="e.g., text, watermark, blurry..."
                value={negativePrompt}
                onChange={(e) => setNegativePrompt(e.target.value)}
              ></textarea>
            </div>

            <div className="form-group">
              <label htmlFor="checkpoint-model" className="form-label">Checkpoint Model</label>
              <select
                id="checkpoint-model"
                className="form-select"
                value={checkpointModel}
                onChange={(e) => setCheckpointModel(e.target.value)}
              >
                <option value="" disabled>Select a checkpoint model</option>
                {checkpointModels.map(model => (
                  <option key={model.id} value={model.id}>{model.name}</option>
                ))}
              </select>
            </div>

            <button
              onClick={handleGenerateClick}
              disabled={isGenerating || !prompt || !checkpointModel}
              className="generate-button"
            >
              {isGenerating ? (
                <>
                  <SpinnerIcon />
                  Generating...
                </>
              ) : (
                <>
                  <GenerateIcon />
                  Generate Pixel Art
                </>
              )}
            </button>
          </div>

          <div className="image-panel">
            <h2 className="panel-title">Generated Images</h2>
            <div className="image-display-area">
              {isGenerating ? (
                <div className="loading-state">
                  <SpinnerIcon />
                  <p>Generating your masterpiece...</p>
                </div>
              ) : generatedImages.length > 0 ? (
                <div className="image-grid">
                  {generatedImages.map(image => (
                    <div key={image.id} className="image-wrapper">
                      <img
                        src={image.url}
                        alt={`Generated pixel art ${image.id}`}
                        className="generated-image"
                        onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/512x512/ef4444/ffffff?text=Error'; }}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="placeholder-state">
                  <ImageIcon />
                  <h3>No images generated yet</h3>
                  <p>Enter a prompt and generate your first pixel art masterpiece!</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
