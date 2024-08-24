import { ListObjectsV2Command, ListObjectsV2CommandOutput, S3Client } from '@aws-sdk/client-s3';
import { Box } from '@mui/material';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import { useEffect, useState } from 'react';

const BUCKET_NAME = "terrible-idea-hackathon-2024-blink-camera";
const REGION = "us-east-2";

const client = new S3Client({
    region: REGION,
    credentials: {
        accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID ?? "",
        secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY ?? "",
    },
});

function ImageGallery() {
    // From https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_ListObjectsWeb_section.html
    const [imageObjs, setImageObjs] = useState<Required<ListObjectsV2CommandOutput>["Contents"]>([]);

    const listImagesInS3 = () => {
        const command = new ListObjectsV2Command({
            Bucket: BUCKET_NAME,
            MaxKeys: 100,
        });

        client.send(command).then(({Contents}) => setImageObjs(Contents ?? []));
    };
    
    useEffect(() => {
        listImagesInS3()
    }, []);

    return (
        <Box width="100%"  height="100%" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <ImageList sx={{ width:"100%", height:"100%", padding:"5%" }} cols={4} gap={20}>
            {imageObjs.map((obj) => (
                <ImageListItem key={obj.Key}>
                    <img
                        srcSet={`https://${BUCKET_NAME}.s3.${REGION}.amazonaws.com/${obj.Key}`}
                        src={`https://${BUCKET_NAME}.s3.${REGION}.amazonaws.com/${obj.Key}`}
                        alt="test-image"
                        loading="lazy"
                    />
                </ImageListItem>
            ))}
            </ImageList>
            
        </Box>
    );
}

export default ImageGallery;