#!/bin/bash
 
# install dependencies if any needed
pip3 install -r requirements.txt

# Run all FastAPI services on different ports
# /api
uvicorn api_gateway.main:app --reload --port 8000 &
# /auth
uvicorn auth_service.main:app --reload --port 8001 &
# /resume
uvicorn resume_service.main:app --reload --port 8002 &
# /matches
uvicorn match_service.main:app --reload --port 8003 &
# /jobs
uvicorn job_service.main:app --reload --port 8004 &

wait
