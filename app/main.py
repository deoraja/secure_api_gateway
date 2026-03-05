from fastapi import FastAPI
from app.routers import auth_routes, task_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(task_routes.router)

@app.get("/")
def home():
    return {"message": "Secure API Gateway Starting"}