"""Configuration centralisée du pipeline RAG ShopVite.

Toutes les valeurs sont surchargeable via le fichier .env,
ce qui permet de modifier le comportement sans toucher au code.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charge les variables du fichier .env dans l'environnement
load_dotenv()

# --- Chemins ---
# resolve() donne le chemin absolu, .parent.parent remonte de src/ vers la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# --- LLM ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# gpt-4o-mini : bon rapport qualité/coût, bonne compréhension du français, latence faible (~1-2s)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
# text-embedding-3-small : 1536 dimensions, performant pour le retrieval sémantique et peu coûteux
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# --- Chunking ---
# 500 caractères : assez grand pour contenir une réponse complète (ex: une Q/R de FAQ),
# assez petit pour que le retriever reste précis (moins de bruit)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
# Chevauchement de 100 caractères : si une réponse est à cheval sur deux chunks,
# le chevauchement garantit qu'au moins un chunk contient l'information complète
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# --- Retrieval ---
# Top-K = 4 : on récupère les 4 chunks les plus similaires à la question.
# Trop peu → risque de manquer l'info. Trop → bruit dans le contexte du LLM.
TOP_K = int(os.getenv("TOP_K", "4"))

# --- API ---
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
