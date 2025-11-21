import time
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled = True


def register_middleware(app: FastAPI):
    
    
    @app.middleware('http')
    async def custom_middleware(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        message = f"{request.method} : {request.url.path} - {response.status_code} completed after {processing_time}s"
        
        print(message)
        
        return response
    
    
    
    
""" 
    More use case of middleware
    
    @app.middleware('http')
    async def authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            return JSONResponse(content = {"message":"Not Authenticated",
                       "resolution":"Please provide the right credential to procced"},
                                status_code=status.HTTP_401_UNAUTHORIZED)
            
            
        response = await call_next(request)
        return response
"""