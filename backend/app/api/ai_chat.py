from pydantic import BaseModel

from fastapi import APIRouter

from app.ai.rag_service import ask_datasense


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

    return ask_datasense(
        request.question
    )