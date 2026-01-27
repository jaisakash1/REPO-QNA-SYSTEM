"""
FastAPI Backend for Repo QnA System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.ingest import router as ingest_router
from api.routes.query import router as query_router

app = FastAPI(
    title="Repo QnA API",
    description="Query your GitHub repositories using natural language",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest_router, prefix="/api", tags=["Ingestion"])
app.include_router(query_router, prefix="/api", tags=["Query"])


@app.get("/")
async def root():
    return {
        "message": "Repo QnA API",
        "docs": "/docs",
        "endpoints": {
            "ingest": "POST /api/ingest",
            "query": "POST /api/query",
            "repos": "GET /api/repos"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
