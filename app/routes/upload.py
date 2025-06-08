from fastapi import APIRouter, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from app.services.s3_handler import save_text_to_s3

router = APIRouter()

@router.post("/upload-cover-letter")
async def upload_cover_letter(
    user_id: str = Form(...), #todo: implement user management and authentication
    past_letter_text: str = Form(...)
):
    try:
        result = save_text_to_s3(past_letter_text, user_id=user_id, category="cover_letter")
        if "error" in result:
            return JSONResponse(content={"error": result["error"]}, status_code=400)
        return JSONResponse(content={"success": True, "key": result["key"]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
