import boto3
import logging
from botocore.exceptions import ClientError
import urllib
import base64
import botocore

bucket_name = "temp_name"

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

def upload_base64_to_s3(encoded_image: str, output_name: str):
    # Base64 문자열을 디코딩하여 바이너리 데이터로 변환
    image_data = base64.b64decode(encoded_image)

    # S3에 업로드
    s3.put_object(Bucket=bucket_name, Key=output_name, Body=image_data)
