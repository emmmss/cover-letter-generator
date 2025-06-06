from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from .utils import extract_text
from dotenv import load_dotenv
from mangum import Mangum
import uvicorn
import boto3
import json
import fitz  # PyMuPDF
import os

load_dotenv()

app = FastAPI()

# Lambda entrypoint
handler = Mangum(app)

# Use your preferred region where Bedrock is enabled
bedrock = boto3.client("bedrock-runtime", region_name="eu-north-1")

@app.post("/generate")
async def generate_cover_letter(
    cv: UploadFile = File(...),
    job_description: str = Form(...),
    past_letter: UploadFile = File(None)
):
    try:
        cv_text = extract_text(cv)
        past_letter_text = extract_text(past_letter) if past_letter else ""

        prompt = f"""
You're a cover letter generator AI.

Here's the job description:
{job_description}

Here is the candidate's CV:
{cv_text}

Here is a past cover letter (if any):
{past_letter_text}

Now generate a tailored, professional cover letter for this job.
"""

        response = bedrock.converse(
            modelId="eu.anthropic.claude-3-7-sonnet-20250219-v1:0",  # or the correct Claude 3 model ID
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

        generated = response["output"]["message"]["content"]
        return JSONResponse(content={"cover_letter": generated})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
