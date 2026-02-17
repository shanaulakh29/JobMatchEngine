from fastapi import Header, HTTPException, status
from resume_service.schemas import Resume
from resume_service.db import db_query
from typing import Optional
from sentence_transformers import SentenceTransformer
import os
from datetime import datetime, timezone
from resume_service.db import db_execute
from worker.model_parser import parse_resume_raw
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import boto3
from urllib.parse import urlparse

load_dotenv()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_user_id(user_id: str = Header(..., alias="user_id")) -> str:
    """Extracts the user_ID from header. Used as a dependency"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID required")
    return user_id

def get_resume_info(resume_id: str, user_id: str) -> Optional[Resume]:
    """Gets information about resume for a specific user"""
    
    rows = db_query("SELECT s3_key, status, uploaded_at FROM resumes r WHERE r.user_id = %s AND r.id = %s", (user_id,resume_id))
    
    if not rows:
        raise HTTPException(status_code=401, detail="Resume not found")
    
    # unpack tuple
    s3_key, status, uploaded_at = rows[0]

    return Resume(s3_key=s3_key, status=status, uploaded_at=uploaded_at)

def get_resume_status(resume_id: str, user_id: str) -> Optional[str]:
    """Queries a resume from db"""
    rows = db_query("SELECT status FROM resumes r WHERE r.user_id = %s AND r.id = %s", (user_id,resume_id))
    
    if not rows:
        raise HTTPException(status_code=401, detail="Resume not found")
    # unpack
    status = rows[0]
    return status

def generate_embeddings(text: str):
    """Generates embeddings for a given string"""
    return model.encode(text).tolist()
 


def parse_resume(s3_url:str, user_id:str, resume_id: int) -> dict:
    """Parses a resume from S3 and generates embeddings"""
    print(f"Started parsing resume for user:{user_id}")
    s3_client = boto3.client('s3', region_name='ap-south-1')
    try:
        parsed = urlparse(s3_url)
        key = parsed.path.lstrip("/")
        filename: str = key.split("/")[-1]
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
        file_bytes: bytes = response["Body"].read()
        data: dict = parse_resume_raw(filename=filename, file_bytes=file_bytes)
        print("RESUME TEXT IS: \n")
        print(data)
        
        
        # insert the data into the database
        experience_combined = data['experience'] + data['projects']
        # Gather full resume data and generate embeds
        resume_combined = data['education'] + data['skills'] + experience_combined
        resume_embeddings = generate_embeddings(resume_combined)
        current_date = datetime.now(timezone.utc)
        # format data to insert
        cleaned = (resume_id,
            data['skills'],
            experience_combined,
            data['education'],
            resume_embeddings,
            current_date,)
        print("Inserting to db...")
        # insert into the database
        db_execute("INSERT INTO parsed_resumes (resume_id, skills, experience, education, embedding, parsed_at) VALUES (%s, %s, %s, %s, %s, %s)", cleaned)
        print(cleaned)
    

    except ClientError as e:
        print(f"AWS error: {e}")

    except Exception as e:
        print(f"General error: {e}")