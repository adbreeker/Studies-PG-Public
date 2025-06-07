import React, { createContext, useContext, useState } from 'react';

const ChangesContext = createContext();

export const useChanges = () => {
  const context = useContext(ChangesContext);
  if (!context) {
    throw new Error('useChanges must be used within a ChangesProvider');
  }
  return context;
};

export const ChangesProvider = ({ children }) => {
  const [allChanges, setAllChanges] = useState([]);

  const addChange = (change) => {
    setAllChanges(prevChanges => {
      // Check if this change already exists (by ID)
      const exists = prevChanges.some(existing => existing.id === change.id);
      if (exists) return prevChanges;

      // Add new change to the beginning
      const newChanges = [change, ...prevChanges];
      
      // Keep only the last 50 changes to prevent memory issues
      return newChanges.slice(0, 50);
    });
  };

  const clearChanges = () => {
    setAllChanges([]);
  };

  const getRecentChanges = (count = 10) => {
    return allChanges.slice(0, count);
  };

  return (
    <ChangesContext.Provider value={{
      allChanges,
      addChange,
      clearChanges,
      getRecentChanges
    }}>
      {children}
    </ChangesContext.Provider>
  );
};