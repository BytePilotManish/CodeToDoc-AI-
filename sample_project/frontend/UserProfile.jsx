import React, { useState, useEffect } from 'react';
import { useFetch } from './hooks/useFetch';
import { apiRequest } from './utils/api';

/**
 * UserProfile component displays user information and handles local state.
 * 
 * @param {string} userId - The ID of the user to display.
 * @param {string} theme - The visual theme (light/dark).
 */
const UserProfile = ({ userId, theme }) => {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mocking an API call
        setTimeout(() => {
            setUserData({ name: 'John Doe', email: 'john@example.com' });
            setLoading(false);
        }, 1000);
    }, [userId]);

    if (loading) return <div>Loading...</div>;

    return (
        <div style={{ color: theme === 'dark' ? 'white' : 'black' }}>
            <h1>{userData.name}</h1>
            <p>Email: {userData.email}</p>
        </div>
    );
};

export default UserProfile;
