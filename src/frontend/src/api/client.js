import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
});

export const getImpact       = ()          => api.get('/disruptions/impact');
export const getDisruptions  = ()          => api.get('/disruptions');
export const reroute         = (id)        => api.post(`/shipments/${id}/reroute`);
export const getFleetIdle    = (region)    => api.get('/fleet/idle', { params: region ? { region } : {} });
export const getColdChain    = ()          => api.get('/coldchain/alerts');
export const agentQuery      = (query)     => api.post('/agent/query', { query });
