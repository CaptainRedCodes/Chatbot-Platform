import axios from 'axios';

const client = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    // Crucial for FastAPI
    withCredentials: true,
});

client.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.error("Unauthorized! Redirecting to login...");
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default client;