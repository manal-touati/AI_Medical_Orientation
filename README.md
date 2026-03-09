
# IA GEN — Orientation Médicale Assistée par IA Générative

## Objectif du projet

Ce projet a été réalisé dans le cadre d’un **projet de Master en IA Générative**.
L'objectif est de développer un **système d'orientation médicale assistée par intelligence artificielle** capable d'analyser des symptômes décrits par un utilisateur et de suggérer les spécialités médicales les plus pertinentes.

⚠️ Ce système **ne réalise aucun diagnostic médical**.  
Il fournit uniquement une **orientation indicative** vers des spécialités médicales.

---

# Principe général du système

Le système combine :

- **IA sémantique (SBERT)** pour comprendre les symptômes
- **Règles métier médicales**
- **IA générative (OpenAI)** pour produire des explications compréhensibles

Pipeline global :

Utilisateur → API FastAPI → Analyse sémantique SBERT → Scoring hybride → Détection red flags → Génération explication GenAI → Résultat API

---

# Architecture du projet

Architecture simplifiée :

Backend API :
- FastAPI

Moteur IA :
- Sentence Transformers (SBERT)

IA générative :
- OpenAI API

Base de données :
- PostgreSQL

Conteneurisation :
- Docker
- Docker Compose

Tests :
- Pytest

---

# Pipeline d'analyse des symptômes

## 1. Préprocessing

Le texte utilisateur est structuré avec :

- description du symptôme
- intensité
- durée
- localisation
- contexte additionnel

Un texte consolidé est construit pour l'analyse sémantique.

---

## 2. Analyse sémantique avec SBERT

Le modèle SBERT transforme :

- le texte utilisateur
- les descriptions des spécialités

en **vecteurs sémantiques**.

La similarité cosinus permet d'évaluer la proximité entre les symptômes et les spécialités médicales.

---

## 3. Scoring hybride

Le score final combine :

- Similarité sémantique
- Bonus de localisation
- Bonus d’intensité
- Bonus red flags

Formule utilisée :

final_score = semantic_similarity × 0.8 + metadata_bonus × 0.2

---

## 4. Détection de red flags

Le système détecte des **signes critiques** comme :

- severe chest pain
- fainting
- seizure
- sudden paralysis
- difficulty breathing
- suicidal thoughts

Si détecté, un **message d'avertissement renforcé** est affiché.

---

## 5. Génération d'explication avec IA générative

OpenAI est utilisé pour produire une **explication pédagogique** expliquant pourquoi une spécialité peut être pertinente.

L’IA générative est utilisée uniquement pour :

- reformulation
- explication

Elle **ne participe pas au scoring**.

---

# Gestion des erreurs et robustesse

Pour éviter toute défaillance :

- appels OpenAI encapsulés dans try/except
- fallback automatique si l’API échoue
- cache PostgreSQL pour éviter les appels répétés

---

# Stack technique

| Composant | Technologie |
|-----------|-------------|
| API | FastAPI |
| IA sémantique | Sentence Transformers |
| IA générative | OpenAI |
| Base de données | PostgreSQL |
| Conteneurisation | Docker |
| Tests | Pytest |

---

# Structure du projet

```
ia-gen-medical-orientation/

app/
 ├── api/
 ├── services/
 ├── models/
 ├── schemas/
 ├── repositories/
 ├── utils/
 └── main.py

tests/
scripts/

Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

# Lancement du projet

## 1. Cloner le projet

```
git clone <repo>
cd ia-gen-medical-orientation
```

## 2. Lancer les conteneurs

```
docker compose up --build
```

---

# Accès à l'API

Swagger UI :

http://localhost:8000/docs

---

# Endpoints principaux

## Health

GET /api/v1/health

Retourne l'état de l'API.

---

## Questionnaire

GET /api/v1/questionnaire/template

Retourne la structure du questionnaire.

---

## Recommandation

POST /api/v1/recommendations

Exemple :

```
{
  "symptom_description": "I have chest pain and shortness of breath",
  "intensity": "high",
  "duration": "2 days",
  "location": "chest",
  "additional_context": "The pain increases when walking"
}
```

Retour :

- top spécialités
- score
- explication
- red flags éventuels

---

# Tests

Exécution des tests :

```
docker compose exec api pytest
```

---

# Limites du système

Ce système :

- ne remplace pas un médecin
- ne produit pas de diagnostic
- sert uniquement d'outil d'orientation

---

# Améliorations possibles

- enrichir la base médicale
- utiliser un modèle biomédical
- interface utilisateur
- monitoring

---

Projet réalisé dans le cadre du **Master IA Générative**.
