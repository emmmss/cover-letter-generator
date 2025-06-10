import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
pinecone_api_key=os.getenv("PINECONE_API_KEY")

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=pinecone_api_key)

#pinecone index
def get_index():
    index = pc.Index("cover-letter")
    return index

index = get_index()

def upsert_text(text: str, record_id: str, user_id: str, metadata: dict = None):
    """
    Upserts a text record into Pinecone using automatic embedding.

    Args:
        text (str): The text to embed and store.
        record_id (str): The unique ID for the record.
        user_id (str): Namespace (user-specific).
        metadata (dict, optional): Any additional metadata.

    Returns:
        dict: Upsert response from Pinecone.
    """
    if metadata is None:
        metadata = {}

    record = {
        "_id": record_id,
        "text": text
    }

    if metadata:
        record.update(metadata)

    index.upsert_records(
        namespace=user_id,
        records=[record]
    )

def get_similar_cover_letter_ids(query: str, user_id: str, top_k: int = 3) -> list[str]:
    matches = index.search(
        namespace=user_id,
        query={
            "inputs": {"text": query},
            "top_k": top_k,
            "filter": {"category": "cover_letter"}
        },
        fields=["_id"]
    )

    if not matches:
        return []

    return [item['_id'] for item in matches.result.hits]
