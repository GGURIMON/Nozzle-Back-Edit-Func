import json
import logging
from s3 import download_file
from image_app import image_edit
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # POST 요청 본문에서 데이터 가져오기
        logger.info(event)
        prompt = event.get("prompt").replace(" ","")
        logger.info(prompt)
        file_name = event.get("file_name", None)  # 원본 이미지 파일 경로
        logger.info(file_name)
        if '.' not in file_name:
            logger.error(f"Invalid file name format: {file_name}")
            return {
                "statusCode": 400,
                "body": json.dumps("Invalid file name format. Please include an extension (e.g., .jpg, .png).")
            }
        masked_name = file_name.split(".")
        masked_image_name = f"{masked_name[0]}_masked.{masked_name[1]}"
        # masked_image_name = body.get("masked_image_name", None)  # 마스킹 이미지 파일 경로

        if not prompt or not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps("Missing 'prompt' or 'file_name' in request body.")
            }

        # 원본 이미지 다운로드 및 Base64 인코딩
        original_image_base64 = download_file(file_name)
        if not original_image_base64:
            return {
                "statusCode": 500,
                "body": json.dumps("Failed to download original image from S3.")
            }

        # "배경 제거" 조건일 경우 bgrm 기능 실행
        if "배경제거" in prompt:
            response = image_edit(original_image_base64, task="BACKGROUND_REMOVAL")
        elif "컨디셔닝" in prompt:
            response = image_edit(original_image_base64, prompt, task = "IMAGE_CONDITIONING")
        elif "아웃페인팅" in prompt:
            if not masked_image_name:
                return {
                    "statusCode": 400,
                    "body": json.dumps("Missing 'masked_image_name' for inpainting task.")
                }

            # 마스킹 이미지 다운로드 및 Base64 인코딩
            mask_image_base64 = download_file(masked_image_name)
            if not mask_image_base64:
                return {
                    "statusCode": 500,
                    "body": json.dumps("Failed to download mask image from S3.")
                }
            response = image_edit(original_image_base64, mask_image_base64, prompt, task = "OUTPAINTING")

        else:
            if not masked_image_name:
                return {
                    "statusCode": 400,
                    "body": json.dumps("Missing 'masked_image_name' for inpainting task.")
                }

            # 마스킹 이미지 다운로드 및 Base64 인코딩
            mask_image_base64 = download_file(masked_image_name)
            if not mask_image_base64:
                return {
                    "statusCode": 500,
                    "body": json.dumps("Failed to download mask image from S3.")
                }

            # 인페인팅 기능 실행
            response = image_edit(original_image_base64, mask_image_base64, prompt)
            logger.info(response)
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"An unexpected error occurred: {str(e)}")
        }