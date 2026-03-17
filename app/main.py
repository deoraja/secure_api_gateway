from fastapi import FastAPI,Request
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.routers import auth_routes, task_routes
from app.core.rate_limiter import limiter
from fastapi.responses import JSONResponse

app = FastAPI()

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc:RateLimitExceeded):
    return JSONResponse(status_code=429,content={"detail": "Too many requests. Try again later."})

app.include_router(auth_routes.router)
app.include_router(task_routes.router)

@app.get("/")
def home():
    return {"message": "Secure API Gateway Starting"}