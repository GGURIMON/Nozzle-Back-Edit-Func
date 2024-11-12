import boto3
import logging
from botocore.exceptions import ClientError
import urllib
import base64
import botocore

bucket_name = "image-save-presigned-url-student03-v1"

s3 = boto3.client(
    's3',
    region_name="ap-northeast-2"
)



def download_file(filePath: str):
    destination_path = "/tmp/output" + filePath
    try:
        s3.download_file(bucket_name, filePath, destination_path)
        with open(destination_path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode("utf-8")
        return encoded_string
    except (botocore.exceptions.ClientError, IOError) as error:
        print(f"Error downloading file: {error}")
