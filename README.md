# ShopVite FAQ Assistant — Pipeline RAG

Assistant FAQ intelligent pour **ShopVite**, une boutique en ligne de produits électroniques. Propulsé par un pipeline **RAG (Retrieval-Augmented Generation)** qui répond aux questions des clients en se basant exclusivement sur la documentation officielle.

## Architecture du pipeline

<p align="center">
  <img src="images/architecture.png" width="700"/>
</p>

## Stack technique — Justification des choix

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **API** | FastAPI | Framework Python rapide, auto-documentation Swagger, support async natif, validation Pydantic intégrée |
| **LLM** | GPT-4o-mini (OpenAI) | Excellent rapport qualité/coût, bonne compréhension du français, faible latence. Facilement remplaçable via `.env` |
| **Embeddings** | text-embedding-3-small | Modèle OpenAI performant pour le retrieval sémantique, 1536 dimensions, coût très bas |
| **Vector Store** | ChromaDB | Léger, persistant, sans infrastructure externe. Idéal pour un PoC / déploiement Docker |
| **Chunking** | RecursiveCharacterTextSplitter | Découpe intelligente respectant la hiérarchie du texte (paragraphes > lignes > phrases) |
| **Orchestration** | LangChain | Simplifie le chaînage ingestion → vectorisation → retrieval. Écosystème riche et bien documenté |
| **Déploiement** | Docker | Reproductible, portable, déploiement en une commande |

## Démarrage rapide

### Prérequis
- Python 3.11+ ou Docker
- Une clé API OpenAI

### Option A — Docker (recommandé)

```bash
cp .env.example .env          # Configurer OPENAI_API_KEY
docker build -t shopvite-faq .
docker run -p 8000:8000 --env-file .env shopvite-faq
```

### Option B — Python local

```bash
cp .env.example .env          # Configurer OPENAI_API_KEY
pip install -r requirements.txt
python -m src.main
```

L'API est accessible sur `http://localhost:8000`. Documentation Swagger sur `http://localhost:8000/docs`.

## Utilisation de l'API

### POST /ask — Poser une question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelle est la politique de retour ?"}'
```

**Réponse attendue :**
```json
{
  "answer": "Le délai de retour chez ShopVite est de 30 jours calendaires à compter de la date de réception. Le produit doit être dans son emballage d'origine, en état neuf, avec tous les accessoires. Les retours sont gratuits pour les produits défectueux ; sinon, des frais de 9,95 $ s'appliquent. [Source : politique_retour.txt]",
  "sources": ["politique_retour.txt"],
  "confidence": "high"
}
```

### GET /health — Statut de l'API

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "vectorstore_loaded": true,
  "num_documents": 42
}
```

### Exemples de requêtes

| Question | Type | Confiance attendue |
|----------|------|--------------------|
| "Quelle est la politique de retour ?" | In-scope | high |
| "Combien coûte le TechPhone Pro 15 ?" | In-scope | high |
| "Quel est le délai de livraison express ?" | In-scope | high |
| "Comment contacter le service client ?" | In-scope | high |
| "Quel est le prix du Bitcoin ?" | Hors-scope | low |
| "Quelle est la météo à Montréal ?" | Hors-scope | low |

## Structure du projet

```
shopvite-faq-assistant/
├── README.md                  # Ce fichier
├── reflection.md              # Réflexion sur les choix techniques
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Image Docker
├── docker-compose.yml         # Orchestration Docker
├── .env.example               # Variables d'environnement (template)
├── .gitignore
├── data/                      # Corpus de documents ShopVite
│   ├── data_sources.md        # Origine des documents
│   ├── faq_generale.txt       # FAQ générale (10 Q/R)
│   ├── politique_retour.txt   # Politique de retour (7 sections)
│   ├── guide_produits.json    # Catalogue produits (5 produits)
│   ├── livraison_expedition.md# Politique de livraison
│   └── conditions_generales.txt# CGV (9 articles)
├── src/                       # Code source
│   ├── __init__.py
│   ├── config.py              # Configuration centralisée
│   ├── ingestion.py           # Chargement et chunking
│   ├── vectorstore.py         # Embeddings + ChromaDB
│   ├── retriever.py           # Retrieval contextuel
│   ├── generator.py           # Génération LLM
│   ├── prompts.py             # System prompt
│   └── main.py                # API FastAPI
├── eval/                      # Évaluation quantitative
│   └── evaluate.py            # Script d'évaluation (10+ questions)
└── demo.ipynb                 # Notebook de démonstration
```
