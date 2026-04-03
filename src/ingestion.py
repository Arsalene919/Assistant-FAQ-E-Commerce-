"""Module d'ingestion : chargement et découpage des documents ShopVite."""

import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_txt(path: Path) -> str:  # Returns raw text content of the file
    """Charge un fichier texte brut."""
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> str:
    """Charge un fichier JSON et le convertit en texte lisible pour le RAG."""
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = [f"Catalogue : {data.get('catalogue', '')}\n"]
    for prod in data.get("produits", []):
        lines.append(f"--- Produit : {prod['nom']} (ID: {prod['id']}) ---")
        lines.append(f"Catégorie : {prod['categorie']}")
        lines.append(f"Prix : {prod['prix']} {prod['devise']}")
        lines.append(f"Description : {prod['description']}")
        lines.append(f"Garantie : {prod['garantie']}")
        lines.append(f"Disponibilité : {prod['disponibilite']}")
        lines.append(f"Note clients : {prod['note_clients']}/5 ({prod['nombre_avis']} avis)")
        lines.append(f"Points forts : {', '.join(prod['points_forts'])}")
        lines.append(f"Compatibilité : {prod['compatibilite']}\n")
    return "\n".join(lines)


def load_markdown(path: Path) -> str:
    """Charge un fichier Markdown."""
    return path.read_text(encoding="utf-8")


LOADERS = {
    ".txt": load_txt,
    ".json": load_json,
    ".md": load_markdown,
}


def load_all_documents() -> list[Document]:
    """Charge tous les fichiers du dossier data/ et les convertit en Documents LangChain."""
    documents = []
    for file_path in sorted(DATA_DIR.iterdir()):
        if file_path.suffix in LOADERS and file_path.name != "data_sources.md":
            content = LOADERS[file_path.suffix](file_path)
            documents.append(
                Document(page_content=content, metadata={"source": file_path.name})
            )
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Découpe les documents en chunks avec chevauchement."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def ingest() -> list[Document]:
    """Pipeline complet d'ingestion : chargement + chunking."""
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    return chunks
