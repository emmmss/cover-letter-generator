from app.services.s3_handler import save_text_to_s3
from app.services.pinecone_handler import upsert_text

def save_and_index_text(
    text: str,
    user_id: str,
    category: str
) -> dict:
    """
    Save text to S3 and index it in Pinecone.

    Returns:
        {"success": True, "doc_id" ...} or {"error": "..."}
    """
    result = save_text_to_s3(text, user_id=user_id, category=category)

    if "key" in result:
        doc_id = result["key"]
        # upload the text to pinecone
        upsert_text(text, record_id=doc_id, user_id=user_id, metadata={"category": "cover_letter"})

    if "error" in result:
        return {"error": result["error"]}

    return {"success": True, "doc_id": doc_id}
