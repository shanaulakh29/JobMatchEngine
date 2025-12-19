from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv
from typing import Optional
from api_gateway.authorize_middleware import authorize_middleware
from starlette.responses import Response as StarletteResponse

load_dotenv()

app = FastAPI(title="API Gateway", version="1.0.0")
app.middleware("http")(authorize_middleware)
# microservices urls dictionary
SERVICES: dict = {
    "auth": os.environ['AUTH_SERVICE'],
    "resume": os.environ['RESUME_SERVICE'],
    "match": os.environ['MATCH_SERVICE'],
    "job": os.environ['JOB_SERVICE']
}

# health check endpoint (root)
@app.get("/")
async def root():
    """Returns a JSON with gateway status and all microservices health"""
    services_health: dict = {}
    # loop through SERVICES and check each one's health endpoints
    for service, service_url in SERVICES.items():
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{service_url}/health", headers=None, params=None)
                services_health[service] = "healthy"
            except:
                services_health[service] = "unhealthy"
    
    return {"Service": "API Gateway", "Status": "Running OK", "Services": services_health}

# # TODO: Configure timeout settings (OPTIONAL) -> Automatic timeout for response that take long time

# # Create an httpx.Timeout object with:
# # - Overall timeout (e.g., 30 seconds)
# # - Connect timeout (e.g., 10 seconds)
# TIMEOUT = None  # Replace with httpx.Timeout(...)


async def forward_request(
    service_url: str,
    method: str,
    path: str,
    headers: dict,
    body = None,
    params: Optional[dict] = None,
    json_body=None,
    form_body=None
):
    """
    This is the CORE function - forwards requests to microservices
    """
    async with httpx.AsyncClient() as client:
        try:
            # service ur;
            url = f"{service_url}{path}"

            # await thre response from service
            response = await client.request(method, url, content=body, headers=headers, params=params)    
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {service_url}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=503, detail="Gateway timeout")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        return response


# Route handler for a service request
@app.api_route("/{service}/{path:path}", methods=["GET", "POST"])
async def req_route(service: str, path: str, request: Request):
    """Route requests to proper service"""
    # check if service exists
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    # get the url for service
    service_url = SERVICES[service]

    # gather req headers
    headers = dict(request.headers)

    # get any body if POST req
    body = await request.body() if request.method in ["POST"] else None
  
    if hasattr(request.state, "user_id"):
        headers["user_id"] = str(request.state.user_id)

    # forwrd reqeust to microservice
    response = await forward_request(service_url, request.method, f"/{path}", headers, body, dict(request._query_params))

    #  return the response
    return StarletteResponse(content=response.content, status_code=response.status_code, headers=dict(response.headers), media_type=response.headers.get("content-type"))