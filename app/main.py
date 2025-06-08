from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from app.utils import extract_text
from app.prompt_builder import build_prompt
from app.bedrock_client import generate_from_bedrock
from dotenv import load_dotenv
from mangum import Mangum
import os

load_dotenv()

app = FastAPI()
lambda_handler = Mangum(app)

@app.post("/generate")
async def generate_cover_letter(
    cv_text: str = Form(...),
    job_description: str = Form(...),
    past_letter_text: str = Form("")
):
    try:
        prompt = build_prompt(cv_text, job_description, past_letter_text)
        generated = generate_from_bedrock(prompt)
        return JSONResponse(content={"cover_letter": generated})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
# Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)