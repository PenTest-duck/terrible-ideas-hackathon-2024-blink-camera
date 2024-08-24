import cv2
import boto3
from datetime import datetime

BUCKET_NAME = "terrible-idea-hackathon-2024-blink-camera"
s3_resource = boto3.resource('s3')

# Uploads an image to S3
def uploadToS3(image):
  timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
  key = timestamp + ".jpg"

  image_string = cv2.imencode('.jpg', image)[1].tostring()

  bucket = s3_resource.Bucket(BUCKET_NAME)
  bucket.put_object(
    Key = key,
    Body = image_string,
  )

  print("Upload Complete!")