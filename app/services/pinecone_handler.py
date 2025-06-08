import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()  # Safe to use in Lambda too if local


pinecone_api_key=os.getenv("PINECONE_API_KEY")

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=pinecone_api_key)

#pinecone index
def get_index():
    index = pc.Index("cover-letter")
    return index

index = get_index()

def store_cover_letter(user_id: str, text: str, metadata: dict = None):
    vector_id = str(uuid.uuid4())

    index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": text,  # raw text, Pinecone will embed it
                "metadata": {
                    "category": "cover_letter",
                    **(metadata or {})
                }
            }
        ],
        namespace=user_id
    )

    return vector_id

