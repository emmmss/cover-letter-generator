from fastapi import APIRouter, File, UploadFile, Form, Request, Depends
from fastapi.responses import JSONResponse
from app.services.document_store import save_and_index_text
from app.services.cognito_auth import get_current_user
router = APIRouter()

@router.post("/upload-cover-letter")
async def upload_cover_letter(
    past_letter_text: str = Form(...),
    user=Depends(get_current_user)
):
    try:
        user_id = user["sub"]
        result = save_and_index_text(past_letter_text, user_id, category="cover_letter")
        if "error" in result:
            return JSONResponse(content={"error": result["error"]}, status_code=400)
        return JSONResponse(content={"success": True, "doc_id": result["doc_id"]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
