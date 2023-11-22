import boto3
from os import environ
import numpy as np
import cv2

# Your AWS credentials and bucket name
aws_access_key = environ.get('AWS_ACCESS_KEY')
aws_secret_key = environ.get('AWS_SECRET_KEY')
bucket_name = environ.get('S3_BUCKET_NAME')

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg'
}

# Initialize AWS S3 client
# s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# boto3 resource instead of client
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
bucket = s3.Bucket(bucket_name)

async def s3_upload(dir: str, key: str, contents: bytes):
    try:
        bucket.put_object(Key=key, Body=contents)
        
        # Generate the S3 URL for the uploaded file
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        
        return {"message": "File uploaded successfully", "s3_url": s3_url}
    except Exception as e:
        return {"error": str(e)}

def s3_download(key: str):
    try:
        response = s3.Object(bucket_name=bucket_name, key=key).get()['Body'].read()

        np_array = np.frombuffer(response, np.uint8)

        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        return image

    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return 0