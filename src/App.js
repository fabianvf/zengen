// src/App.js
import './App.css';  // Importing the CSS file
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import KoanDisplay from './components/KoanDisplay';
import HomePage from './components/HomePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage />} />
        <Route path="/koan/:id" element={<KoanDisplay />} />
      </Routes>
    </Router>
  );
}

export default App;
