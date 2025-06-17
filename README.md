# 📝 Cover Letter Generator

An intelligent cover letter generator that customizes cover letters based on a user's CV, job description, and previously written cover letters. The system uses **retrieval-augmented generation (RAG)** to find past relevant cover letters and uses them as context for generating new ones.

Built with **FastAPI**, deployed on **AWS Lambda**, with vector search via **Pinecone**, and model inference using **AWS Bedrock**.

---

## 🚀 Features

- 📄 Upload or submit CVs and job descriptions
- ✨ AI-powered cover letter generation using Claude (via AWS Bedrock)
- 🧠 Memory: Stores past letters for context-aware generation
- 🗂️ File storage via Amazon S3
- 🔍 Vector search using Pinecone with Llama v2 embeddings
- ✏️ Cover letter refinement: Send feedback and get an improved version
- 👤 (Todo: Basic user management with support for AWS Cognito integration)

---

## 🧱 Tech Stack

| Component        | Stack / Service                      |
|------------------|--------------------------------------|
| API              | FastAPI + Mangum (for Lambda)        |
| Model Inference  | AWS Bedrock (Claude)                 |
| File Storage     | Amazon S3                            |
| Vector Search    | Pinecone (with llama-text-embed-v2 Embeddings)  |
| Serverless Infra | AWS Lambda + API Gateway             |
| User Auth (TODO) | AWS Cognito                          |

---
## 🧪 Prompt Evaluation with promptfoo

This project uses [promptfoo](https://github.com/promptfoo/promptfoo) to evaluate the quality and reliability of prompt engineering for cover letter generation. The configuration is in `promptfooconfig.yaml`.

- **Test Cases:** Located in `test_data/`, these provide real CVs, job descriptions, and past letters for evaluation.
- **Prompt Evaluation:** The main prompt is built in `app/services/prompt_builder.py:build_prompt` and tested with various inputs.
- **Providers:** Evaluations use the Bedrock Claude model.
- **Custom Grading:** A custom Python script (`evals/custom_llm_eval_cover_letter.py`) is used for model-graded evaluation, allowing for tailored quality checks.
- **How to Run:**
  1. Install promptfoo: `npm install -g promptfoo`
  2. Run: `promptfoo eval` (ensure AWS credentials are set in your environment)

See `promptfooconfig.yaml` for details and to add more test cases or prompt variations.

---

## Usage instructions
You can test the api [here](https://mebltwxoio5s546ogy3mjrh5yu0bqdco.lambda-url.eu-north-1.on.aws/docs). The API is deployed on AWS Lambda and can be accessed via the provided URL. There is no user authentication implemented yet, so to indicate who you are come up with your own user_id.

## 🧠 Future Roadmap

🤖 Improved AI features
- Give more context to refinement requests such as the CV, or relevant retrieved letters
- Try out different techniques such as promt chaining for better results
- Add support for multiple AI models

🔒 Authentication
- Add full AWS Cognito integration for user management
- Secure endpoints based on user auth

🧪 Developer Features
- Add unit and integration tests
- Add more examples to promptfoo for better evaluation

💻 Frontend
- Simple web UI for users to upload, generate, and review letters