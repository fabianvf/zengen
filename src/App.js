// src/App.js
import './App.css';  // Importing the CSS file
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import PromptHandler from './components/PromptHandler';
import KoanDisplay from './components/KoanDisplay';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PromptHandler />} />
        <Route path="/koan/:id" element={<KoanDisplay />} />
      </Routes>
    </Router>
  );
}

export default App;
