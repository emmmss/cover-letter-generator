import boto3
import os

region = os.getenv("BEDROCK_REGION", "eu-north-1")
model_id = os.getenv("BEDROCK_MODEL_ID", "eu.anthropic.claude-3-7-sonnet-20250219-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=region)

def generate_from_bedrock(prompt: str) -> str:
    response = bedrock.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 1000,
            "temperature": 0.7,
        }
    )
    return response["output"]["message"]["content"]
