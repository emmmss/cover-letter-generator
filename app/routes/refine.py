from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.refinement import RefinementRequest, refine_cover_letter

router = APIRouter()

@router.post("/refine")
async def refine_endpoint(payload: RefinementRequest):
    try:
        result = refine_cover_letter(payload)
        return JSONResponse(content={"refined_letter": result.refined_letter})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
