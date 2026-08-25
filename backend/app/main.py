from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ai_chat import router as ai_chat_router
from app.db.database import Base, engine
from app.api.semantic_search import router as semantic_search_router
from app.routers.datasets import router as dataset_router
from app.routers.auth import router as auth_router
from app.api.dashboard import router as dashboard_router

# Import models so SQLAlchemy creates all tables
from app.models.dataset import Dataset
from app.models.user import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataSense AI API",
    description="AI Powered Dataset Discovery Platform",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(dataset_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(semantic_search_router)
app.include_router(ai_chat_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to DataSense AI API",
        "version": "1.0.0",
        "status": "Running"
    }