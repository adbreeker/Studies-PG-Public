import React, { useState, useEffect } from 'react';
import { useChanges } from '../contexts/ChangesContext'; // Add this import
import * as signalR from '@microsoft/signalr';
import styles from '../styles/homePage.module.css';

const transactionManagerApi = '/api/transaction-manager'

export default function TrainDetailsChanges({ train, searchQuery, goBack }) {
  const [selectedCars, setSelectedCars] = useState([]);
  const [reservedCars, setReservedCars] = useState([]);
  const [showChangeHistory, setShowChangeHistory] = useState(false); // Add this
  
  const { allChanges } = useChanges(); // Add this

  // Filter changes for this specific train
  const trainChanges = allChanges.filter(change => 
    change.tripId === train.trainId.toString()
  ).slice(0, 20); // Show last 20 changes
  const [connection, setConnection] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');

  useEffect(() => {
    fetchReservedCars();
    
    // Setup SignalR connection
    const newConnection = new signalR.HubConnectionBuilder()
      .withUrl(`${transactionManagerApi}/trainReservationEventHub`, {
        skipNegotiation: false,
        transport: signalR.HttpTransportType.WebSockets | signalR.HttpTransportType.ServerSentEvents
      })
      .withAutomaticReconnect()
      .configureLogging(signalR.LogLevel.Information)
      .build();

    setConnection(newConnection);

    newConnection.start()
      .then(() => {
        console.log('SignalR connection established');
        setConnectionStatus('Connected');
        
        // Join the train-specific group
        newConnection.invoke("JoinTrainGroup", train.trainId.toString())
          .then(() => {
            console.log(`Joined train group: ${train.trainId}`);
          })
          .catch(err => {
            console.error('Error joining train group:', err);
          });
        
        // Subscribe to reservation notifications
        newConnection.on('ReceiveReservationNotification', (message) => {
          alert(`🚆 Train Reservation Update: ${message}`);
          // Refresh reserved cars when a new reservation is made
          setSelectedCars([]);
          fetchReservedCars();
        });
      })
      .catch(error => {
        console.error('SignalR connection failed:', error);
        setConnectionStatus('Failed');
      });

    // Handle reconnection events
    newConnection.onreconnecting(() => {
      setConnectionStatus('Reconnecting...');
    });

    newConnection.onreconnected(() => {
      setConnectionStatus('Connected');
      console.log('SignalR reconnected');
      // Rejoin the train group after reconnection
      newConnection.invoke("JoinTrainGroup", train.trainId.toString());
    });

    newConnection.onclose(() => {
      setConnectionStatus('Disconnected');
    });

    // Cleanup on component unmount
    return () => {
      if (newConnection) {
        // Leave the train group before disconnecting
        newConnection.invoke("LeaveTrainGroup", train.trainId.toString())
          .then(() => {
            console.log(`Left train group: ${train.trainId}`);
          })
          .catch(err => {
            console.error('Error leaving train group:', err);
          })
          .finally(() => {
            newConnection.stop();
          });
      }
    };
  }, [train.trainId, searchQuery.from, searchQuery.to, searchQuery.date, train.departureScheduled, train.arrivalScheduled]);

  const fetchReservedCars = async () => {
    try {
      // Validate and log the parameters
      if (!searchQuery.date || !train.departureScheduled || !train.arrivalScheduled) {
        console.error('Missing required parameters:', {
          date: searchQuery.date,
          departureTime: train.departureScheduled,
          arrivalTime: train.arrivalScheduled,
        });
        return;
      }

      // Combine date and time, and convert to UTC
      const departureDateTime = new Date(`${searchQuery.date}T${train.departureScheduled}`).toISOString();
      const arrivalDateTime = new Date(`${searchQuery.date}T${train.arrivalScheduled}`).toISOString();

      const apiUrl = `${transactionManagerApi}/reservation/queries/train-cars?trainId=${train.trainId}&departureStation=${searchQuery.from}&departureDate=${departureDateTime}&arrivalStation=${searchQuery.to}&arrivalDate=${arrivalDateTime}`;
      console.log('Checking reserved cars:', apiUrl);

      const response = await fetch(apiUrl);
      if (response.ok) {
        const data = await response.json();
        console.log('Currently reserved:', data);
        setReservedCars(data || []);
      } else {
        console.error('Failed to fetch reserved cars:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching reserved cars:', error);
    }
  };

  const handleReserveCar = async () => {
    if (selectedCars.length === 0) {
      alert('Please select at least one train car to reserve.');
      return;
    }

    const accountId = localStorage.getItem('accountId') || 'Guest';

    const payload = {
      accountId: accountId,
      trainId: train.trainId,
      departureDate: new Date(`${searchQuery.date}T${train.departureScheduled}`).toISOString(),
      departureStation: searchQuery.from,
      arrivalDate: new Date(`${searchQuery.date}T${train.arrivalScheduled}`).toISOString(),
      arrivalStation: searchQuery.to,
      trainCars: selectedCars,
    };

    try {
      // Get the connection ID to exclude from notifications
      const connectionId = connection?.connectionId;
      
      const response = await fetch(`${transactionManagerApi}/reservation/commands/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': '*/*',
          'X-SignalR-ConnectionId': connectionId || '',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const successText = await response.text();
        alert(`Reservation successful!: ${successText}`);
      } else {
        const errorText = await response.text();
        console.error('Failed to create reservation:', errorText);
        alert('Failed to create reservation. Please try again.');
      }
    } catch (error) {
      console.error('Error creating reservation:', error);
      alert('An error occurred while creating the reservation. Please try again.');
    }

    setSelectedCars([]);
    fetchReservedCars();
  };

  const toggleCarSelection = (carId) => {
    if (reservedCars.includes(carId)) return; // Prevent selecting reserved cars
    setSelectedCars((prevSelectedCars) => {
      const updatedCars = prevSelectedCars.includes(carId)
        ? prevSelectedCars.filter((id) => id !== carId) // Remove the car if already selected
        : [...prevSelectedCars, carId]; // Add the car if not selected

      return updatedCars.sort((a, b) => a - b); // Sort the array in ascending order
    });
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const formatChangeAge = (timestamp) => {
    const now = new Date();
    const changeTime = new Date(timestamp);
    const diffInMinutes = Math.floor((now - changeTime) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hours ago`;
    return `${Math.floor(diffInMinutes / 1440)} days ago`;
  };

  const trainCars = Array.from(
    { length: train.trainId.split(',')[0].trim().split('').map(Number).reduce((sum, n) => sum + n, 0) % 5 + 5 },
    (_, index) => ({
      id: index + 1,
      icon: index === 0 ? '/assets/icons/train1.png' : '/assets/icons/train2.png',
    })
  );

  return (
    <div className={styles.card}>
      <h2 className={styles.trainTitle}>Journey Details</h2>
      <h3 className={styles.trainSubTitle}>({searchQuery.from} → {searchQuery.to} : {searchQuery.date})</h3> 
      
      {/* Show change indicators if this train has recent changes */}
      {(train.priceChanged || train.availabilityChanged) && (
        <div style={{ 
          background: '#fff3cd', 
          padding: '0.5rem', 
          borderRadius: '4px', 
          margin: '0.5rem 0',
          border: '1px solid #ffeaa7'
        }}>
          {train.priceChanged && <div>💰 <strong>Price recently updated!</strong></div>}
          {train.availabilityChanged && <div>🚫 <strong>Availability recently changed!</strong></div>}
        </div>
      )}
      
      <p className={styles.trainInfo}>Departure: {train.departureScheduled}</p>
      <p className={styles.trainInfo}>Arrival: {train.arrivalScheduled}</p>
      <p className={styles.trainInfo}>Travel time: {train.travelTime}</p>
      <p className={styles.trainInfo}>Delayed: {train.delayed ? 'Yes' : 'No'}</p>
      
      {/* Add Change History Section */}
      <div style={{ margin: '1rem 0' }}>
        <button 
          className="secondary"
          onClick={() => setShowChangeHistory(!showChangeHistory)}
          style={{ marginBottom: '0.5rem' }}
        >
          {showChangeHistory ? '📈 Hide' : '📈 Show'} Change History ({trainChanges.length})
        </button>
        
        {showChangeHistory && (
          <div style={{ 
            background: '#f8f9fa', 
            padding: '1rem', 
            borderRadius: '8px',
            maxHeight: '300px',
            overflowY: 'auto',
            border: '1px solid #dee2e6'
          }}>
            <h4 style={{ margin: '0 0 1rem 0' }}>Price & Availability Changes</h4>
            {trainChanges.length === 0 ? (
              <p style={{ color: '#666', fontStyle: 'italic' }}>
                No changes recorded yet. Changes will appear here as they happen.
              </p>
            ) : (
              <div>
                {trainChanges.map((change, index) => (
                  <div key={`${change.id}-${index}`} style={{
                    background: 'white',
                    padding: '0.8rem',
                    marginBottom: '0.5rem',
                    borderRadius: '4px',
                    borderLeft: `4px solid ${change.type === 'PRICE_CHANGE' ? '#28a745' : '#dc3545'}`
                  }}>
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      marginBottom: '0.3rem'
                    }}>
                      <strong>
                        {change.type === 'PRICE_CHANGE' ? '💰 Price Change' : '🚫 Availability Change'}
                      </strong>
                      <small style={{ color: '#666', fontStyle: 'italic' }}>
                        {formatChangeAge(change.timestamp)}
                      </small>
                    </div>
                    <div style={{ marginBottom: '0.3rem' }}>
                      {change.details}
                    </div>
                    <small style={{ color: '#999', fontFamily: 'monospace' }}>
                      {formatTimestamp(change.timestamp)}
                    </small>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
      
      <div className={styles.trainCars}>
        {trainCars.map((car) => (
          <button
            key={car.id}
            className={`${styles.trainCarIcon} ${
              selectedCars.includes(car.id) ? styles.selectedCar : ''
            }`}
            style={{
              '--car-icon': `url(${car.icon})`,
            }}
            onClick={() => toggleCarSelection(car.id)}
            title={`Train car ${car.id}`}
            disabled={reservedCars.includes(car.id)} // Disable button for reserved cars
          ></button>
        ))}
      </div>
      <div className={styles.buttonGroup}>
        <button
          className="primary"
          onClick={handleReserveCar}
          disabled={selectedCars.length === 0}
        >
          Reserve{selectedCars.length > 0 && train.price
            ? ` ${(parseFloat(train.price.replace(',', '.')) * 30 * selectedCars.length).toFixed(2)} PLN`
            : ''}
        </button>
        <button className="secondary" onClick={goBack}>
          Back
        </button>
      </div>
    </div>
  );
}