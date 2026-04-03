"""API FastAPI — Assistant FAQ ShopVite avec RAG."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import OPENAI_API_KEY, API_HOST, API_PORT
from src.ingestion import ingest
from src.vectorstore import create_vectorstore, load_vectorstore
from src.retriever import retrieve, format_context
from src.generator import generate_answer, estimate_confidence

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable globale pour le vector store
vectorstore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise le vector store au démarrage de l'application."""
    global vectorstore
    logger.info("Ingestion des documents et création du vector store...")
    try:
        chunks = ingest()
        logger.info(f"{len(chunks)} chunks créés à partir des documents.")
        vectorstore = create_vectorstore(chunks)
        logger.info("Vector store initialisé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation : {e}")
        raise
    yield
    logger.info("Arrêt de l'application.")


app = FastAPI(
    title="ShopVite FAQ Assistant",
    description="Assistant FAQ intelligent pour ShopVite, propulsé par RAG (Retrieval-Augmented Generation).",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Modèles Pydantic ---

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="La question du client")


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: str


class HealthResponse(BaseModel):
    status: str
    vectorstore_loaded: bool
    num_documents: int


# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Vérifie le statut de l'API et du vector store."""
    if vectorstore is None:
        raise HTTPException(status_code=503, detail="Le vector store n'est pas initialisé.")
    collection = vectorstore._collection
    count = collection.count()
    return HealthResponse(
        status="ok",
        vectorstore_loaded=True,
        num_documents=count,
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Endpoint principal : reçoit une question et retourne une réponse RAG."""
    if vectorstore is None:
        raise HTTPException(status_code=503, detail="Le vector store n'est pas encore prêt.")

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="La clé API OpenAI n'est pas configurée.")

    try:
        # Retrieval
        docs = retrieve(vectorstore, request.question)
        context, sources = format_context(docs)

        # Génération
        answer = generate_answer(request.question, context)
        confidence = estimate_confidence(answer, sources)

        return AnswerResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
        )
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la question : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=API_HOST, port=API_PORT, reload=True)
