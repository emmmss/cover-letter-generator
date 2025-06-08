from fastapi import FastAPI
from dotenv import load_dotenv
from mangum import Mangum
from app.routes import generate, upload

load_dotenv()
app = FastAPI()

# Register routes
app.include_router(generate.router)
app.include_router(upload.router)

# Lambda entrypoint
lambda_handler = Mangum(app)

# Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)