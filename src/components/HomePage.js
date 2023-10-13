import React from 'react';
import KoanList from './KoanList';
import PromptHandler from './PromptHandler';
import './HomePage.css';

function Homepage() {
  return (
    <div className="container">
      <h1>Welcome to ZenGen</h1>
      <PromptHandler />  {/* Render PromptHandler here */}
      <KoanList />
    </div>
  );
}

export default Homepage;
