
from fastapi import FastAPI

# Creating our API application
app = FastAPI(
    title="TaskFlow API",
    description="A RESTful Task Management API built with Python",
    version="1.0.0"
)


# First endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API!",
        "status": "online"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
