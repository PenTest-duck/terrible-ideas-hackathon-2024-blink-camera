import React from 'react';
// import logo from './logo.svg';
import './App.css';
import { Box, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { grey } from '@mui/material/colors';
import Carousel from 'react-material-ui-carousel';

function App() {
  const theme = createTheme({
    palette: {
      background: {
        default: "black"
      },
      primary: {
        main: grey[100],
      },
    }
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box width="100%" flexDirection="column" paddingY="3%">
        <Box width="100%" justifyContent="center" alignItems="center">
          <Typography variant="h1" gutterBottom align="center" color="primary">Terrible Ideas Hackathon</Typography>
          <Typography variant="h4" gutterBottom align="center" color="primary">Check out the photos taken</Typography>
        </Box>
        <Carousel autoPlay={true}></Carousel>
      </Box>
    </ThemeProvider>
  );
}

export default App;
