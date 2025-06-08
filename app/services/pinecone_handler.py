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

#TODO: Implement the following functions
def upsert_document():
    pass

def query_similar_documents():
    pass

