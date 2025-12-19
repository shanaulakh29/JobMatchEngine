from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from resume_service.db import init_db,  db_execute
from resume_service.bucket import upload_s3, create_presigned_url
import logging
from resume_service.dependencies import get_user_id, get_resume_info, get_resume_status
from datetime import datetime, timezone

# build tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan, title="Resume Service")

# document validations
ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
MAX_FILE_SIZE_MB=5

# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "This is the Resume Service for JobMatchEngine", 
            "status": "Running OK"
            }

# resume upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_user_id)):
    
    # check if allowed content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF, DOCX or TXT files are allowed")
    
    contents = await file.read()
    file_size = len(contents)
        
    # check if < 5MM
    file_size_mb = file_size / (1024 *1024) # type: ignore
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="file size must be within 5MB")
    
    file_name = file.filename
   
    # reset seek pointer
    await file.seek(0)
    
    # upload to AWS S3
    if not await upload_s3(file, file_name): # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="unable to upload file at this time")
    
    # generate a S3 url
    s3_url = await create_presigned_url(file_name)  # type: ignore
    logging.info("S3_URL: ", s3_url)
    
    dt = datetime.now(timezone.utc)
    params=(
        user_id,
        s3_url,
        dt
    )
    
    # upload to the resumes table with userID connected
    db_execute("INSERT INTO resumes (user_id, s3_key, uploaded_at) VALUES(%s, %s, %s)", params)
    
    
    # TODO: push to redis queue
    
     
    # successful upload
    return JSONResponse(
        content="Resume uploaded successfully. Please wait while it is being parsed",
        status_code=201
    )
    
    

@app.get("/{resume_id}", summary="get all the information about a posted resume")
async def get_resume(resume_id: str, user_id: str = Depends(get_user_id)):
    return get_resume_info(resume_id, user_id)
    
    

@app.get("/{resume_id}/status", summary="Get the current status of a resume")
async def resume_status(resume_id: str, user_id: str = Depends(get_user_id)):
    return get_resume_status(resume_id, user_id)
