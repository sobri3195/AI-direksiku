import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

const api = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const candidatesAPI = {
  getAll: (params = {}) => api.get('/candidates', { params }),
  getById: (id) => api.get(`/candidates/${id}`),
  create: (data) => api.post('/candidates', data),
  update: (id, data) => api.put(`/candidates/${id}`, data),
  delete: (id) => api.delete(`/candidates/${id}`),
};

export const screeningAPI = {
  startScreening: (candidateId, platforms = ['linkedin', 'twitter', 'facebook']) => 
    api.post('/screening/analyze', { 
      candidate_id: candidateId,
      platforms,
      deep_analysis: true 
    }),
  getResults: (candidateId) => api.get(`/screening/${candidateId}/results`),
  getResultById: (resultId) => api.get(`/screening/result/${resultId}`),
  getDigitalFootprints: (candidateId) => api.get(`/screening/${candidateId}/digital-footprints`),
  getStatistics: () => api.get('/screening/statistics/summary'),
};

export const dashboardAPI = {
  getMeritDashboard: () => api.get('/dashboard/merit'),
  getAnalytics: () => api.get('/dashboard/analytics'),
  getRiskAssessment: () => api.get('/dashboard/risk-assessment'),
};

export default api;
