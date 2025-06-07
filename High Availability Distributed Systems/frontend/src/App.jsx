import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import AccountLoginPage from './pages/AccountLoginPage';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import AnalyticsPageSimple from './pages/AnalyticsPageSimple';
import AccountPage from './pages/AccountPage';
import ChangedDataPage from './pages/ChangedDataPage';
import AccountReservationsPage from './pages/AccountReservationsPage';
import RequireAuth from './components/RequireAuth';
import './styles/global.css';
import RecentChanges from './pages/RecentChanges';
import { ChangesProvider } from './contexts/ChangesContext';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem('isLoggedIn') === 'true';
  });
  const [accountId, setAccountId] = useState(() => {
    return localStorage.getItem('accountId');
  });
  const [email, setEmail] = useState(() => {
    return localStorage.getItem('email');
  });

  useEffect(() => {}, []);

  const handleLogin = (id, userEmail) => {
    setIsLoggedIn(true);
    setAccountId(id);
    setEmail(userEmail);
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('accountId', id);
    localStorage.setItem('email', userEmail);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setAccountId(null);
    setEmail(null);
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('accountId');
    localStorage.removeItem('email');
  };

  return (
    <ChangesProvider>
    <Router>
      <Navbar isLoggedIn={isLoggedIn} email={email} onLogout={handleLogout} />      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analytics" element={<AnalyticsPageSimple />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/account/login" element={<AccountLoginPage onLogin={handleLogin} />} />
        <Route path="/changed-data" element={<ChangedDataPage/>} />
        <Route path="/recent-changes" element={<RecentChanges />} />
        <Route
          path="/account"
          element={
            <RequireAuth isLoggedIn={isLoggedIn}>
              <AccountPage />
            </RequireAuth>
          }
        />
        <Route
          path="/account/reservations"
          element={
            <RequireAuth isLoggedIn={isLoggedIn}>
              <AccountReservationsPage accountId={accountId} />
            </RequireAuth>
          }
        />
      </Routes>
    </Router>
  );
    </ChangesProvider>
    );
}

export default App;
