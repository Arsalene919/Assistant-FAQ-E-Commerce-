"""Module de génération : appel au LLM avec le contexte RAG."""

from openai import OpenAI

from src.config import OPENAI_API_KEY, LLM_MODEL
from src.prompts import SYSTEM_PROMPT


def generate_answer(question: str, context: str) -> str:
    """Génère une réponse à partir de la question et du contexte RAG."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = SYSTEM_PROMPT.replace("{context}", context)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=600,
    )
    return response.choices[0].message.content


def estimate_confidence(answer: str, sources: list[str]) -> str:
    """Estime le niveau de confiance de la réponse.

    - "high" : la réponse cite des sources et ne contient pas le message hors-scope
    - "low" : la réponse est le message hors-scope
    - "medium" : autre cas
    """
    out_of_scope_marker = "je ne dispose pas de cette information"
    if out_of_scope_marker.lower() in answer.lower():
        return "low"
    if sources and len(sources) >= 1:
        return "high"
    return "medium"
