import boto3
from fastapi import UploadFile
import os
from os import environ
import io
import numpy as np
import cv2 as cv

# Your AWS credentials and bucket name
aws_access_key = environ.get('AWS_ACCESS_KEY')
aws_secret_key = environ.get('AWS_SECRET_KEY')
bucket_name = environ.get('S3_BUCKET_NAME')

# Initialize AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# boto3 resource instead of client
s3_ = boto3.resource('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

def upload_to_s3(dir: str, id: str, file: UploadFile, file_name: str):
    try:
        # Generate a unique file name
        file_path = f"{dir}/{id}/video-recognition/{file_name}"
        
        # Upload the file to S3
        s3.upload_fileobj(file, bucket_name, file_path, ExtraArgs={'ContentType': 'image/png'})
        
        # Generate the S3 URL for the uploaded file
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"
        
        return {"message": "File uploaded successfully", "s3_url": s3_url}
    except Exception as e:
        return {"error": str(e)}

def get_from_s3(dir: str, id: str):
    try:
        # Ruta del archivo
        file_path = f"{dir}/{id}/video-recognition"

        # Realizamos la petición para obtener el dataset correspondiente        
        response = s3.list_objects(Bucket=bucket_name, Prefix=file_path)
        # Se extraen las llaves de los archivos de la respuesta
        files = [obj['Key'] for obj in response.get('Contents', [])]

        # Realizamos la petición para obtener el dataset correspondiente
        bucket = s3_.Bucket(bucket_name)

        images = []
        # Extraemos las llaves de los archivos desde la respuesta
        for file_key in files:

            object = bucket.Object(file_key)

            # Descargamos la imagen desde s3
            file_stream = io.BytesIO()
            object.download_fileobj(file_stream)

            print("Content Type:", object.content_type)

            # Convertimos los bytes descargados a una imagen
            try:
                file_stream.seek(0)  # Reset the BytesIO object to the beginning
                img_array = np.frombuffer(file_stream.getvalue(), dtype=np.uint8)
                img = cv.imdecode(img_array, cv.IMREAD_COLOR)
                if img is not None:
                    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                    images.append(img)
                else:
                    print("Failed to decode image:", object.key)
            except Exception as e:
                print("Failed to decode image:", object.key, "|", str(e))

        # Retornamos las imagenes obtenidos
        return images

    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return []