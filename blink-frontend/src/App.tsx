import React, { useEffect, useState } from 'react';
import './App.css';
import { Box, Stack, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { grey } from '@mui/material/colors';
import ImageGallery from './components/gallery';
import BigPhoto from './components/bigPhoto';
import ImagesClient from './clients/images-client';
import BgPhoto from './assets/instagram-colour-background.png';

function App() {
  const theme = createTheme({
    palette: {
      primary: {
        main: grey[100],
      },
      secondary: {
        main: "#3f3838",
      },
    }
  });

  const [images, setImages] = useState<string[]>([]);
  
  useEffect(() => {
    const imagesClient = new ImagesClient();
    imagesClient.listImages().then((urls) => setImages(urls));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box 
        width="100%"
        flexDirection="column"
        paddingTop="3%"
        paddingBottom="1%"
        textAlign="center"
        sx={{
          backgroundImage:`url(${BgPhoto})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
          height: "100%",
        }}
      >
        <Typography variant="h1" fontWeight="bold" gutterBottom align="center" color="primary">Terrible Ideas Hackathon</Typography>
        <Typography variant="h3" color="primary" pb="1%">Capturing you in your "eye-catching" moment.</Typography>
        <Typography variant="h4" gutterBottom align="center" color="primary">
          <div style={{ fontSize: '28px', color: 'white', fontWeight: 'bold'  }}>
            Message from 👀
          </div>

          <div style={{fontSize:'20px', fontWeight:'bold'}}>
          "my health is IMPORTANT!!!   Click

          <a style={{ textDecoration: 'none', color:'white' }} rel="noopener noreferrer" target="_blank" href="https://www.health.gov.au/topics/eye-health-and-vision"> 
            <u style={{textDecoration:'none'}}> 🏥</u> for more info"
          </a>
          </div>
        </Typography>

        <BigPhoto images={images} />

        <Typography marginTop="3%" fontWeight="bold" color="primary">Click on each image to admire it in full screen.</Typography>
        <ImageGallery images={images} />

        <Stack flexDirection="row" paddingX="3%" justifyContent="space-between">
          <Typography color="secondary">Submission for the Terrible Ideas Hackathon 2024 @ UNSW.</Typography>
          <Typography color="secondary">Made with 👀 by Bianca Ren, Cameron McDonald, and Chris Yoo.</Typography>
        </Stack>
      </Box>
    </ThemeProvider>
  );
}

export default App;
