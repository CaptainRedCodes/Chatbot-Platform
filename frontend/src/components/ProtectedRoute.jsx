import React from 'react';
import { Navigate } from 'react-router-dom';

const isTokenExpired = (token) => {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        // Check if token has expired
        if (payload.exp && payload.exp * 1000 < Date.now()) {
            return true;
        }
        return false;
    } catch {
        return true;
    }
};

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token');

    if (!token || isTokenExpired(token)) {
        // Clear invalid/expired token
        localStorage.removeItem('token');
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default ProtectedRoute;
