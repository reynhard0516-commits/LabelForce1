import os
import uuid
from typing import Tuple

USE_S3 = os.getenv("USE_S3", "false").lower() in ("1", "true", "yes")

if USE_S3:
    import boto3
    S3_BUCKET = os.getenv("S3_BUCKET")
    s3 = boto3.client("s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"))

def store_file(file_obj, filename: str) -> Tuple[str,str]:
    """
    Store file_obj (file-like) and return (url, storage_path)
    """
    ext = os.path.splitext(filename)[1]
    key = f"uploads/{uuid.uuid4().hex}{ext}"
    if USE_S3:
        s3.upload_fileobj(file_obj, S3_BUCKET, key, ExtraArgs={'ACL':'private'})
        url = f"s3://{S3_BUCKET}/{key}"
        return url, key
    else:
        os.makedirs("uploads", exist_ok=True)
        path = os.path.join("uploads", key.split("/")[-1])
        with open(path, "wb") as f:
            file_obj.seek(0)
            f.write(file_obj.read())
        return f"/uploads/{os.path.basename(path)}", path
