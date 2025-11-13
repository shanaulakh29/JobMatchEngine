from fastapi import FastAPI

app = FastAPI()

@app.get("/resume")
async def root():
    return {"message": "This is the Resume Service for JobMatchEngine"}

