// src/components/InputField.js
import React, { useState } from 'react';

function InputField({ onSubmit }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();  // Prevent the default form submission behavior
    onSubmit(prompt);
  };

  return (
    <form onSubmit={handleSubmit}>  {/* Add a form with a submit event handler */}
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button type="submit">Generate</button>  {/* Set the button type to submit */}
    </form>
  );
}

export default InputField;
