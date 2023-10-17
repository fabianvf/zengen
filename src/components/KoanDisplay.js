// src/components/KoanDisplay.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import PromptHandler from './PromptHandler';  // Import the PromptHandler component
import './KoanDisplay.css';  // Import the CSS file

function KoanDisplay() {
  const { id } = useParams();
  const [koan, setKoan] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    const fetchKoan = async () => {
        const response = await fetch(`/api/koan/${id}`);
      const data = await response.json();
      setKoan(data.koan);
      setImageUrl(data.image_url);
    };
    fetchKoan();
  }, [id]);

  return (
    <div>
        <PromptHandler />
        <div className="koan-display">
        {koan && (
            <React.Fragment>
                {imageUrl && <div className="koan-image"><img src={imageUrl} alt="Koan imagery" /></div>}
            <div className="koan-text">{koan}</div>
            </React.Fragment>
        )}
        </div>
    </div>
  );
}

export default KoanDisplay;
