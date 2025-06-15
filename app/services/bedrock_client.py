import boto3
import os
import json

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
    return response["output"]["message"]["content"][0]["text"]

# get embedding for a given text using Amazon Titan Embed Text model
def get_embedding(text: str):
    body = {
        "inputText": text
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId="amazon.titan-embed-text-v1",
        accept="application/json",
        contentType="application/json"
    )

    embedding = json.loads(response["body"].read())["embedding"]
    return embedding
