
# Orientation Médicale par IA

Projet de Master en IA Générative. Le système analyse les symptômes décrits par un utilisateur et suggère les spécialités médicales les plus pertinentes.

Ce système ne réalise aucun diagnostic médical. Il fournit uniquement une orientation indicative.

---

## Fonctionnement

1. Les données saisies (symptômes, intensité, durée, localisation, contexte) sont consolidées en un texte structuré
2. SBERT calcule la similarité sémantique entre ce texte et les descriptions des spécialités médicales
3. Un score hybride combine la similarité sémantique avec des bonus (localisation, intensité, red flags)
4. Les mots-clés critiques sont détectés et déclenchent un avertissement
5. OpenAI génère une explication lisible pour chaque spécialité recommandée

Formule de scoring : `score_final = similarité_sémantique × 0.8 + bonus_metadata × 0.2`

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| API | FastAPI |
| IA sémantique | Sentence Transformers (SBERT) |
| IA générative | OpenAI |
| Base de données | PostgreSQL |
| Frontend | Streamlit |
| Conteneurisation | Docker / Docker Compose |
| Tests | Pytest |

---

## Structure du projet

```
app/
  api/
  services/
  models/
  schemas/
  repositories/
  utils/
  main.py
front/
tests/
scripts/
Dockerfile
docker-compose.yml
requirements.txt
```

---

## Lancement

```bash
git clone <repo>
cd ia-gen-medical-orientation
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend (Streamlit) | http://localhost:8501 |
| API (Swagger UI) | http://localhost:8000/docs |

---

## Endpoints API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/health | Etat de l'API |
| GET | /api/v1/questionnaire/template | Structure du questionnaire |
| POST | /api/v1/recommendations | Obtenir des recommandations |
| GET | /api/v1/admin/responses | 20 dernières soumissions |
| GET | /api/v1/admin/recommendations | 50 dernières recommandations |
| GET | /api/v1/admin/genai-cache | 50 dernières entrées du cache GenAI |

### Exemple de requête

```json
{
  "symptom_description": "I have chest pain and difficulty breathing",
  "intensity": "high",
  "duration": "2 days",
  "location": "chest",
  "additional_context": "The pain increases when walking"
}
```

---

## Tests

```bash
docker compose exec api pytest
```

---

## Limites

- Ne remplace pas un professionnel de santé
- Ne produit pas de diagnostic
- Sert uniquement d'outil d'orientation

# Améliorations possibles

- enrichir la base médicale
- utiliser un modèle biomédical
- monitoring

---

Projet réalisé dans le cadre du **Master Data Engineering & IA**.