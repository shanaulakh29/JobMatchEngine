from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from resume_service.db import init_db,  db_execute, db_query
from resume_service.bucket import upload_s3, create_presigned_url
import logging

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
async def upload_file(file: UploadFile = File(...)):
    
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
    if not await upload_s3(file, file_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="unable to upload file at this time")
    
    # generate a S3 url
    s3_url = await create_presigned_url(file_name)
    logging.info("S3_URL: ", s3_url)
    
    
    # TODO: upload to the resumes table with userID connected
    
    
    # TODO: push to redis queue
     
    # successful upload
    return JSONResponse(
        content="Resume uploaded successfully. Please wait while it is being parsed",
        status_code=201
    )
    
    
# TODO: get endpoints for resume id
@app.get("/{resume_id}", summary="get all the information about a posted resume")

# TODO: get endpoints for a resume status
@app.get("/{resume_id}/status", summary="Get the current status of a resume")
async def resume_status():
    