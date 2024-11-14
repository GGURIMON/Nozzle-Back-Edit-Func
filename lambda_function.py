import json
import logging
from s3 import download_file, upload_base64_to_s3
from image_app import image_edit
import base64
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # POST 요청 본문에서 데이터 가져오기
        logger.info(event)
        # query_params = event.get("queryStringParameters", {})
        # edit_task = query_params.get("task", "")
        edit_task = event.get("task", None)
        logger.info(edit_task)
        prompt = event.get("prompt", None)
        logger.info(prompt)
        file_name = event.get("file_name", None)  # 원본 이미지 파일 경로
        logger.info(file_name)

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
        if edit_task == "bgrm":
            response = image_edit(original_image_base64, task="BACKGROUND_REMOVAL")
        elif edit_task == "conditioning":
            response = image_edit(original_image_base64, prompt, task = "IMAGE_CONDITIONING")
        elif edit_task == "outpaint":
            if not masked_image_name:
                return {
                    "statusCode": 400,
                    "body": json.dumps("Missing 'masked_image_name' for outpainting task.")
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
            logger.info(prompt)
            response = image_edit(original_image_base64, mask_image_base64, prompt)
            logger.info(response)
            logger.info(type(response))
            # result = base64.b64encode(response)
            # logger.info(result)

        random_number = random.randint(1, 10000)
        try:
            upload_base64_to_s3(response, f"output_image_{random_number}.jpg")
        except:
            pass
            
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