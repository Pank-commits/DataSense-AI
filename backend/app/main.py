from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import API_CORS_ORIGINS

from app.api.ai_chat import router as ai_chat_router
from app.api.semantic_search import router as semantic_search_router
from app.api.dashboard import router as dashboard_router

from app.routers.datasets import router as dataset_router
from app.routers.auth import router as auth_router

from app.db.database import Base, engine

# Import models so SQLAlchemy creates all tables
from app.models.dataset import Dataset
from app.models.user import User
from app.models.source_sync import SourceSyncState

# Scheduler
from app.scheduler import start_scheduler, stop_scheduler
from app.ai.qdrant_service import verify_connection


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="DataSense AI API",
    description="AI Powered Dataset Discovery Platform",
    version="1.0.0"
)


# ==========================================
# STARTUP / SHUTDOWN
# ==========================================

@app.on_event("startup")
def startup_event():
    print()
    print("================================")
    print("DATASENSE AI STARTUP")
    print("================================")

    qdrant_status = verify_connection()
    print(f"Qdrant connected: {qdrant_status['collection']}")
    start_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    print()
    print("================================")
    print("DATASENSE AI SHUTDOWN")
    print("================================")

    stop_scheduler()


# ==========================================
# CORS
# ==========================================

origins = API_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ROUTES
# ==========================================

app.include_router(
    dataset_router
)

app.include_router(
    auth_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    semantic_search_router
)

app.include_router(
    ai_chat_router
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Welcome to DataSense AI API",
        "version": "1.0.0",
        "status": "Running"
    }


@app.get("/health/qdrant")
def qdrant_health():
    """Connectivity and collection health check for local Qdrant."""
    return verify_connection()
