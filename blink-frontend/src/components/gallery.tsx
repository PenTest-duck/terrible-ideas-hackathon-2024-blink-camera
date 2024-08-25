import { Box } from '@mui/material';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ModalImage from 'react-modal-image';

const styles = {
    container: {
        display: 'flex',        
        justifyContent: 'center',
        alignItems: 'center',      
        margin: 0,              
    }
};

interface ImageGalleryParams {
    images: string[];
}

const ImageGallery = ({ images }: ImageGalleryParams) => {
    return (
        <Box width="100%" height="100%" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <ImageList sx={{ width:"100%", height:"100%", paddingX: "4%" }} cols={3} gap={20}>
            {images.map((image) => (
                <ImageListItem key={image.split("/").at(-1)}>
                    <div style={styles.container}>
                    <ModalImage
                        small={image}
                        large={image}
                    />
                    </div>
                    
                </ImageListItem>
            ))}
            </ImageList>
            
        </Box>
    );
}

export default ImageGallery;