import React, { useState, useEffect } from 'react';
import './KoanList.css';

function KoanList() {
  const [koans, setKoans] = useState([]);

  useEffect(() => {
    async function fetchKoans() {
        const response = await fetch('/api/koans');
      const data = await response.json();
      setKoans(data.koans);
    }

    fetchKoans();
  }, []);

  return (
    <div className="koan-list">
      {koans.map((koan, index) => (
        <div key={index} className="koan-item">
          <img src={koan.image_url} alt={`Imagery for koan ${index}`} />
          <div>{koan.koan_text}</div>
        </div>
      ))}
    </div>
  );
}

export default KoanList;
