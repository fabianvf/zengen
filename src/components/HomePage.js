import React from 'react';
import KoanList from './KoanList';
import PromptHandler from './PromptHandler';
import './HomePage.css';

function Homepage() {
  return (
    <div>
      <PromptHandler />  {/* Render PromptHandler here */}
      <div className="container">
        <KoanList />
      </div>
    </div>
  );
}

export default Homepage;
