from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API Gateway", version="1.0.0")

# microservices urls dictionary
SERVICES: dict = {
    "/auth": os.environ['AUTH_SERVICE'],
    "/resume": os.environ['RESUME_SERVICE'],
    "/match": os.environ['MATCH_SERVICE'],
    "/job": os.environ['JOB_SERVICE']
}

@app.get("/")
async def root():
    """API GATEWAY INFORMATION"""
    return {"service": "API Gateway", "status": "Running OK", "available_routes": list(SERVICES.keys())}

# TODO: Configure timeout settings
# Create an httpx.Timeout object with:
# - Overall timeout (e.g., 30 seconds)
# - Connect timeout (e.g., 10 seconds)
TIMEOUT = None  # Replace with httpx.Timeout(...)


async def forward_request(
    service_url: str,
    path: str,
    method: str,
    headers: dict,
    body: Optional[bytes] = None,
    params: dict = None
):
    """
    This is the CORE function - forwards requests to microservices
    
    TODO: Implement the forwarding logic:
    1. Create an async HTTP client using httpx.AsyncClient with timeout
    2. Clean up headers (remove 'host' and 'content-length' to avoid conflicts)
       - Hint: Use dict comprehension to filter out unwanted headers
    3. Make the request to the target service:
       - Use client.request() method
       - Pass: method, url (service_url + path), headers, content (body), params
    4. Return a Response object with:
       - content from the microservice response
       - status_code from the microservice response
       - headers from the microservice response
    5. Handle errors:
       - httpx.ConnectError → raise HTTPException with 503 (Service Unavailable)
       - httpx.TimeoutException → raise HTTPException with 504 (Gateway Timeout)
       - General Exception → raise HTTPException with 500 (Internal Server Error)
    """
    # Your implementation here
    pass


# TODO: Create route handler for Auth Service
# Use @app.api_route decorator with:
# - Path: "/auth/{path:path}" (captures everything after /auth/)
# - Methods: ["GET", "POST", "PUT", "DELETE", "PATCH"]
# 
# Inside the function:
# 1. Extract request body if method is POST, PUT, or PATCH
#    - Hint: await request.body() if request.method in [...]
# 2. Call forward_request() with:
#    - Service URL from SERVICES dict
#    - The path parameter (add "/" prefix)
#    - request.method
#    - dict(request.headers)
#    - body (if applicable)
#    - dict(request.query_params)
# 3. Return the result


# TODO: Create route handler for Job Service
# Same pattern as auth service but for "/jobs/{path:path}"


# TODO: Create route handler for Resume Service  
# Same pattern for "/resumes/{path:path}"


# TODO: Create route handler for Match Service
# Same pattern for "/match/{path:path}"


# TODO: Create a health check endpoint
# @app.get("/health")
# This should:
# 1. Create a dict to store health status of each service
# 2. Loop through SERVICES and check each one's /health endpoint
# 3. For each service:
#    - Try to make a GET request to service_url/health
#    - If successful (200), mark as "healthy"
#    - If error, mark as "unhealthy" or "unreachable"
# 4. Return a JSON with gateway status and all services' health


# TODO: Create a root endpoint
# @app.get("/")
# Return basic info about the gateway:
# - Service name
# - Version
# - List of available routes/services





