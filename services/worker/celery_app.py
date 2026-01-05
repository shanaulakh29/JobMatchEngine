import logging
import os
from celery import Celery
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
load_dotenv()

celery=Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

@celery.task
def test_task():
    return "Celery worker OK!"



@celery.task
def parse_resume(s3_url:str, user_id:str):
    print(f"Started parsing resume for user:{user_id}")
    s3_client = boto3.client('s3', region_name='ap-south-1')
    try:
        parsed = urlparse(s3_url)

        # Case 1: s3://bucket/key
        if parsed.scheme == "s3":
            bucket_name = parsed.netloc
            key = parsed.path.lstrip("/")

        # Case 2: https://bucket.s3.amazonaws.com/key
        elif "s3" in parsed.netloc:
            bucket_name = parsed.netloc.split(".")[0]
            key = parsed.path.lstrip("/")

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

        print(f"Downloaded {len(file_bytes)} bytes from S3")


    except ClientError as e:
        print(f"AWS error: {e}")

    except Exception as e:
        print(f"General error: {e}")



# celery.conf.task_routes = {
#     "worker.celery_app.parse_resume": {"queue": "resume_queue"},
# }