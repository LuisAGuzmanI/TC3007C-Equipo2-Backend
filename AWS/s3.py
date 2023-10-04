import boto3
from fastapi import UploadFile
from os import environ

# Your AWS credentials and bucket name
aws_access_key = environ.get('AWS_ACCESS_KEY')
aws_secret_key = environ.get('AWS_SECRET_KEY')
bucket_name = environ.get('S3_BUCKET_NAME')

# Initialize AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

def upload_to_s3(dir: str, id: str, file: UploadFile, file_name: str):
    try:
        print(file)

        # Generate a unique file name
        file_path = f"{dir}/{id}/video-recognition/{file_name}"
        
        # Upload the file to S3
        s3.upload_fileobj(file.file, bucket_name, file_path)
        
        # Generate the S3 URL for the uploaded file
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"
        
        return {"message": "File uploaded successfully", "s3_url": s3_url}
    except Exception as e:
        return {"error": str(e)}
