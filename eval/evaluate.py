"""Évaluation quantitative du pipeline RAG ShopVite.

Évalue la faithfulness (fidélité aux sources) et la relevancy (pertinence)
sur un jeu de 12 questions avec réponses attendues.
"""

import json
import sys
import requests

BASE_URL = "http://localhost:8000"

# Jeu de test : 12 questions avec réponses attendues et type
TEST_QUESTIONS = [
    {
        "question": "Quelle est la politique de retour ?",
        "expected_keywords": ["30 jours", "emballage d'origine", "retour"],
        "expected_source": "politique_retour.txt",
        "type": "in_scope",
    },
    {
        "question": "Combien coûte le TechPhone Pro 15 ?",
        "expected_keywords": ["1299.99", "CAD"],
        "expected_source": "guide_produits.json",
        "type": "in_scope",
    },
    {
        "question": "Quel est le délai de livraison standard au Canada ?",
        "expected_keywords": ["5", "7", "jours ouvrables"],
        "expected_source": "livraison_expedition.md",
        "type": "in_scope",
    },
    {
        "question": "Comment contacter le service client ?",
        "expected_keywords": ["support@shopvite.ca", "1-800-555-SHOP"],
        "expected_source": "faq_generale.txt",
        "type": "in_scope",
    },
    {
        "question": "La garantie couvre-t-elle les dommages accidentels ?",
        "expected_keywords": ["ne couvre pas", "mauvaise utilisation", "chutes"],
        "expected_source": "conditions_generales.txt",
        "type": "in_scope",
    },
    {
        "question": "Quels moyens de paiement acceptez-vous ?",
        "expected_keywords": ["Visa", "Mastercard", "PayPal"],
        "expected_source": "faq_generale.txt",
        "type": "in_scope",
    },
    {
        "question": "Combien coûte la livraison express au Canada ?",
        "expected_keywords": ["14,95", "2 à 3 jours"],
        "expected_source": "livraison_expedition.md",
        "type": "in_scope",
    },
    {
        "question": "La TabVite 12 Pro est-elle disponible ?",
        "expected_keywords": ["rupture", "stock", "avril"],
        "expected_source": "guide_produits.json",
        "type": "in_scope",
    },
    {
        "question": "Quel est le programme de fidélité ?",
        "expected_keywords": ["point", "500", "25 $"],
        "expected_source": "faq_generale.txt",
        "type": "in_scope",
    },
    {
        "question": "Que faire si je reçois un produit défectueux ?",
        "expected_keywords": ["48 heures", "retour prioritaire", "remplacement"],
        "expected_source": "politique_retour.txt",
        "type": "in_scope",
    },
    {
        "question": "Quel est le prix du Bitcoin aujourd'hui ?",
        "expected_keywords": ["ne dispose pas"],
        "expected_source": None,
        "type": "out_of_scope",
    },
    {
        "question": "Quelle est la météo à Montréal ?",
        "expected_keywords": ["ne dispose pas"],
        "expected_source": None,
        "type": "out_of_scope",
    },
]


def evaluate_answer(result: dict, test_case: dict) -> dict:
    """Évalue une réponse selon les critères de faithfulness et relevancy."""
    answer = result.get("answer", "").lower()
    sources = result.get("sources", [])
    confidence = result.get("confidence", "")

    # Faithfulness : les mots-clés attendus sont-ils présents ?
    keywords_found = sum(
        1 for kw in test_case["expected_keywords"] if kw.lower() in answer
    )
    faithfulness = keywords_found / len(test_case["expected_keywords"])

    # Source accuracy : la bonne source est-elle citée ?
    if test_case["expected_source"] is None:
        source_match = confidence == "low"
    else:
        source_match = test_case["expected_source"] in sources

    # Relevancy : la réponse est-elle pertinente par rapport au type ?
    if test_case["type"] == "out_of_scope":
        relevancy = 1.0 if "ne dispose pas" in answer else 0.0
    else:
        relevancy = faithfulness  # Basé sur la couverture des mots-clés

    return {
        "question": test_case["question"],
        "type": test_case["type"],
        "faithfulness": round(faithfulness, 2),
        "relevancy": round(relevancy, 2),
        "source_match": source_match,
        "confidence": confidence,
    }


def main():
    print("=" * 80)
    print("ÉVALUATION DU PIPELINE RAG — ShopVite FAQ Assistant")
    print("=" * 80)

    # Vérifier que l'API est accessible
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=10)
        health.raise_for_status()
        print(f"\nAPI Status: {health.json()['status']}")
    except requests.exceptions.ConnectionError:
        print("\nERREUR: L'API n'est pas accessible. Lancez le serveur d'abord.")
        print("  python -m src.main")
        sys.exit(1)

    results = []
    for i, test_case in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[{i}/{len(TEST_QUESTIONS)}] {test_case['question']}")
        try:
            resp = requests.post(
                f"{BASE_URL}/ask",
                json={"question": test_case["question"]},
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            evaluation = evaluate_answer(result, test_case)
            results.append(evaluation)
            print(f"  Faithfulness: {evaluation['faithfulness']}")
            print(f"  Relevancy:    {evaluation['relevancy']}")
            print(f"  Source OK:    {evaluation['source_match']}")
            print(f"  Confiance:    {evaluation['confidence']}")
        except Exception as e:
            print(f"  ERREUR: {e}")
            results.append({
                "question": test_case["question"],
                "type": test_case["type"],
                "faithfulness": 0.0,
                "relevancy": 0.0,
                "source_match": False,
                "confidence": "error",
            })

    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)

    avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
    avg_relevancy = sum(r["relevancy"] for r in results) / len(results)
    source_accuracy = sum(1 for r in results if r["source_match"]) / len(results)

    print(f"\n  Faithfulness moyenne : {avg_faithfulness:.2%}")
    print(f"  Relevancy moyenne   : {avg_relevancy:.2%}")
    print(f"  Source accuracy     : {source_accuracy:.2%}")
    print(f"  Questions évaluées  : {len(results)}")

    print("\n  Détail par question :")
    print(f"  {'#':<3} {'Type':<12} {'Faith.':<10} {'Relev.':<10} {'Source':<8}")
    print(f"  {'-'*3} {'-'*12} {'-'*10} {'-'*10} {'-'*8}")
    for i, r in enumerate(results, 1):
        src = "OK" if r["source_match"] else "MISS"
        print(f"  {i:<3} {r['type']:<12} {r['faithfulness']:<10.2f} {r['relevancy']:<10.2f} {src:<8}")


if __name__ == "__main__":
    main()
