import os

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def ask_gemini(question: str, context: str) -> str:
    """
    Ask Gemini using retrieved dataset context.
    """

    prompt = f"""
You are DataSense AI.

You are an AI Dataset Discovery Assistant.

Use ONLY the datasets provided below.

If the answer is not available in the context,
say:

"I couldn't find a suitable dataset."

=========================
DATASETS
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
ANSWER
=========================

Provide:

1. Best recommendation
2. Why it matches
3. ML task
4. Category
5. Short explanation
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text
