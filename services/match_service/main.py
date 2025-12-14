from fastapi import FastAPI

app = FastAPI()

# status check
@app.get('/health', summary="Status check")
async def root():
    return {"description": "This is the Match Service for JobMatchEngine", 
            "status": "Running OK"
            }