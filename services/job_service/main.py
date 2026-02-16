from fastapi import FastAPI, HTTPException, Query,Path
from dotenv import load_dotenv
import httpx
import os
load_dotenv()

app = FastAPI()


# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "This is the Job Service for JobMatchEngine", 
            "status": "Running OK"
            }

@app.get('/jobs', summary="Get All Jobs")
async def getAllJobs(
    query: str = Query("jobs", description="Search query for jobs"),
    country: str = Query("us", description="Country code e.g: US"),
    page: int = Query(1, ge=1, le=50, description="Page number between 1 and 50"),
    num_pages: int = Query(1, description="Number of pages"),
    date_posted: str = Query("all", description="Date filter, e.g., 'all', 'last_7_days'")):

    
    # return "hello jobs"
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": os.environ["JSEARCH_API_KEY"]
    }
    # in params we can add the functionality of num_pages, country, page
    params = {
        "query": query,
        "page": page,
        "num_pages": num_pages,
        "country": country,
        "date_posted": date_posted
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/{job_id}", summary="Get Job Details by ID")
async def getJobDetail(job_id: str = Path(..., description="ID of the job to fetch")):
    url = "https://jsearch.p.rapidapi.com/job-details"

    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": os.environ["JSEARCH_API_KEY"],
    }

    params = {
        "job_id": job_id
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/applied-jobs")
# async def appliedJobs():

#     return ""