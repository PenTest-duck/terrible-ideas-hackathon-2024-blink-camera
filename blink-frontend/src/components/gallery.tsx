import { Box } from '@mui/material';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';

function ImageGallery() {
    const images = require.context('../../public/photo/', false, /\.(png|jpg)$/);
    const imageList = images.keys().map(image => images(image));
    
    return (
        <Box width="100%"  height="100%" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <ImageList sx={{ width:"100%", height:"100%", padding:"5%" }} cols={4} gap={20}>
            {imageList.map((item) => (
                <ImageListItem key={item}>
                    <img
                        srcSet={item}
                        src={item}
                        alt={item.title}
                        loading="lazy"
                    />
                </ImageListItem>
            ))}
            </ImageList>
            
        </Box>
    );
}

export default ImageGallery;