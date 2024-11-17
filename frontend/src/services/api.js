import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api'
});

export const getAddressInfo = (address) => 
  api.get(`/address/${address}`).then(res => res.data);

export const getPrices = () => 
  api.get('/prices').then(res => res.data);

export const setAlert = (alertData) => 
  api.post('/alerts', alertData).then(res => res.data);

export const removeAlert = (alertData) => 
  api.delete('/alerts', { data: alertData }).then(res => res.data);
