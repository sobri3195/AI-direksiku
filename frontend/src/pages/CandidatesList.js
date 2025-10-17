import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
  IconButton,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as VisibilityIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { candidatesAPI, screeningAPI } from '../services/api';

function CandidatesList() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [screeningLoading, setScreeningLoading] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidatesAPI.getAll();
      setCandidates(response.data);
      setError(null);
    } catch (err) {
      setError('Gagal memuat data kandidat');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartScreening = async (candidateId) => {
    try {
      setScreeningLoading({ ...screeningLoading, [candidateId]: true });
      await screeningAPI.startScreening(candidateId);
      alert('Analisis screening berhasil dimulai!');
      fetchCandidates();
    } catch (err) {
      alert('Gagal memulai screening: ' + err.message);
    } finally {
      setScreeningLoading({ ...screeningLoading, [candidateId]: false });
    }
  };

  const getStatusChip = (status) => {
    if (status?.includes('layak')) {
      return <Chip label={status} color="success" size="small" />;
    } else if (status?.includes('dipertimbangkan')) {
      return <Chip label={status} color="warning" size="small" />;
    } else if (status?.includes('tidak_layak')) {
      return <Chip label={status} color="error" size="small" />;
    } else if (status === 'pending') {
      return <Chip label="Pending" color="default" size="small" />;
    }
    return <Chip label={status} size="small" />;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Daftar Kandidat
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/candidates/new')}
        >
          Tambah Kandidat
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nama</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>NIK</TableCell>
              <TableCell>Posisi</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Aksi</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {candidates.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography color="text.secondary">
                    Belum ada data kandidat
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              candidates.map((candidate) => (
                <TableRow key={candidate.id}>
                  <TableCell>{candidate.full_name}</TableCell>
                  <TableCell>{candidate.email}</TableCell>
                  <TableCell>{candidate.nik}</TableCell>
                  <TableCell>{candidate.applied_position}</TableCell>
                  <TableCell>{getStatusChip(candidate.status)}</TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/candidates/${candidate.id}`)}
                      title="Lihat Detail"
                    >
                      <VisibilityIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="secondary"
                      onClick={() => handleStartScreening(candidate.id)}
                      disabled={screeningLoading[candidate.id]}
                      title="Mulai Screening"
                    >
                      {screeningLoading[candidate.id] ? (
                        <CircularProgress size={20} />
                      ) : (
                        <AssessmentIcon />
                      )}
                    </IconButton>
                    {candidate.status?.includes('screened') && (
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/screening/${candidate.id}`)}
                        title="Lihat Hasil Screening"
                      >
                        <VisibilityIcon />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default CandidatesList;
