from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the Jobs Service for JobMatchEngine"}