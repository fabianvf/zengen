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
        <a href={"/koan/" + koan.koan_id} style={{textDecoration: 'none', color: 'inherit'}}>
          <div key={index} className="koan-item">
            <img src={koan.image_url} alt={koan.image_alt_text} />
            <div>{koan.koan_text}</div>
          </div>
        </a>
      ))}
    </div>
  );
}

export default KoanList;
