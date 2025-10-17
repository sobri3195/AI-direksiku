import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Cancel as CancelIcon,
  People as PeopleIcon,
} from '@mui/icons-material';
import { dashboardAPI, screeningAPI } from '../services/api';

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [meritData, setMeritData] = useState(null);
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [meritResponse, statsResponse] = await Promise.all([
        dashboardAPI.getMeritDashboard(),
        screeningAPI.getStatistics(),
      ]);
      setMeritData(meritResponse.data);
      setStatistics(statsResponse.data);
      setError(null);
    } catch (err) {
      setError('Gagal memuat data dashboard');
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

  const { overview } = meritData || { overview: {} };
  const { recommendations, average_scores } = statistics || { recommendations: {}, average_scores: {} };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Merit ASN
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Ringkasan Analisis Jejak Digital Kandidat ASN
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <PeopleIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" variant="body2">
                    Total Kandidat
                  </Typography>
                  <Typography variant="h4">
                    {overview.total_candidates || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CheckCircleIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" variant="body2">
                    Layak
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {recommendations.layak || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <WarningIcon color="warning" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" variant="body2">
                    Dipertimbangkan
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {recommendations.dipertimbangkan || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CancelIcon color="error" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="text.secondary" variant="body2">
                    Tidak Layak
                  </Typography>
                  <Typography variant="h4" color="error.main">
                    {recommendations.tidak_layak || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Rata-rata Skor
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Skor Keseluruhan
                </Typography>
                <Typography variant="h5">
                  {average_scores.overall?.toFixed(1) || 0} / 100
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Etika Digital
                </Typography>
                <Typography variant="h6">
                  {average_scores.digital_ethics?.toFixed(1) || 0} / 100
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Profesionalisme
                </Typography>
                <Typography variant="h6">
                  {average_scores.professionalism?.toFixed(1) || 0} / 100
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Kandidat Teratas
            </Typography>
            {meritData?.top_candidates?.slice(0, 5).map((candidate, index) => (
              <Box
                key={candidate.candidate_id}
                sx={{
                  p: 2,
                  mb: 1,
                  bgcolor: 'background.default',
                  borderRadius: 1,
                }}
              >
                <Typography variant="subtitle2">
                  {index + 1}. {candidate.candidate_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Skor: {candidate.overall_score?.toFixed(1)} | {candidate.recommendation}
                </Typography>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
