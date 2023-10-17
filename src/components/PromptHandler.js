// src/components/PromptHandler.js
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import InputField from './InputField';
import './Spinner.css';
import './PromptHandler.css';

function PromptHandler() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);  // Add state to track loading

  const handlePromptSubmit = async (prompt) => {
    setIsLoading(true);  // Set loading to true when request starts
      const response = await fetch('/api/generate-koan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();

    // Check if the koan was generated successfully before proceeding
    if (data.koan_id) {
      // Now call the /generate-image endpoint
        const imageResponse = await fetch('/api/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ koan_id: data.koan_id }),
      });
      const imageData = await imageResponse.json();
      if (imageData.image_url) {
        // Navigate to the koan page if the image was generated successfully
        navigate(`/koan/${data.koan_id}`);
        setIsLoading(false);  // Set loading to false when request completes
      } else {
        console.error('Failed to generate image:', imageData.error || 'Unknown error');
        setIsLoading(false);  // Set loading to false when request completes
      }
    } else {
      console.error('Failed to generate koan:', data.error || 'Unknown error');
      setIsLoading(false);  // Set loading to false when request completes
    }
  };

  return (
    <div className="prompt-container">
      <InputField onSubmit={handlePromptSubmit} />
      {isLoading && (  // Conditionally render loading overlay
        <div className="loading-overlay">
            <div className="spinner"></div>  {/* Spinner animation */}
            <div className="loading-text">Manifesting...</div>
        </div>
      )}
    </div>
  );
}

export default PromptHandler;
