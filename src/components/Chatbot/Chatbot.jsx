import React, { useState, useEffect } from 'react';
import ChatInterface from './ChatInterface';
import SelectionHandler from './SelectionHandler';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  // Function to handle text selection
  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
    }
  };

  // Add event listener for text selection
  useEffect(() => {
    const handleMouseUp = () => {
      setTimeout(handleTextSelection, 0); // Delay to ensure selection is complete
    };

    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return (
    <div className="chatbot-container">
      {!isOpen ? (
        <button
          className="chatbot-toggle"
          onClick={() => setIsOpen(true)}
        >
          💬 Ask about ROS 2
        </button>
      ) : (
        <div className="chatbot-panel">
          <div className="chatbot-header">
            <h3>ROS 2 Humanoid Robotics Assistant</h3>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>
          <ChatInterface
            selectedText={selectedText}
            onClearSelection={() => setSelectedText('')}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;