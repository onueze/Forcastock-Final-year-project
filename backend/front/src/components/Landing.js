import React from 'react';
import { Box, Typography, Button, Grid, Avatar } from '@mui/material';
import { Link } from 'react-router-dom';
import stockgraphImage from '../images/stockgraph.jpg'; 
import logoImage from '../images/logopng/logo-no-background.png'


const LandingPage = () => {

  return (
    <Box 
    textAlign="center" 
    p={6}
    style={{
        backgroundImage: `url(${stockgraphImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    }}
        >
      <img src={logoImage} alt="Forcastock Logo" style={{ width: '30%', marginBottom: '2px' }} />

      <Grid container spacing={2} mt={4}>
        {[
          {
            title: 'Trading with perspective',
            description: 'Dive into the stock market and explore the dynamics',
          },
          {
            title: 'Streak Mechanism for engagement',
            description: 'Enhance your daily financial and psychological awareness with Forcastock`s unique streak mechanism. Stay engaged with the stock market as the streak feature prompts and encourages you to place trades regularly, fostering a consistent and informed approach to your trading journey.',
          },
          {
            title: 'Machine Learning Enhanced Stock Prediction',
            description: 'Experience a new level of precision in your trading decisions with Forcastock\'s machine learning enhanced stock prediction. Our advanced algorithms analyze real-time market data, providing you with accurate insights into trends. Elevate your trading strategy with the power of machine learning and stay ahead in the stock market game.'
          }
          
          
        ].map((item, index) => (
          <Grid key={index} item xs={12} md={4}>
            <Box
              height="100%"
              display="flex"
              flexDirection="column"
              justifyContent="space-between"
              p={3}
              borderRadius={12}
              boxShadow={5}
              
            >
              <Box mb={2}>{item.icon}</Box>
              <Typography variant="h6" gutterBottom>
                {item.title}
              </Typography>
              <Typography>
                {item.description}
              </Typography>
              <Button variant="contained" component={Link} to="/register">
                Get Started
              </Button>
            </Box>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default LandingPage;



