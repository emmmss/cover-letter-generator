from pydantic import BaseModel
from app.services.prompt_builder import build_refinement_prompt
from app.services.bedrock_client import generate_from_bedrock

class RefinementRequest(BaseModel):
    original_letter: str
    feedback: str
    job_description: str

class RefinementResponse(BaseModel):
    refined_letter: str

def refine_cover_letter(data: RefinementRequest) -> RefinementResponse:
    prompt = build_refinement_prompt(
        original_letter=data.original_letter,
        feedback=data.feedback,
        job_description=data.job_description
    )
    refined = generate_from_bedrock(prompt)
    return RefinementResponse(refined_letter=refined)
