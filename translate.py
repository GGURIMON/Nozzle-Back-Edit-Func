import boto3

translate = boto3.client('translate', region_name='us-east-1')

def translate_to_english(korean_text):
    response = translate.translate_text(
        Text=korean_text,
        SourceLanguageCode="ko",
        TargetLanguageCode="en"
    )
    return response['TranslatedText']