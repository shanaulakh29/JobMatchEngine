from fastapi import Header, HTTPException, status
from resume_service.schemas import Resume
from resume_service.db import db_query
from typing import Optional

def get_user_id(user_id: str = Header(...)) -> str:
    """Extracts the user_ID from header. Used as a dependency"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID required")
    return user_id

def get_resume_info(resume_id: str, user_id: str) -> Optional[Resume]:
    """Gets information about resume for a specific user"""
    
    resume = db_query("SELECT s3_key, status, uploaded_at FROM resumes r WHERE r.user_id = %s AND r.id = %s", (user_id,resume_id))
    
    if not resume:
        raise HTTPException(status_code=401, detail="Resume not found")
    
    # unpack tuple
    s3_key, status, uploaded_at = resume

    return Resume(s3_key=s3_key, status=status, uploaded_at=uploaded_at)

def get_resume_status(resume_id: str, user_id: str) -> Optional[str]:
    query = db_query("SELECT status FROM resumes r WHERE r.user_id = %s AND r.id = %s", (user_id,resume_id))
    
    if not query:
        raise HTTPException(status_code=401, detail="Resume not found")
    # unpack
    status = query
    return status
    