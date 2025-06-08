import boto3
import botocore
import uuid
from fastapi import UploadFile

s3 = boto3.client("s3")
S3_BUCKET = "cover-letter-storage"

# Function to check if an S3 object exists
def s3_object_exists(bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise

def save_text_to_s3(text: str, user_id: str, category: str = "cover_letter", filename: str = None):
    if not filename:
        filename = f"{uuid.uuid4().hex}.txt"
    key = f"{user_id}/{category}/{filename}"

    try:
        if s3_object_exists(S3_BUCKET, key):
            return {"error": "A file with that name already exists."}
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=text)
        return {"success": True, "key": key}
    except botocore.exceptions.ClientError as e:
        return {"error": f"S3 ClientError: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def save_file_to_s3(file: UploadFile, user_id: str, category: str = "cover_letter"):
    key = f"{user_id}/{category}/{file.filename}"
    try:
        if s3_object_exists(S3_BUCKET, key):
            return {"error": "A file with that name already exists."}
        s3.upload_fileobj(file.file, Bucket=S3_BUCKET, Key=key)
        return {"success": True, "key": key}
    except botocore.exceptions.ClientError as e:
        return {"error": f"S3 ClientError: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}