import React, { useState, useEffect } from 'react';
import { useChanges } from '../contexts/ChangesContext';
import styles from '../styles/recentChanges.module.css';

export default function RecentChanges() {
  const { allChanges, getRecentChanges } = useChanges();
  const [displayChanges, setDisplayChanges] = useState([]);

  useEffect(() => {
    // Update display changes whenever allChanges updates
    setDisplayChanges(getRecentChanges(10));
  }, [allChanges, getRecentChanges]);

  const formatChange = (change) => {
    switch (change.type) {
      case 'PRICE_CHANGE':
        return `Price changed from ${change.oldPrice} PLN to ${change.newPrice} PLN`;
      case 'AVAILABILITY_CHANGE':
        return `Availability changed to ${change.newAvailability ? 'available' : 'unavailable'}`;
      default:
        return change.details;
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
      return `${diffInSeconds} seconds ago`;
    } else if (diffInSeconds < 3600) {
      return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    } else {
      return date.toLocaleString();
    }
  };

  return (
    <div className={styles.container}>
      <h1 className='mainTitle'>Recent Trip Changes</h1>
      <h3>Last 10 changes from live monitoring ({allChanges.length} total recorded)</h3>
      
      <div className={styles.changesList}>
        {displayChanges.length === 0 && (
          <p className={styles.noChanges}>
            No changes recorded yet. Go to the Live Updates page and search for trains to start monitoring!
          </p>
        )}
        {displayChanges.map(change => (
          <div 
            key={change.id} 
            className={`${styles.changeCard} ${styles[change.type.toLowerCase()]}`}
          >
            <div className={styles.changeHeader}>
              <span className={styles.changeType}>
                {change.type === 'PRICE_CHANGE' ? '💰 Price Change' : '🚫 Availability Change'}
              </span>
              <span className={styles.timestamp}>
                {formatTimestamp(change.timestamp)}
              </span>
            </div>
            <p className={styles.trainId}>Train ID: {change.tripId}</p>
            <p className={styles.details}>{formatChange(change)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}