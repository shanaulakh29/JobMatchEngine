#!/bin/bash

# Run all FastAPI services on different ports
uvicorn api_gateway.main:app --reload --port 8000 &
uvicorn auth_service.main:app --reload --port 8001 &
uvicorn resume_service.main:app --reload --port 8002 &
uvicorn match_service.main:app --reload --port 8003 &
uvicorn job_service.main:app --reload --port 8004 &
wait
