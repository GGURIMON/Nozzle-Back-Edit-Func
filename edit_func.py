import base64
import json
import logging
from translate import translate_to_english
import boto3


model_id = "amazon.titan-image-generator-v2:0"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
client = boto3.client("bedrock-runtime", region_name="us-east-1")


def background_removal(original_image_base64):
    # 배경 제거 작업 수행
    try:
        request = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": original_image_base64
            }
        })
        logger.info("Background removal request sent.")
        return client.invoke_model(modelId=model_id, body=request)
    except Exception as e:
        logger.error(f"Error in background_removal: {str(e)}")
        return {"error": str(e)}
def inpainting(original_image_base64, mask_image_base64, prompt):
    translated_prompt = translate_to_english(prompt)
    try:
        # 인페인팅 작업 수행
        request = json.dumps({
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "image": original_image_base64,
                "text": translated_prompt,
                "maskImage": mask_image_base64
            }
        })
        logger.info("Inpainting request sent.")
        return client.invoke_model(modelId=model_id, body=request)
    except Exception as e:
        logger.error(f"Error in inpainting: {str(e)}")
        return {"error": str(e)}