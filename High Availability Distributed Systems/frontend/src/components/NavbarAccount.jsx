import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/navbar.module.css';
import accountGuestImg from '../assets/icons/accountGuest.png';
import accountJohnImg from '../assets/icons/accountJohn.png';

export default function NavbarAccount({ isLoggedIn, email, onLogout }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  // Hide dropdown when clicking outside
  useEffect(() => {
    if (!isDropdownOpen) return;
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
      ) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isDropdownOpen]);

  const handleOptionClick = (action) => {
    if (action === 'logout') {
      onLogout();
      navigate('/account/login');
    } else if (action === 'login') {
      navigate('/account/login', { state: { mode: 'login' } });
    } else if (action === 'signIn') {
      navigate('/account/login', { state: { mode: 'signIn' } });
    }
    else if (action === 'myAccount'){
      navigate('/account')
    }
    else if (action === 'reservations'){
      navigate('/account/reservations')
    }
    setIsDropdownOpen(false);
  };

  const username = email ? email.split('@')[0] : 'Guest';

  return (
    <div className={styles.right} ref={dropdownRef}>
      <div className={styles.accountContainer} onClick={toggleDropdown}>
        <p className={styles.accountName}>{isLoggedIn ? username : 'Guest'}</p>
        <img
          src={isLoggedIn ? accountJohnImg : accountGuestImg}
          alt={isLoggedIn ? 'Account' : 'Guest'}
          className={styles.accountPicture}
        />
      </div>
      {isDropdownOpen && (
        <div className={styles.dropdownPanel}>
          {isLoggedIn ? (
            <>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('myAccount')}
              >
                My Account
              </button>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('reservations')}
              >
                Reservations
              </button>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('settings')}
              >
                Settings
              </button>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('logout')}
              >
                Log Out
              </button>
            </>
          ) : (
            <>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('login')}
              >
                Log In
              </button>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('signIn')}
              >
                Sign In
              </button>
              <button
                className={styles.dropdownButton}
                onClick={() => handleOptionClick('settings')}
              >
                Settings
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}