"""
FastAPI entry point for F1 Strategy Room backend.
"""
from app.config import CORS_ORIGINS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="F1 Strategy Room API",
    description="Turn F1 telemetry into race-winning strategy insights",
    version="0.1.0",
)

# CORS middleware - allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "F1 Strategy Room API is running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {"status": "healthy", "service": "f1-strategy-room-api"}
