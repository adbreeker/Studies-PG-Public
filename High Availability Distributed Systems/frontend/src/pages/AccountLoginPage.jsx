import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from '../styles/accountPage.module.css';

const accountManagerApi = '/api/account-manager' 

export default function LoginPage({ onLogin }) {
  const location = useLocation();
  const navigate = useNavigate();
  const [isSigningIn, setIsSigningIn] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (location.state?.mode === 'signIn') {
      setIsSigningIn(true);
    } else {
      setIsSigningIn(false);
    }
  }, [location.state]);

  const toggleMode = () => {
    setIsSigningIn((prev) => !prev);
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setError('');
    setMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (isSigningIn) {
      // Sign In (Create Account)
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      try {
        const res = await fetch(`${accountManagerApi}/account/commands/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(errorText || 'Failed to create account');
        }

        const responseText = await res.text();
        setMessage(responseText); // "Account created successfully."

        // Automatically switch to login mode with the same email and password
        setIsSigningIn(false);
        setMessage('Account created successfully. Please log in.');
      } catch (err) {
        setError(err.message || 'An error occurred while creating the account');
        setEmail('');
        setPassword('');
        setConfirmPassword('');
      }
    } else {
      // Log In
      try {
        const res = await fetch(`${accountManagerApi}/account/commands/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (!res.ok) {
          const errorText = await res.json();
          throw new Error(errorText.message || 'Failed to log in');
        }

        const responseData = await res.json();
        setMessage(responseData.message);
        onLogin(responseData.accountId, email); // Pass accountId and email to parent
        navigate('/');
      } catch (err) {
        setError(err.message || 'An error occurred while logging in');
        setEmail('');
        setPassword('');
      }
    }
  };

  return (
    <div className={styles.loginPage}>
      <h1>{isSigningIn ? 'Sign In' : 'Log In'}</h1>
      <form className={styles.loginForm} onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {isSigningIn && (
          <label>
            Confirm Password:
            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </label>
        )}
        {error && <p className="errorMessage">{error}</p>}
        {message && <p className="successMessage">{message}</p>}
        <button type="submit" className="primary">
          {isSigningIn ? 'Sign In' : 'Log In'}
        </button>
      </form>
      <small onClick={toggleMode} className={styles.toggleMode}>
        {isSigningIn ? 'Already have an account? Log In' : "Don't have an account? Sign In"}
      </small>
    </div>
  );
}