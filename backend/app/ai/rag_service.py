from app.ai.qdrant_service import search
from app.ai.llm_service import ask_gemini


# ==========================
# BUILD RAG CONTEXT
# ==========================

def build_context(results):
    """
    Convert retrieved datasets into structured LLM context.
    """

    if not results:
        return "No datasets were retrieved."

    context_parts = []

    for index, dataset in enumerate(results, start=1):

        context_parts.append(
            f"""
Dataset {index}

ID: {dataset.get("id")}
Name: {dataset.get("name")}
Slug: {dataset.get("slug")}
Category: {dataset.get("category")}
Machine Learning Task: {dataset.get("ml_task")}
Data Type: {dataset.get("data_type")}
Difficulty: {dataset.get("difficulty")}
Tags: {dataset.get("tags")}
Description: {dataset.get("description")}

----------------------------------------
"""
        )

    return "\n".join(context_parts)


# ==========================
# BUILD RAG PROMPT
# ==========================

def build_prompt(question, context):
    """
    Create a grounded prompt for Gemini.

    Gemini must only recommend datasets
    that appear in the retrieved context.
    """

    return f"""
You are DataSense AI, an AI assistant for a dataset discovery platform.

User question:
{question}

Retrieved datasets:
{context}

IMPORTANT RULES:

1. Only recommend datasets that appear in the retrieved datasets above.
2. Do not invent datasets.
3. Do not recommend a dataset that is not present in the retrieved context.
4. Choose the most relevant dataset based on the user's question.
5. If several datasets are relevant, mention the best one first.
6. Use the exact dataset name from the retrieved context.
7. Keep the answer concise and useful.

Format your answer exactly like this:

1. Best recommendation: <exact dataset name>
2. Why it matches: <short explanation>
3. ML task: <machine learning task>
4. Category: <category>
5. Short explanation: <short explanation>

If none of the retrieved datasets are clearly relevant, say:

"No strongly matching dataset was found in the current dataset collection."
"""


# ==========================
# ASK DATASENSE
# ==========================

def ask_datasense(question: str):
    """
    Complete RAG pipeline:

    User Question
        ↓
    Qdrant Retrieval
        ↓
    Context Construction
        ↓
    Gemini
        ↓
    Grounded Answer
    """

    # --------------------------------
    # Validate question
    # --------------------------------

    if not question or not question.strip():
        return {
            "question": question,
            "answer": "Please enter a question.",
            "datasets": [],
        }

    question = question.strip()

    # --------------------------------
    # Retrieve relevant datasets
    # --------------------------------

    from app.agents.dataset_agent import (
        understand_request,
        build_search_query,
        rerank_datasets,
    )

    intent = understand_request(question)
    datasets = search(
        build_search_query(question, intent),
        limit=20,
        intent=intent,
    )
    datasets = rerank_datasets(datasets, question, intent)[:5]

    # --------------------------------
    # Build context
    # --------------------------------

    context = build_context(datasets)

    # --------------------------------
    # Build grounded prompt
    # --------------------------------

    prompt = build_prompt(
        question=question,
        context=context,
    )

    # --------------------------------
    # Ask Gemini
    # --------------------------------

    answer = ask_gemini(
        question=question,
        context=prompt,
    )

    # --------------------------------
    # Return API response
    # --------------------------------

    return {
        "question": question,
        "answer": answer,
        "datasets": datasets,
    }
