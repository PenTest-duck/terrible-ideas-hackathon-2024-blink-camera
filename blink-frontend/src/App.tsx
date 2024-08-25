import React, { useEffect, useState } from 'react';
import './App.css';
import { Box, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { grey } from '@mui/material/colors';
import Carousel from 'react-material-ui-carousel';
import ImageGallery from './components/gallery';
import BigPhoto from './components/bigPhoto';
import ImagesClient from './clients/images-client';

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

  const [images, setImages] = useState<string[]>([]);
  
  useEffect(() => {
    const imagesClient = new ImagesClient();
    imagesClient.listImages().then((urls) => setImages(urls));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box width="100%" flexDirection="column" paddingY="3%">
        <Box width="100%" justifyContent="center" alignItems="center">
          <Typography variant="h1" gutterBottom align="center" color="primary">Terrible Ideas Hackathon</Typography>
          <Typography variant="h4" gutterBottom align="center" color="primary">Check out the photos taken</Typography>
        </Box>
        <Carousel autoPlay={true}></Carousel>
        <BigPhoto images={images}/>
        <ImageGallery images={images} />
      </Box>
    </ThemeProvider>
  );
}

export default App;
