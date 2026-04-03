# Sources de données — ShopVite FAQ Assistant

## Corpus utilisé

Tous les documents ont été créés manuellement pour simuler un environnement e-commerce réaliste pour le client fictif **ShopVite**. Le contenu est inspiré des FAQ et politiques publiques de boutiques en ligne canadiennes (Best Buy Canada, Amazon.ca, Fnac).

| Fichier | Format | Contenu | Origine |
|---------|--------|---------|---------|
| `faq_generale.txt` | TXT | 10 questions-réponses couvrant les sujets les plus fréquents (compte, paiement, suivi, fidélité) | Créé manuellement |
| `politique_retour.txt` | TXT | Politique complète de retour et remboursement (7 sections) | Créé manuellement |
| `guide_produits.json` | JSON | Catalogue de 5 produits phares avec spécifications détaillées | Créé manuellement |
| `livraison_expedition.md` | Markdown | Politique de livraison (zones, tarifs, transporteurs, suivi) | Créé manuellement |
| `conditions_generales.txt` | TXT | CGV complètes (9 articles : prix, garantie, données personnelles, litiges) | Créé manuellement |

## Justification du corpus personnalisé

Plutôt que d'utiliser un dataset public générique, j'ai choisi de créer un corpus sur mesure pour ShopVite afin de :
1. **Contrôler la qualité** : chaque document est pertinent et cohérent avec le contexte e-commerce canadien
2. **Diversifier les formats** : TXT, JSON et Markdown pour tester la robustesse de l'ingestion
3. **Couvrir les cas d'usage réels** : FAQ, retours, livraison, produits, CGV — les 5 piliers du support client
4. **Faciliter l'évaluation** : en connaissant exactement le contenu, on peut évaluer précisément la fidélité des réponses
