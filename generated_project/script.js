// script.js
// QuizMaster client-side bootstrap and utilities

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';

// Import page components (ensure these paths exist in the project)
import Home from './components/Home';
import Quiz from './components/Quiz';
import EditQuiz from './components/EditQuiz';
import Admin from './components/Admin';

/**
 * Utility wrapper around fetch that automatically attaches a JWT token
 * (if present) from localStorage to the Authorization header.
 *
 * @param {RequestInfo} input - URL or Request object
 * @param {RequestInit} [init={}] - Fetch options
 * @returns {Promise<Response>} - The fetch promise
 */
export function fetchWithAuth(input, init = {}) {
  const token = localStorage.getItem('jwtToken') || localStorage.getItem('token');
  const headers = new Headers(init.headers || {});
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  return fetch(input, { ...init, headers });
}

/**
 * Main application component that defines the client‑side routes.
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/quiz/:id" element={<Quiz />} />
      <Route path="/edit/:id" element={<EditQuiz />} />
      <Route path="/admin" element={<Admin />} />
    </Routes>
  );
}

// Bootstrap the React application
const rootEl = document.getElementById('root');
if (!rootEl) {
  console.error('QuizMaster: No element with id "root" found in the DOM.');
} else {
  const root = ReactDOM.createRoot(rootEl);
  root.render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  );
  console.log('QuizMaster: Application initialized successfully.');
}

// Register a service worker for offline capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/service-worker.js')
      .then(registration => {
        console.log('QuizMaster: Service worker registered.', registration);
      })
      .catch(error => {
        console.error('QuizMaster: Service worker registration failed.', error);
      });
  });
}
