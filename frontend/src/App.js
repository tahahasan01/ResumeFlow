import React, { useState } from 'react';
import {
  Container,
  CssBaseline,
  Box,
  Typography,
  Button,
  CircularProgress,
  Paper,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  createTheme,
  ThemeProvider,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
} from '@mui/material';
import { CloudUpload as CloudUploadIcon, ExpandMore as ExpandMoreIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#76ff03',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b3b3b3',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
});

function KeyInfoCard({ result }) {
  if (!result) return null;
  const {
    name,
    email,
    mobile_number,
    education,
    experience,
    skills,
    certifications,
    projects,
  } = result;

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>Extracted Resume Information</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
        <Box>
          <Typography variant="subtitle2">Name</Typography>
          <Typography variant="body2">{name || 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Email</Typography>
          <Typography variant="body2">{email || 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Phone</Typography>
          <Typography variant="body2">{mobile_number || 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Education</Typography>
          <Typography variant="body2">{education ? (Array.isArray(education) ? education.join(', ') : education) : 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Experience</Typography>
          <Typography variant="body2">{experience ? (Array.isArray(experience) ? experience.join(', ') : experience) : 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Skills</Typography>
          <Typography variant="body2">{skills ? (Array.isArray(skills) ? skills.join(', ') : skills) : 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Certifications</Typography>
          <Typography variant="body2">{certifications ? (Array.isArray(certifications) ? certifications.join(', ') : certifications) : 'Not found'}</Typography>
        </Box>
        <Box>
          <Typography variant="subtitle2">Projects</Typography>
          <Typography variant="body2">{projects ? (Array.isArray(projects) ? projects.join(', ') : projects) : 'Not found'}</Typography>
        </Box>
      </Box>
    </Paper>
  );
}

function ResultsPanel({ result, loading, error }) {
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
      return (
          <Box sx={{textAlign: 'center', p: 4}}>
              <Typography variant="h5" color="error">An Error Occurred</Typography>
              <Typography variant="body1" color="text.secondary">{error}</Typography>
          </Box>
      );
  }

  if (!result) {
    return (
      <Box sx={{textAlign: 'center', p: 4}}>
        <Typography variant="h5" color="text.primary">Welcome!</Typography>
        <Typography variant="body1" color="text.secondary">Upload your resume to get started.</Typography>
      </Box>
    );
  }
  
  if (!result.ats_score) {
    return (
        <Box sx={{textAlign: 'center', p: 4}}>
            <Typography variant="h5" color="text.primary">Parsing Complete</Typography>
            <Typography variant="body1" color="text.secondary">The resume was parsed, but an ATS score could not be calculated.</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>Please check the developer console for the raw data.</Typography>
        </Box>
    );
  }

  return (
    <Box sx={{p: 4}}>
      <KeyInfoCard result={result} />
      <Typography variant="h5" color="text.primary">Good morning, Taha Hasan.</Typography>
      <Typography variant="body1" color="text.secondary">Welcome to your resume review.</Typography>
      
      <Paper elevation={2} sx={{ p: 2, my: 2 }}>
        <Typography variant="body1" color="text.secondary">Your resume scored {result.ats_score.overall_score} out of 100.</Typography>
        <LinearProgress variant="determinate" value={result.ats_score.overall_score} sx={{ my: 1 }} />
      </Paper>

      <TableContainer component={Paper} elevation={2}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Category</TableCell>
              <TableCell align="right">Score (out of 10)</TableCell>
              <TableCell>Comments</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {result.ats_score.details.map((item) => (
              <TableRow key={item.category}>
                <TableCell component="th" scope="row">
                  {item.category}
                </TableCell>
                <TableCell align="right">{item.score}</TableCell>
                <TableCell>{item.comment}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);
    try {
      const res = await fetch('http://localhost:8000/parse', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Error parsing resume');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              Modern Resume Parser
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Upload a resume and job description to get an ATS score.
            </Typography>
          </Box>
          <Grid container spacing={3} justifyContent="center">
            <Grid item xs={12}>
              <TextField
                label="Job Description (Optional)"
                multiline
                rows={4}
                fullWidth
                variant="outlined"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Button
                component="label"
                variant="contained"
                startIcon={<CloudUploadIcon />}
                fullWidth
              >
                Select File
                <input type="file" hidden accept=".pdf,.doc,.docx" onChange={handleFileChange} />
              </Button>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Button
                onClick={handleSubmit}
                disabled={!file || loading}
                variant="contained"
                color="primary"
                fullWidth
                endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <CheckCircleIcon />}
              >
                {loading ? 'Parsing...' : 'Upload & Parse'}
              </Button>
            </Grid>
          </Grid>
          {file && (
            <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
              Selected file: {file.name}
            </Typography>
          )}
          {error && (
            <Typography color="error" sx={{ mt: 2, textAlign: 'center' }}>
              {error}
            </Typography>
          )}
          <ResultsPanel result={result} loading={loading} error={error} />
        </Paper>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 4 }}>
          &copy; {new Date().getFullYear()} Resume Parser
        </Typography>
      </Container>
    </ThemeProvider>
  );
}

export default App;
