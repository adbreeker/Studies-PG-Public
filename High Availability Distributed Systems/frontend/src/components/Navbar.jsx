import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/navbar.module.css';
import NavbarAccount from './NavbarAccount';

export default function Navbar({ isLoggedIn, email, onLogout }) {
  return (
    <div className={styles.navbar}>
      <div className={styles.left}>        <Link to="/" className={styles.link}>
          Home
        </Link>        <Link to="/analytics" className={styles.link}>
          Analytics
        </Link>        <Link to="/about" className={styles.link}>
          About
        </Link>
        <a
          href="https://www.youtube.com/watch?v=-50NdPawLVY"
          className={styles.link}
          target="_blank"
          rel="noopener noreferrer"
        >
          MUSIC ♫
        </a>
        <a href="/changed-data" className={styles.link}>
          Changing data funcionality
        </a>
      </div>

      <NavbarAccount isLoggedIn={isLoggedIn} email={email} onLogout={onLogout} />
    </div>
  );
}