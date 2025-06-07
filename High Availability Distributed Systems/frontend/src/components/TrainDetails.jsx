import React, { useState, useEffect } from 'react';
import * as signalR from '@microsoft/signalr';
import styles from '../styles/homePage.module.css';

const transactionManagerApi = '/api/transaction-manager'

export default function TrainDetails({ train, searchQuery, goBack }) {
  const [selectedCars, setSelectedCars] = useState([]);
  const [reservedCars, setReservedCars] = useState([]);
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
    }    const accountId = localStorage.getItem('accountId') || 'Guest';

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
      <p className={styles.trainInfo}>Departure: {train.departureScheduled}</p>
      <p className={styles.trainInfo}>Arrival: {train.arrivalScheduled}</p>
      <p className={styles.trainInfo}>Travel time: {train.travelTime}</p>
      <p className={styles.trainInfo}>Delayed: {train.delayed ? 'Yes' : 'No'}</p>
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