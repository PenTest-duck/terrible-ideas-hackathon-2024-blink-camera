import React, { useEffect, useState } from 'react';
import './App.css';
import { Box, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { grey } from '@mui/material/colors';
import Carousel from 'react-material-ui-carousel';
import ImageGallery from './components/gallery';
import BigPhoto from './components/bigPhoto';
import { ListObjectsV2Command } from '@aws-sdk/client-s3';
import { S3_BUCKET_NAME, S3_MAX_KEYS, S3_REGION, s3Client } from './clients/s3-client';

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

  const getImagesFromS3 = () => {
    const command = new ListObjectsV2Command({
        Bucket: S3_BUCKET_NAME,
        MaxKeys: S3_MAX_KEYS,
    });

    s3Client.send(command).then(({Contents}) => {
      const tmpImages: string[] = [];
      Contents?.forEach((obj) => {
        tmpImages.push(`https://${S3_BUCKET_NAME}.s3.${S3_REGION}.amazonaws.com/${obj.Key}`);
      });
      setImages(tmpImages);
    })
  };
  
  useEffect(() => {
    getImagesFromS3()
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
