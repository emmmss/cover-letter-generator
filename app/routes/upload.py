from fastapi import APIRouter, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from app.services.document_store import save_and_index_text
router = APIRouter()

@router.post("/upload-cover-letter")
async def upload_cover_letter(
    user_id: str = Form(...), #todo: implement user management and authentication
    past_letter_text: str = Form(...)
):
    try:
        result = save_and_index_text(past_letter_text, user_id, category="cover_letter")
        if "error" in result:
            return JSONResponse(content={"error": result["error"]}, status_code=400)
        return JSONResponse(content={"success": True, "doc_id": result["doc_id"]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
