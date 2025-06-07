import React from 'react';
import styles from '../styles/accountPage.module.css';
import { Link } from 'react-router-dom';

export default function AccountPage() {
  return (
    <div className={styles.container}>
      <h1 className="mainTitle">Account Page</h1>
      <div className={styles.accountContent}>
        <p className={styles.accountWelcome}>Welcome to your account!</p>
        <div className={styles.accountLinks}>
          <Link to="/account/reservations" className={styles.accountLink}>
            My Reservations
          </Link>
          <Link to="/recent-changes" className={styles.accountLink}>
            Recentl changes
          </Link>
        </div>
      </div>
    </div>
  );
}