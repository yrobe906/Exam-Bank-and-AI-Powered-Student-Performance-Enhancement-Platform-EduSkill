// services/api.js
import axios from 'axios';

const api = axios.create({
baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(request => {
  // Try to get user token first, then admin token
  const userToken = localStorage.getItem('token');
  const adminToken = localStorage.getItem('admin_token') || sessionStorage.getItem('admin_token');
  
  const token = userToken || adminToken;
  
  if (token) {
    request.headers['Authorization'] = `Bearer ${token}`;
  }
  
  console.log('🚀 Request:', request.method.toUpperCase(), request.url);
  console.log('📦 Full URL:', `${request.baseURL || 'http://localhost:8000'}${request.url}`);
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('✅ Response:', response.status, response.config.url);
    return response.config.headers['Content-Type']?.includes('multipart/form-data') || response.config.data instanceof FormData ? response : response.data;
  },
  error => {
    console.error('❌ API Error:', error.response?.status, error.config?.url);
    console.error('Error details:', error.response?.data);
    return Promise.reject(error);
  }
);

export default api;