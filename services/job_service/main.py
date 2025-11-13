from fastapi import FastAPI

app = FastAPI()

@app.get("/jobs")
async def root():
    return {"message": "This is the Jobs Service for JobMatchEngine"}