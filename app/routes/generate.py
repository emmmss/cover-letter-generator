from fastapi import APIRouter, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from app.utils import extract_text
from app.services.prompt_builder import build_prompt
from app.services.bedrock_client import generate_from_bedrock
from app.services.s3_handler import get_text_from_s3
from app.services.pinecone_handler import get_similar_cover_letter_ids
from app.services.document_store import save_and_index_text

router = APIRouter()

@router.post("/generate")
async def generate_cover_letter(
        user_id: str = Form(...), #Todo: implement user management and authentication
        cv: UploadFile = File(...),
        job_description: str = Form(...),
        past_letter_text: str = Form("")
):
    try:
        # Step 1: Query Pinecone for similar cover letters
        similar_ids = get_similar_cover_letter_ids(query=job_description, user_id=user_id, top_k=3)

        # Step 2: Fetch full content from S3
        example_texts = []
        for doc_id in similar_ids:
            s3_key = f"{user_id}/cover_letter/{doc_id}.txt"
            text = get_text_from_s3(s3_key)
            if text:
                example_texts.append(text)

        # Step 3: Save submitted cover letter (if any)
        if past_letter_text.strip():
            result = save_and_index_text(past_letter_text, user_id, category="cover_letter")
            if "error" in result:
                return JSONResponse(content={"error": result["error"]}, status_code=400)

        # Step 4: Build prompt
        cv_text = extract_text(cv)
        prompt = build_prompt(cv_text, job_description, past_letter_text)

        # Step 5: Generate cover letter
        generated = generate_from_bedrock(prompt)
        return JSONResponse(content={"cover_letter": generated})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
