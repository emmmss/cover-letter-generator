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

def upsert_record(text: str, record_id: str, namespace: str, metadata: dict = None):
    """
    Upserts a text record into Pinecone using automatic embedding.

    Args:
        text (str): The text to embed and store.
        user_id (str): Namespace (user-specific).
        category (str): Type of data (e.g., cover_letter).
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
        namespace=namespace,
        records=[record]
    )

def store_cover_letter_to_pinecone(past_letter_text: str, record_id: str, user_id: str
):
    """
    Stores a cover letter in Pinecone under the 'cover_letter' category.

    Args:
        text (str): The cover letter text.
        record_id (str): The unique ID for the record (should match S3 key).
        user_id (str): The namespace (usually the user ID).
        extra_metadata (dict, optional): Any additional metadata to attach.

    Returns:
        dict: Upsert response from Pinecone.
    """
    metadata = {"category": "cover_letter"}

    return upsert_record(
        text=past_letter_text,
        record_id=record_id,
        namespace=user_id,
        metadata=metadata
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
