import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

export default function RequireAuth({ isLoggedIn, children }) {
  const location = useLocation();
  if (!isLoggedIn) {
    return <Navigate to="/account/login" state={{ from: location }} replace />;
  }
  return children;
}