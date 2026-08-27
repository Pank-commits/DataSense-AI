from pydantic import BaseModel

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.dataset_agent import run_dataset_agent


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):
    """
    AI Dataset Assistant
    """

    try:
        return run_dataset_agent(question=request.question)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Recommendation service is temporarily unavailable.",
        ) from error
