from fastapi import FastAPI

app = FastAPI()


# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "This is the Job Service for JobMatchEngine", 
            "status": "Running OK"
            }

@app.get('/jobs', summary="Get All Jobs")
async def getAllJobs():
    return {
        "jobs": [
            {
                "id": 1,
                "title": "Backend Developer",
                "company": "TechNova",
                "location": "Vancouver, BC",
                "type": "Full-time",
                "salary": "90,000 - 110,000 CAD",
                "posted_at": "2025-12-01",
                "description": "Build and maintain REST APIs using FastAPI and PostgreSQL."
            },
            {
                "id": 2,
                "title": "Frontend Developer",
                "company": "PixelWorks",
                "location": "Remote",
                "type": "Contract",
                "salary": "60 - 80 CAD/hour",
                "posted_at": "2025-12-05",
                "description": "Develop responsive UI using React and Tailwind CSS."
            },
            {
                "id": 3,
                "title": "DevOps Engineer",
                "company": "CloudBridge",
                "location": "Toronto, ON",
                "type": "Full-time",
                "salary": "100,000 - 130,000 CAD",
                "posted_at": "2025-12-10",
                "description": "Manage Dockerized services and CI/CD pipelines."
            }
        ]
    }