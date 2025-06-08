from fastapi import APIRouter, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from app.utils import extract_text
from app.services.prompt_builder import build_prompt
from app.services.bedrock_client import generate_from_bedrock
from app.services.s3_handler import save_text_to_s3

router = APIRouter()

@router.post("/generate")
async def generate_cover_letter(
        user_id: str = Form(...), #Todo: implement user management and authentication
        cv: UploadFile = File(...),
        job_description: str = Form(...),
        past_letter_text: str = Form("")
):
    try:
        # upload cover letter text to S3 if provided
        if past_letter_text.strip():
            result = save_text_to_s3(past_letter_text, category="cover_letter", user_id=user_id)
            if "key" in result:
                past_letter_text = result["key"]
                # upload the text to pinecone

            if "error" in result:
                return JSONResponse(content={"error": result["error"]}, status_code=400)
        cv_text = extract_text(cv)
        # build the prompt for the AI model and generate the cover letter
        prompt = build_prompt(cv_text, job_description, past_letter_text)
        generated = generate_from_bedrock(prompt)
        return JSONResponse(content={"cover_letter": generated})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
