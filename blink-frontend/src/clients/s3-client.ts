import { S3Client } from "@aws-sdk/client-s3";

export const S3_BUCKET_NAME = "terrible-idea-hackathon-2024-blink-camera";
export const S3_REGION = "us-east-2";
export const s3Client = new S3Client({
    region: S3_REGION,
    credentials: {
        accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID ?? "",
        secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY ?? "",
    },
});
