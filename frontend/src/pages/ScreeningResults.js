import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { screeningAPI } from '../services/api';

function ScreeningResults() {
  const { candidateId } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);
  const [footprints, setFootprints] = useState([]);

  useEffect(() => {
    fetchScreeningData();
  }, [candidateId]);

  const fetchScreeningData = async () => {
    try {
      setLoading(true);
      const [resultsResponse, footprintsResponse] = await Promise.all([
        screeningAPI.getResults(candidateId),
        screeningAPI.getDigitalFootprints(candidateId),
      ]);
      setResults(resultsResponse.data);
      setFootprints(footprintsResponse.data);
      setError(null);
    } catch (err) {
      setError('Gagal memuat hasil screening');
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

  if (results.length === 0) {
    return (
      <Alert severity="info">
        Belum ada hasil screening untuk kandidat ini
      </Alert>
    );
  }

  const latestResult = results[0];

  const getRecommendationIcon = (recommendation) => {
    if (recommendation === 'layak') {
      return <CheckCircleIcon color="success" sx={{ fontSize: 60 }} />;
    } else if (recommendation === 'dipertimbangkan') {
      return <WarningIcon color="warning" sx={{ fontSize: 60 }} />;
    } else {
      return <CancelIcon color="error" sx={{ fontSize: 60 }} />;
    }
  };

  const getRecommendationColor = (recommendation) => {
    if (recommendation === 'layak') return 'success';
    if (recommendation === 'dipertimbangkan') return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Hasil Analisis Screening
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              {getRecommendationIcon(latestResult.recommendation)}
              <Typography variant="h5" sx={{ mt: 2 }}>
                Rekomendasi
              </Typography>
              <Chip
                label={latestResult.recommendation?.toUpperCase()}
                color={getRecommendationColor(latestResult.recommendation)}
                sx={{ mt: 1 }}
              />
              <Typography variant="h3" sx={{ mt: 2 }}>
                {latestResult.overall_score?.toFixed(1)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Skor Keseluruhan / 100
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Rincian Skor
            </Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Etika Digital
                </Typography>
                <Typography variant="h5">
                  {latestResult.digital_ethics_score?.toFixed(1)}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Profesionalisme
                </Typography>
                <Typography variant="h5">
                  {latestResult.professionalism_score?.toFixed(1)}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Sentimen
                </Typography>
                <Typography variant="h5">
                  {latestResult.sentiment_score?.toFixed(1)}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">
                  Sosial
                </Typography>
                <Typography variant="h5">
                  {latestResult.social_score?.toFixed(1)}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Analisis Sentimen
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 1 }}>
                <Typography>Positif</Typography>
                <Typography>
                  {((latestResult.positive_content_ratio || 0) * 100).toFixed(1)}%
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" sx={{ mb: 1 }}>
                <Typography>Netral</Typography>
                <Typography>
                  {((latestResult.neutral_content_ratio || 0) * 100).toFixed(1)}%
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between">
                <Typography>Negatif</Typography>
                <Typography>
                  {((latestResult.negative_content_ratio || 0) * 100).toFixed(1)}%
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Platform Media Sosial
            </Typography>
            <List>
              {footprints.map((footprint) => (
                <ListItem key={footprint.id}>
                  <ListItemText
                    primary={footprint.platform?.toUpperCase()}
                    secondary={`@${footprint.username} | ${footprint.post_count} posts`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Alasan Rekomendasi
            </Typography>
            <Typography
              variant="body1"
              sx={{ whiteSpace: 'pre-line', mt: 2 }}
            >
              {latestResult.recommendation_reason}
            </Typography>
          </Paper>
        </Grid>

        {latestResult.risk_flags && Object.keys(latestResult.risk_flags).length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="error">
                Indikator Risiko
              </Typography>
              <List>
                {Object.entries(latestResult.risk_flags).map(([key, value]) => (
                  <ListItem key={key}>
                    <ListItemText
                      primary={value.description}
                      secondary={`Tingkat: ${value.severity}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        )}

        {latestResult.positive_indicators && Object.keys(latestResult.positive_indicators).length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="success.main">
                Indikator Positif
              </Typography>
              <List>
                {Object.entries(latestResult.positive_indicators).map(([key, value]) => (
                  <ListItem key={key}>
                    <ListItemText primary={value.description} />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}

export default ScreeningResults;
