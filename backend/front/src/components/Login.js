import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Container, Typography, TextField, Button, Grid, Box  } from "@mui/material";

const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/base/login/", {
        email: email,
        password: password,
      });

      console.log(response.data.message); // Message from the Django backend
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  const handleRegister = () => {
    // Navigate to the register page
    navigate("/register");
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
    >
      <Container component="main">
        <div>
          <Typography component="h2" variant="h5">
            Login
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
            <Button
              type="button"
              variant="contained"
              color="primary"
              onClick={handleLogin}
            >
              Login
            </Button>
            <Button
              type="button"
              variant="outlined"
              color="primary"
              onClick={handleRegister}
            >
              Register
            </Button>
          </form>
        </div>
      </Container>
    </Box>
  );
};

export default Login;
