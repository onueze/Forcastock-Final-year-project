import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, TextField, Button, Grid } from '@mui/material';

const Register = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/base/register/', {
        email: email,
        password: password,
      });

      console.log(response.data.message); // Message from the Django backend

      // After successful registration, you can redirect to another page if needed
      navigate('/dashboard'); // Replace '/dashboard' with the desired route
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  const handleLoginRedirect = () => {
    // Navigate to the login page
    navigate('/login');
  };

  return (
    <Container component="main" maxWidth="xs">
      <div>
        <Typography component="h2" variant="h5">
          Register
        </Typography>
        <form>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                variant="outlined"
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                variant="outlined"
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Grid>
          </Grid>
          <Button type="button" variant="contained" color="primary" onClick={handleRegister}>
            Register
          </Button>
          <Button type="button" variant="outlined" color="primary" onClick={handleLoginRedirect}>
            Login
          </Button>
        </form>
      </div>
    </Container>
  );
};

export default Register;
