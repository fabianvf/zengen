import React from 'react';

function ImageDisplay({ image }) {
  return (
    <div>
      <img src={image} alt="Generated Imagery" />
    </div>
  );
}

export default ImageDisplay;
