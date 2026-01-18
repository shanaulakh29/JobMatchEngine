import logging
import os
from celery import Celery
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import urlparse
import pdfplumber
from docx import Document



load_dotenv()

celery=Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

@celery.task
def test_task():
    return "Celery worker OK!"

def bytes_to_text(file_bytes: bytes, filename: str) -> str:
    """
    Convert file bytes to plain text.
    Supports PDF, DOCX, TXT.
    """

    filename = filename.lower()

    # -------- PDF --------
    if filename.endswith(".pdf"):
        text_pages = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
        return "\n".join(text_pages)

    # -------- DOCX --------
    elif filename.endswith(".docx"):
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    # -------- TXT --------
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    else:
        raise ValueError("Unsupported file type")

@celery.task
def parse_resume(s3_url:str, user_id:str):
    print(f"Started parsing resume for user:{user_id}")
    s3_client = boto3.client('s3', region_name='ap-south-1')
    try:
        parsed = urlparse(s3_url)
        key = parsed.path.lstrip("/")
        filename = key.split("/")[-1]
        # Case 1: s3://bucket/key
        if parsed.scheme == "s3":
            bucket_name = parsed.netloc

        # Case 2: https://bucket.s3.amazonaws.com/key
        elif "s3" in parsed.netloc:
            bucket_name = parsed.netloc.split(".")[0]
            
        else:
            raise ValueError("Unsupported S3 URL format")

        print(f"Bucket: {bucket_name}")
        print(f"Key: {key}")

        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=key
        )

        # PDF bytes
        file_bytes = response["Body"].read()
        text = bytes_to_text(file_bytes, filename)

        print(f"Downloaded {len(file_bytes)} bytes from S3")


    except ClientError as e:
        print(f"AWS error: {e}")

    except Exception as e:
        print(f"General error: {e}")



# celery.conf.task_routes = {
#     "worker.celery_app.parse_resume": {"queue": "resume_queue"},
# }