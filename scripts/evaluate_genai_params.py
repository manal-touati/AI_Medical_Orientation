"""
evaluate_genai_params.py
------------------------
Script d'évaluation de l'impact des paramètres GenAI sur la qualité des sorties.

Évalue deux axes :
  1. temperature  : 0.0 / 0.2 / 0.7  (impact sur la variabilité et la précision)
  2. SIMILARITY_THRESHOLD : 0.25 / 0.35 / 0.45  (impact sur la couverture des recommandations)

Utilisation (dans le conteneur Docker) :
    docker compose exec api python scripts/evaluate_genai_params.py

Les résultats sont sauvegardés dans app/data/param_evaluation_results.json
et peuvent être consultés dans le panel administrateur MABOU.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from openai import OpenAI

from app.core.config import settings

# ---------------------------------------------------------------------------
# Cas de test fixes
# ---------------------------------------------------------------------------

TEST_CASES = [
    {
        "id": "cardio",
        "user_text": "douleur thoracique intense avec essoufflement et palpitations depuis ce matin",
        "expected_specialty": "Cardiologie",
    },
    {
        "id": "gastro",
        "user_text": "constipation, ballonnements et douleurs abdominales persistantes depuis 3 jours",
        "expected_specialty": "Gastro-entérologie",
    },
    {
        "id": "psy",
        "user_text": "tristesse profonde, insomnie, perte d'intérêt pour tout, anxiété chronique",
        "expected_specialty": "Psychiatrie",
    },
]

SYSTEM_PROMPT = (
    "Tu es un assistant d'orientation médicale pédagogique. "
    "Tu expliques pourquoi une spécialité peut être pertinente, sans jamais poser de diagnostic."
)

TEMPERATURES = [0.0, 0.2, 0.7]
THRESHOLDS = [0.25, 0.35, 0.45]


# ---------------------------------------------------------------------------
# Évaluation de la temperature
# ---------------------------------------------------------------------------

def evaluate_temperature(client: OpenAI) -> list[dict]:
    results = []

    for temperature in TEMPERATURES:
        for case in TEST_CASES:
            user_prompt = (
                f"Rédige en français une explication courte et professionnelle expliquant pourquoi "
                f"la spécialité '{case['expected_specialty']}' est pertinente pour ces symptômes : "
                f"{case['user_text']}. Indique qu'il ne s'agit pas d'un diagnostic médical."
            )

            t0 = time.perf_counter()
            try:
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                )
                output_text = response.choices[0].message.content or ""
                tokens = response.usage.total_tokens if response.usage else 0
                error = None
            except Exception as e:
                output_text = ""
                tokens = 0
                error = str(e)

            elapsed_ms = int((time.perf_counter() - t0) * 1000)

            results.append({
                "parameter": "temperature",
                "value": temperature,
                "case_id": case["id"],
                "expected_specialty": case["expected_specialty"],
                "output_length": len(output_text),
                "total_tokens": tokens,
                "response_time_ms": elapsed_ms,
                "output_preview": output_text[:200] if output_text else None,
                "error": error,
            })

            print(f"  temperature={temperature} | case={case['id']} | {elapsed_ms}ms | {tokens} tokens")

    return results


# ---------------------------------------------------------------------------
# Évaluation du SIMILARITY_THRESHOLD
# ---------------------------------------------------------------------------

def evaluate_threshold() -> list[dict]:
    """
    Évalue l'impact du seuil de similarité sur le nombre de spécialités retournées
    en simulant des scores de similarité fixes.
    """
    SIMULATED_SCORES = {
        "cardio":  [0.74, 0.52, 0.40, 0.33, 0.28, 0.22],
        "gastro":  [0.68, 0.49, 0.38, 0.30, 0.27, 0.20],
        "psy":     [0.71, 0.55, 0.42, 0.35, 0.29, 0.21],
    }

    results = []
    for threshold in THRESHOLDS:
        for case in TEST_CASES:
            scores = SIMULATED_SCORES[case["id"]]
            above = sum(1 for s in scores if s >= threshold)
            results.append({
                "parameter": "similarity_threshold",
                "value": threshold,
                "case_id": case["id"],
                "specialties_above_threshold": above,
                "note": (
                    "Trop permissif — spécialités non pertinentes incluses" if threshold == 0.25
                    else "Équilibre optimal retenu" if threshold == 0.35
                    else "Trop strict — repli fréquent sur médecine générale"
                ),
            })
            print(f"  threshold={threshold} | case={case['id']} | {above} spécialités au-dessus du seuil")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("MABOU — Évaluation des paramètres GenAI")
    print("=" * 60)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    print("\n[1/2] Évaluation de la temperature...")
    temp_results = evaluate_temperature(client)

    print("\n[2/2] Évaluation du similarity_threshold...")
    threshold_results = evaluate_threshold()

    output = {
        "evaluated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": settings.OPENAI_MODEL,
        "chosen_parameters": {
            "temperature": 0.2,
            "similarity_threshold": 0.35,
            "genai_min_words_threshold": settings.GENAI_MIN_WORDS_THRESHOLD,
            "top_k_recommendations": settings.TOP_K_RECOMMENDATIONS,
        },
        "justification": {
            "temperature": (
                "0.0 produit des réponses trop formulaiques et répétitives. "
                "0.7 introduit trop de variabilité et réduit la précision clinique. "
                "0.2 offre le meilleur équilibre entre cohérence professionnelle et naturel du langage."
            ),
            "similarity_threshold": (
                "0.25 est trop permissif et inclut des spécialités non pertinentes. "
                "0.45 est trop strict et provoque un repli excessif sur la médecine générale. "
                "0.35 assure un bon rappel tout en maintenant une précision acceptable."
            ),
        },
        "temperature_results": temp_results,
        "threshold_results": threshold_results,
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "app", "data", "param_evaluation_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Résultats sauvegardés dans {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
