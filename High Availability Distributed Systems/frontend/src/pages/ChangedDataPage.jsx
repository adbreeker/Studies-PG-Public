import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import SearchForm from '../components/SearchForm';
import TrainList from '../components/TrainList';
import TrainDetailsChanges from '../components/TrainDetailsChanges';
import { useChanges } from '../contexts/ChangesContext';
import styles from '../styles/homePage.module.css';

export default function ChangedDataPage() {
  const [results, setResults] = useState(null);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [searchedQuery, setSearchedQuery] = useState({ from: '', to: '', date: '', time: '' });
  const [searchParams, setSearchParams] = useSearchParams();
  
  const { addChange, clearChanges } = useChanges();

  const selectedTrainId = searchParams.get('trainId');
  const selectedTrain = results?.find((train) => train.trainId === selectedTrainId);

  const handleSelectTrain = (train) => {
    setSearchParams({ trainId: train.trainId });
  };

  const handleGoBack = () => {
    setSearchParams({});
  };

  // Real-time changes polling
  useEffect(() => {
    if (!results || results.length === 0) return;

    let lastProcessedChangeId = null;

    const pollChanges = async () => {
      try {
        const response = await fetch('http://localhost:5222/api/changes/recent?count=1');
        if (!response.ok) return;
        
        const changes = await response.json();
        if (!changes || changes.length === 0) return;

        const latestChange = changes[0];
        
        // Only process if this is a new change
        if (!latestChange || latestChange.id === lastProcessedChangeId) return;
        
        lastProcessedChangeId = latestChange.id;
        
        // Add the change to global state
        addChange(latestChange);
        
        setResults(prevResults => {
          return prevResults.map(train => {
            // Apply new change if it matches this train
            if (latestChange.tripId === train.trainId.toString()) {
              console.log('New change applied and stored:', { 
                trainId: train.trainId, 
                changeType: latestChange.type,
                timestamp: latestChange.timestamp,
                changeId: latestChange.id
              });

              if (latestChange.type === 'PRICE_CHANGE') {
                return {
                  ...train,
                  price: `${latestChange.newPrice},00 PLN`,
                  priceChanged: true,
                  lastChangeTimestamp: latestChange.timestamp,
                  lastChangeId: latestChange.id
                };
              } else if (latestChange.type === 'AVAILABILITY_CHANGE') {
                return {
                  ...train,
                  available: latestChange.newAvailability,
                  availabilityChanged: true,
                  lastChangeTimestamp: latestChange.timestamp,
                  lastChangeId: latestChange.id
                };
              }
            }
            
            // Keep existing changes highlighted for other trains
            return train;
          });
        });
      } catch (error) {
        console.error('Error fetching changes:', error);
      }
    };

    // Register trains for changes
    const registerTrains = async () => {
      if (results && results.length > 0) {
        const trainIds = results.map(train => train.trainId.toString());
        try {
          await fetch('http://localhost:5222/api/changes/active-trains', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(trainIds)
          });
          console.log('Registered trains for live updates:', trainIds);
        } catch (changeError) {
          console.warn('Failed to register trains for changes:', changeError);
        }
      }
    };

    registerTrains();
    
    // Poll every 4 seconds
    const interval = setInterval(pollChanges, 8000);
    
    return () => clearInterval(interval);
  }, [results, addChange]);

  return (
    <div className={styles.container}>
      <h1 className='mainTitle'>Rail Rave - Live Updates</h1>
      {!selectedTrain && (
        <h3 style={{ marginTop: '-2rem' }}>Watch prices change in real-time! 🔄</h3>
      )}
      {!selectedTrain && (
        <>
          <SearchForm
            setResults={(res) => {
              setResults(res);
              setSearchedQuery({ from, to, date, time });
              // Clear changes when new search is performed
              clearChanges();
            }}
            from={from}
            setFrom={setFrom}
            to={to}
            setTo={setTo}
            date={date}
            setDate={setDate}
            time={time}
            setTime={setTime}
          />
          
          {/* Add Clear Highlights Button */}
          {results && results.some(train => train.priceChanged || train.availabilityChanged) && (
            <div style={{ textAlign: 'center', margin: '1rem 0' }}>
              <button 
                className="secondary"
                onClick={() => {
                  setResults(prevResults => 
                    prevResults.map(train => ({
                      ...train,
                      priceChanged: false,
                      availabilityChanged: false
                    }))
                  );
                }}
              >
                Clear All Highlights
              </button>
            </div>
          )}
          
          <TrainList 
            results={results} 
            searchQuery={searchedQuery} 
            onSelect={handleSelectTrain}
            showLiveUpdates={true}
          />
        </>
      )}
      {selectedTrain && (
        <TrainDetailsChanges 
          train={selectedTrain} 
          searchQuery={searchedQuery} 
          goBack={handleGoBack} 
        />
      )}
    </div>
  );
}