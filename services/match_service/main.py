from fastapi import FastAPI

app = FastAPI()

@app.get("/matches")
async def root():
    return {"message": "This is the Match Service for JobMatchEngine"}