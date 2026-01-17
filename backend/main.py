import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .core.config import settings

# Configure logging
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(
    title="ChatBot Platform",
    description="Production-ready authentication based chatbot",
    version="0.1.0",
)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173", 
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint"""
    return {"status": "healthy", "version": "1.1.1"}