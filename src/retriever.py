"""Module de retrieval : recherche des chunks les plus pertinents."""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config import TOP_K


def retrieve(vectorstore: Chroma, query: str) -> list[Document]:
    """Retrouve les k chunks les plus similaires à la requête utilisateur."""
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )
    return retriever.invoke(query)


def format_context(documents: list[Document]) -> tuple[str, list[str]]:
    """Formate les documents récupérés en contexte textuel + liste de sources."""
    context_parts = []
    sources = set()
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "inconnu")
        sources.add(source)
        context_parts.append(f"[Document {i} — {source}]\n{doc.page_content}")
    return "\n\n".join(context_parts), sorted(sources)
