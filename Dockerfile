FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances en premier (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source et les données
COPY src/ src/
COPY data/ data/

# Variables d'environnement par défaut
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
