import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import { dashboardAPI } from '../services/api';

function Analytics() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [riskData, setRiskData] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [analyticsResponse, riskResponse] = await Promise.all([
        dashboardAPI.getAnalytics(),
        dashboardAPI.getRiskAssessment(),
      ]);
      setAnalytics(analyticsResponse.data);
      setRiskData(riskResponse.data);
      setError(null);
    } catch (err) {
      setError('Gagal memuat data analytics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const { score_distribution, average_scores } = analytics || {};
  const { risk_summary, flagged_candidates } = riskData || {};

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Distribusi Rekomendasi
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Layak</Typography>
                <Typography variant="h5" color="success.main">
                  {score_distribution?.layak || 0}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Dipertimbangkan</Typography>
                <Typography variant="h5" color="warning.main">
                  {score_distribution?.dipertimbangkan || 0}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between">
                <Typography>Tidak Layak</Typography>
                <Typography variant="h5" color="error.main">
                  {score_distribution?.tidak_layak || 0}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Rata-rata Skor Komponen
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Overall</Typography>
                <Typography variant="h5">
                  {average_scores?.overall?.toFixed(1) || 0}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Etika Digital</Typography>
                <Typography variant="h6">
                  {average_scores?.digital_ethics?.toFixed(1) || 0}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography>Profesionalisme</Typography>
                <Typography variant="h6">
                  {average_scores?.professionalism?.toFixed(1) || 0}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between">
                <Typography>Sentimen</Typography>
                <Typography variant="h6">
                  {average_scores?.sentiment?.toFixed(1) || 0}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Risk Assessment Summary
            </Typography>
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography color="error" variant="h4">
                    {risk_summary?.high_risk || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    High Risk
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography color="warning.main" variant="h4">
                    {risk_summary?.medium_risk || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Medium Risk
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography color="success.main" variant="h4">
                    {risk_summary?.low_risk || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Low Risk
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Kandidat yang Memerlukan Perhatian
            </Typography>
            <Box sx={{ mt: 2 }}>
              {flagged_candidates?.slice(0, 10).map((candidate) => (
                <Box
                  key={candidate.candidate_id}
                  sx={{
                    p: 2,
                    mb: 1,
                    bgcolor: 'background.default',
                    borderRadius: 1,
                  }}
                >
                  <Box display="flex" justifyContent="space-between">
                    <Box>
                      <Typography variant="subtitle1">
                        {candidate.candidate_name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Skor: {candidate.overall_score?.toFixed(1)} | {candidate.recommendation}
                      </Typography>
                    </Box>
                    <Typography
                      variant="h6"
                      color={candidate.overall_score > 60 ? 'warning.main' : 'error.main'}
                    >
                      {candidate.overall_score?.toFixed(0)}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Analytics;
