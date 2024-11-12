import base64
import json
import logging
from translate import translate_to_english
import boto3


model_id = "amazon.titan-image-generator-v2:0"
client = boto3.client("bedrock-runtime", region_name="us-east-1")

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def background_removal(original_image_base64):
    # 배경 제거 작업 수행
    try:
        request = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": base64.b64encode(original_image_base64).decode('utf-8')
            }
        })
        logger.info("Background removal request sent.")
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        return model_response["images"][0]
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
                "image": base64.b64encode(original_image_base64).decode('utf-8'),
                "text": translated_prompt,
                "maskImage": base64.b64encode(mask_image_base64).decode('utf-8')
            },
            "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 1024,
                    "width": 1024,
                    "cfgScale": 8.0
                }
        })
        logger.info("Inpainting request sent.")
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        return model_response["images"][0]
    except Exception as e:
        logger.error(f"Error in inpainting: {str(e)}")
        return {"error": str(e)}

def image_conditioning(original_image_base64, prompt):
    translate_prompt = translate_to_english(prompt)
    try:
        request=json.dumps( {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": translate_prompt,
                "conditionImage": base64.b64encode(original_image_base64).decode('utf-8'),
                "controlMode": "CANNY_EDGE",
                "controlStrength": 0.7
            },
            "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 1024,
                    "width": 1024,
                    "cfgScale": 8.0
                }
            })
        logger.info("Conditioning request sent.")
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        return model_response["images"][0]
    except Exception as e:
        logger.error(f"Error in Conditioning: {str(e)}")
        return {"error": str(e)}

def outpainting(original_image_base64, mask_image_base64, prompt):
    translate_prompt = translate_to_english(prompt)
    try:
        request = json.dumps({
                    "taskType": "OUTPAINTING",
                    "outPaintingParams": {
                        "image": base64.b64encode(original_image_base64).decode('utf-8'),
                        "text": translate_prompt,
                        "maskImage": base64.b64encode(mask_image_base64).decode('utf-8'),
                        "outPaintingMode": "DEFAULT"
                    },
                    "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 1024,
                    "width": 1024,
                    "cfgScale": 8.0
                }
                })
        logger.info("OutPainting request sent.")
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())
        return model_response["images"][0]
    except Exception as e:
        logger.error(f"Error in Conditioning: {str(e)}")
        return {"error": str(e)}