import React, { useEffect, useState } from 'react';
import styles from '../styles/accountPage.module.css';

const transactionManagerApi = '/api/transaction-manager'

export default function AccountReservationsPage({ accountId }) {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelingId, setCancelingId] = useState(null);

  const fetchReservations = () => {
    if (!accountId) return;
    setLoading(true);
    fetch(`${transactionManagerApi}/reservation/queries/account/${accountId}`)
      .then(res => res.json())
      .then(data => setReservations(data))
      .catch(() => setReservations([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReservations();
  }, [accountId]);

  const handleCancel = async (reservationId) => {
    setCancelingId(reservationId);
    try {
      const res = await fetch(
        `${transactionManagerApi}/reservation/commands/${reservationId}`,
        { method: 'DELETE', headers: { accept: '*/*' } }
      );
      if (res.ok) {
        setReservations(prev => prev.filter(r => r.id !== reservationId));
      } else {
        alert('Failed to cancel reservation.');
      }
    } catch {
      alert('Error cancelling reservation.');
    } finally {
      setCancelingId(null);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.reservationsTitle}>Your Reservations</h2>
      <div className={styles.reservationsContent}>
        {!accountId && <div className={styles.accountMessage}>Please log in to view your reservations.</div>}
        {loading && <div className={styles.accountMessage}>Loading reservations...</div>}
        {!loading && reservations.length === 0 && <div className={styles.accountMessage}>No reservations found.</div>}
        {!loading && reservations.length > 0 && (
          <ul className={styles.reservationsList}>
            {reservations.map(r => (
              <li key={r.id} className={styles.reservationCard}>
                <div>
                  <span className={styles.reservationLabel}>Train:</span> {r.trainId}
                </div>
                <div>
                  <span className={styles.reservationLabel}>Date:</span>{' '}
                  {r.departureDate ? new Date(r.departureDate).toLocaleDateString() : ''}
                </div>
                <div>
                  <span className={styles.reservationLabel}>From:</span> {r.departureStation}
                  <span className={styles.reservationDate}>
                    {r.departureDate ? ` (${new Date(r.departureDate).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })})` : ''}
                  </span>
                </div>
                <div>
                  <span className={styles.reservationLabel}>To:</span> {r.arrivalStation}
                  <span className={styles.reservationDate}>
                    {r.arrivalDate ? ` (${new Date(r.arrivalDate).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })})` : ''}
                  </span>
                </div>
                <div>
                  <span className={styles.reservationLabel}>Cars:</span> {r.trainCars.join(', ')}
                </div>
                <button
                  className="secondary"
                  onClick={() => handleCancel(r.id)}
                  disabled={cancelingId === r.id}
                  style={{ marginTop: '1rem' }}
                >
                  {cancelingId === r.id ? 'Cancelling...' : 'Cancel Reservation'}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}