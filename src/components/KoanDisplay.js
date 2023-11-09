// src/components/KoanDisplay.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {Helmet} from "react-helmet";
import PromptHandler from './PromptHandler';  // Import the PromptHandler component
import './PromptHandler.css';
import './KoanDisplay.css';  // Import the CSS file
import './Spinner.css';

function KoanDisplay() {
  const { id } = useParams();
  const [koan, setKoan] = useState(null);
  const [image, setImage] = useState(null);
  const [isImageLoading, setIsImageLoading] = useState(false);  // Add state to track loading

  useEffect(() => {
    const fetchKoan = async () => {
      const response = await fetch(`/api/koan/${id}`);
      if (!response.ok) {
        console.error(response)
        return
      }
      const data = await response.json();
      setKoan(data);
    };
    fetchKoan();
  }, [id]);

  useEffect(() => {
    const fetchImage = async () => {
      var needs_generation = false;
      if (koan && (!image || !image.image_url)) {
          needs_generation = true;
      }
      if (koan && koan.image_url) {
          const response = await fetch(koan.image_url);
          if (!response.ok) {
              needs_generation = true;
              setIsImageLoading(true);
              setImage(null);
          } else {
              needs_generation = false;
          }
      }
      if (needs_generation) {
        setIsImageLoading(true);
        // Now call the /generate-image because we don't have one yet
        const imageResponse = await fetch('/api/generate-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ koan_id: id }),
        });
        const imageData = await imageResponse.json();
        if (imageData.image_url) {
          setImage(imageData);
          setIsImageLoading(false);  // Set loading to false when request completes
        } else {
          setIsImageLoading(false);  // Set loading to false when request completes
        }
      } else {
        setImage(koan);
        setIsImageLoading(false);
      }
    };
  fetchImage();
  }, [id, koan]);

  return (
    <div>
        <Helmet>
            <meta property="og:title" content="ZenGen" />
            <meta property="og:description" content={koan && koan.koan}/>
            <meta property="og:image" content={image && image.image_url} />
        </Helmet>
        <PromptHandler />
        <div className="koan-display">
        {koan && (
            <React.Fragment>
                {(isImageLoading) ? (
                    <div className="koan-image">
                            <div className="spinner"></div>
                    </div>
                    ) : (
                        (image && <img src={image.image_url} alt={image.image_alt_text} />) || (<div></div>)
                    )
                }
                <div className="koan-text">{koan.koan}</div>
            </React.Fragment>
        )}
        </div>
    </div>
  );
}

export default KoanDisplay;
