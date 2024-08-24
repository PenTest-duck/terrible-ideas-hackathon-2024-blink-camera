import { Box } from '@mui/material';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ModalImage from "react-modal-image"

const styles = {
    container: {
      display: 'flex',        
      justifyContent: 'center',
      alignItems: 'center',      
      margin: 0,              
    }
  };

function ImageGallery() {
    const images = require.context('../../public/photo/', false, /\.(png|jpg)$/);
    const imageList = images.keys().map(image => images(image));

    return (
        <Box width="100%"  height="100%" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <ImageList sx={{ width:"100%", height:"100%", padding:"5%" }} cols={4} gap={20}>
            {imageList.map((item) => (
                <ImageListItem key={item}>
                    <div style={styles.container}>
                    <ModalImage
                        small={item}
                        large={item}
                    />
                    </div>
                    
                </ImageListItem>
            ))}
            </ImageList>
            
        </Box>
    );
}

export default ImageGallery;