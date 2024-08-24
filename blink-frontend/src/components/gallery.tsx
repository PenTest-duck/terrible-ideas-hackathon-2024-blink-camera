import { ListObjectsV2Command, ListObjectsV2CommandOutput } from '@aws-sdk/client-s3';
import { Box } from '@mui/material';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ModalImage from "react-modal-image"
import { useEffect, useState } from 'react';
import { S3_BUCKET_NAME, S3_REGION, s3Client } from '../clients/s3-client';

const styles = {
    container: {
        display: 'flex',        
        justifyContent: 'center',
        alignItems: 'center',      
        margin: 0,              
    }
};

const ImageGallery = () => {
    const [imageObjs, setImageObjs] = useState<Required<ListObjectsV2CommandOutput>["Contents"]>([]);

    const listImagesInS3 = () => {
        const command = new ListObjectsV2Command({
            Bucket: S3_BUCKET_NAME,
            MaxKeys: 100,
        });

        s3Client.send(command).then(({Contents}) => setImageObjs(Contents ?? []));
    };
    
    useEffect(() => {
        listImagesInS3()
    }, []);

    return (
        <Box width="100%"  height="100%" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <ImageList sx={{ width:"100%", height:"100%", padding:"5%" }} cols={4} gap={20}>
            {imageObjs.map((obj) => (
                <ImageListItem key={obj.Key}>
                    <div style={styles.container}>
                    <ModalImage
                        small={`https://${S3_BUCKET_NAME}.s3.${S3_REGION}.amazonaws.com/${obj.Key}`}
                        large={`https://${S3_BUCKET_NAME}.s3.${S3_REGION}.amazonaws.com/${obj.Key}`}
                    />
                    </div>
                    
                </ImageListItem>
            ))}
            </ImageList>
            
        </Box>
    );
}

export default ImageGallery;