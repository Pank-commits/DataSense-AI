from app.ai.qdrant_service import search
from app.ai.llm_service import ask_gemini


def build_context(results):
    """
    Convert retrieved datasets into LLM context.
    """

    if not results:
        return "No datasets found."

    context = ""

    for index, dataset in enumerate(results, start=1):
        context += f"""
Dataset {index}

Name: {dataset.get("name")}

Category: {dataset.get("category")}

Machine Learning Task: {dataset.get("ml_task")}

Slug: {dataset.get("slug")}

----------------------------------------
"""

    return context


def ask_datasense(question: str):
    """
    Complete RAG Pipeline
    """

    # Retrieve relevant datasets
    datasets = search(question, limit=5)

    # Convert datasets into prompt context
    context = build_context(datasets)

    # Ask Gemini
    answer = ask_gemini(
        question=question,
        context=context,
    )

    return {
        "question": question,
        "answer": answer,
        "datasets": datasets,
    }