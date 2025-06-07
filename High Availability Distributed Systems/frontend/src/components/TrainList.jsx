import React, { useState, useEffect } from 'react';
import styles from '../styles/homePage.module.css';

function timeToMinutes(time) {
  if (!time || typeof time !== 'string' || !time.includes(':')) return NaN;
  const [h, m] = time.split(':').map(Number);
  return h * 60 + m;
}

export default function TrainList({ results = [], searchQuery, onSelect, changes = [], showLiveUpdates = false }) {
  const [showEarlier, setShowEarlier] = useState(false);

  useEffect(() => {
    setShowEarlier(false);
  }, [results]);

  if (results === null) return;
  else if (results.length === 0) return <p>No results found.</p>;

  const sortedResults = [...results].sort((a, b) => {
    const timeA = timeToMinutes(a.departureScheduled);
    const timeB = timeToMinutes(b.departureScheduled);
    return timeA - timeB;
  });

  const queryMinutes = timeToMinutes(searchQuery?.time);

  const filteredResults = showEarlier
    ? sortedResults
    : sortedResults.filter(
        train => timeToMinutes(train.departureScheduled) >= queryMinutes
      );

  if(filteredResults.length === 0 && !showEarlier){
    return (
      <div>
        {!showEarlier && sortedResults.length > 0 && (
          <button
            className="secondary"
            style={{ marginTop: '1rem' }}
            onClick={() => setShowEarlier(true)}
          >
            Show earlier trains
          </button>
        )}
        <p>No results found.</p>
      </div>
    );
  }

   return (
    <div>
      {showLiveUpdates && (
        <p className={styles.liveUpdates}>🔄 Live updates every 10 seconds</p>
      )}
      {!showEarlier && sortedResults.length > 0 && (
        <button
          className="secondary"
          style={{ marginTop: '1rem' }}
          onClick={() => setShowEarlier(true)}
        >
          Show earlier trains
        </button>
      )}
      <div className={styles.trainList}>
        {filteredResults.map((train) => {
          // Check for changes from the live updates (priceChanged and availabilityChanged are set directly on train object)
          const priceChange = changes.find(c => c.tripId === train.trainId && c.type === 'PRICE_CHANGE');
          const hasLivePriceChange = train.priceChanged || !!priceChange;
          const hasLiveAvailabilityChange = train.availabilityChanged;
          
          console.log('Live changes for train:', {
            trainId: train.trainId,
            priceChanged: train.priceChanged,
            availabilityChanged: train.availabilityChanged,
            oldPrice: train.price,
            newPrice: priceChange ? priceChange.newPrice : train.price
          });

          const currentPrice = priceChange ? priceChange.newPrice : train.price;

          return (
            <div 
              key={train.trainId} 
              className={`${styles.trainCard} ${hasLivePriceChange ? styles.priceChanged : ''} ${hasLiveAvailabilityChange ? styles.availabilityChanged : ''}`}
              onClick={() => onSelect(train)}
            >
              <div className={styles.trainHeader}>
                <h3 className={styles.trainTitle}>
                  {train.departureScheduled} → {train.arrivalScheduled}
                </h3>
                {hasLivePriceChange && (
                  <span className={styles.changeIndicator}>💰 Price Updated!</span>
                )}
                {hasLiveAvailabilityChange && (
                  <span className={styles.changeIndicator}>🚫 Availability Changed!</span>
                )}
              </div>
              
              <div className={styles.trainDetails}>
                <div className={styles.trainDetailRow}>
                  <small className={styles.trainDetailLabel}>Travel time:</small>
                  <small>{train.travelTime}</small>
                </div>
                <div className={styles.trainDetailRow}>
                  <small className={styles.trainDetailLabel}>Delayed:</small>
                  <small>{train.delayed ? 'Yes' : 'No'}</small>
                </div>
                <div className={styles.trainDetailRow}>
                  <small className={styles.trainDetailLabel}>Available:</small>
                  <small className={hasLiveAvailabilityChange ? styles.availabilityHighlight : ''}>
                    {train.available !== undefined ? (train.available ? 'Yes' : 'No') : 'Unknown'}
                  </small>
                </div>
                <div className={styles.trainDetailRow}>
                  <small className={styles.trainDetailLabel}>Price per train car:</small>
                  <small className={hasLivePriceChange ? styles.priceHighlight : ''}>
                    {currentPrice
                      ? `${(parseFloat(currentPrice.toString().replace(',', '.')) * 30).toFixed(2)} PLN`
                      : 'Price unknown'}
                    {hasLivePriceChange && <span className={styles.updateBadge}>Updated!</span>}
                  </small>
                </div>
              </div>
              <button className='secondary' onClick={() => onSelect(train)}>
                View Details
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}