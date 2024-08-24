import { useEffect, useState } from "react";
import ModalImage from "react-modal-image"
import { S3_BUCKET_NAME, S3_REGION, s3Client } from "../clients/s3-client";
import { ListObjectsV2Command, ListObjectsV2CommandOutput } from "@aws-sdk/client-s3";

const styles = {
    container: {
      display: 'flex',        
      justifyContent: 'center',
      alignItems: 'center',  
      height: '100vh',         
      margin: 0,              
    }
  };

const BigPhoto = () => {
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

    const numPic = imageObjs.length;
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const Id = setInterval(()=>{
            setCurrentIndex(currentIndex === numPic ? 0 : currentIndex + 1);
        }, 2000);

        return () => clearInterval(Id);
    }, [currentIndex, numPic]);

    return (
        <div style={styles.container}>
            <ModalImage
                small={`https://${S3_BUCKET_NAME}.s3.${S3_REGION}.amazonaws.com/${imageObjs[currentIndex]?.Key}`}
                large={`https://${S3_BUCKET_NAME}.s3.${S3_REGION}.amazonaws.com/${imageObjs[currentIndex]?.Key}`}
            />
        </div>
    );
}

export default BigPhoto;