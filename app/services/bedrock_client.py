import boto3
import os
import json

region = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")
#model_id = os.getenv("BEDROCK_MODEL_ID", "eu.anthropic.claude-3-7-sonnet-20250219-v1:0")
# Default model for generation
DEFAULT_GENERATION_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0") # Updated default to 3.5 Sonnet

bedrock = boto3.client("bedrock-runtime", region_name=region)

def converse_with_bedrock(
    messages: list,
    model_id: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    stop_sequences: list = None # This parameter is correct here
) -> str:
    """
    Interacts with AWS Bedrock Converse API with flexible parameters.

    Args:
        messages (list): List of message dictionaries in Bedrock Converse format.
        model_id (str): Override the default model ID.
        temperature (float): Inference temperature.
        max_tokens (int): Max tokens for response.
        stop_sequences (list): List of strings to stop generation.

    Returns:
        str: The generated text from the model.
    """
    target_model_id = model_id if model_id else DEFAULT_GENERATION_MODEL_ID
    # Correctly place stopSequences inside inferenceConfig
    inference_config = {
        "maxTokens": max_tokens,
        "temperature": temperature,
    }
    if stop_sequences is not None and len(stop_sequences) > 0:
        inference_config["stopSequences"] = stop_sequences # <-- FIX IS HERE!

    response = bedrock.converse(
        modelId=target_model_id,
        messages=messages,
        inferenceConfig=inference_config, # Pass the constructed inference_config
        # stopSequences=stop_sequences_payload <-- REMOVE THIS LINE
    )
    return response["output"]["message"]["content"][0]["text"]

# Your original generate_from_bedrock can now be a wrapper around the more flexible function
def generate_from_bedrock(prompt_text: str) -> str:
    """
    Generates a cover letter using the default generation model and temperature.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt_text
                }
            ]
        }
    ]
    return converse_with_bedrock(messages, temperature=0.7)


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