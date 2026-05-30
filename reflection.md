# Réflexion technique: ShopVite FAQ Assistant

## Justification du prompt engineering

Le system prompt a été conçu avec trois techniques complémentaires :

1. **Few-shot examples** (3 exemples) : en montrant une réponse in-scope avec citation de source, une réponse hors-scope avec le refus poli, et un exemple de réponse avec données chiffrées, le modèle apprend le format et le ton attendus sans ambiguïté. Cette technique est plus fiable qu'une simple instruction car elle ancre le comportement via la démonstration.

2. **Garde-fous explicites** : les règles numérotées ("réponds UNIQUEMENT à partir du contexte", "cite tes sources") agissent comme des contraintes dures. La phrase de refus hors-scope est définie mot pour mot, ce qui élimine la variabilité dans le traitement des questions non couvertes.

3. **Chain-of-thought implicite** : la section "Processus de raisonnement" guide le modèle à suivre un cheminement logique (identifier le sujet --> localiser les passages --> formuler --> citer) avant de répondre. Cela réduit les hallucinations en forçant une vérification mentale du contexte avant toute génération.

Le choix d'un ton professionnel et concis en français reflète le contexte francophone du client ShopVite.

## Ce que je ferais différemment avec plus de temps

- **Hybrid search** : combiner la recherche sémantique (embeddings) avec une recherche lexicale (BM25) pour améliorer le recall, surtout pour les requêtes contenant des noms de produits ou des codes (ex: "SV-SP-001").
- **Reranking** : ajouter un modèle de reranking (Cohere Rerank ou cross-encoder) après le retrieval initial pour affiner la pertinence des chunks sélectionnés.
- **Évaluation continue** : intégrer RAGAS dans un pipeline CI/CD pour détecter les régressions de qualité à chaque modification du prompt ou du corpus.
- **Cache sémantique** : mettre en cache les réponses aux questions fréquentes pour réduire la latence et les coûts API.
- **Interface utilisateur** : ajouter un frontend Streamlit ou Gradio pour une démonstration plus visuelle.

## Limitation identifiée

Le système actuel ne gère pas bien les questions **multi-sujets** (ex: "Quelle est la politique de retour ET le délai de livraison ?"). Le retriever retourne les k chunks les plus similaires globalement, mais peut manquer de diversité thématique. Une solution serait d'implémenter un **query decomposition** qui sépare les sous-questions avant le retrieval, puis fusionne les réponses. De plus, le chunking à taille fixe peut couper des sections logiques au milieu — un chunking sémantique (par section/paragraphe) serait plus adapté pour des documents structurés comme les CGV.
