"""Module de vectorisation : embeddings + ChromaDB."""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config import OPENAI_API_KEY, EMBEDDING_MODEL, CHROMA_DIR


def get_embeddings() -> OpenAIEmbeddings:
    """Retourne le modèle d'embedding configuré."""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
    )


def create_vectorstore(chunks: list[Document]) -> Chroma:
    """Crée (ou écrase) le vector store ChromaDB à partir des chunks."""
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="shopvite_faq",
    )
    return vectorstore


def load_vectorstore() -> Chroma:
    """Charge le vector store existant depuis le disque."""
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="shopvite_faq",
    )
