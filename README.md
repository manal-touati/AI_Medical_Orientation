# MABOU — Orientation médicale assistée par IA

## Présentation

**MABOU** est une application d’orientation médicale assistée par intelligence artificielle, conçue pour analyser des symptômes décrits en langage naturel et suggérer la ou les spécialités médicales les plus pertinentes.

L’objectif du projet n’est **pas** de poser un diagnostic médical, mais de fournir une **orientation indicative**, explicable et sécurisée, à partir d’un pipeline hybride combinant :

- **SBERT multilingue** pour la compréhension sémantique,
- **règles métier** pour améliorer le scoring,
- **détection de red flags** pour les cas critiques,
- **OpenAI API** pour la reformulation et la génération d’explications,
- **FastAPI** pour le backend,
- **Streamlit** pour l’interface utilisateur et le panel d’administration,
- **PostgreSQL** pour la persistance et le monitoring.

---

## Objectif du projet

Le but de MABOU est d’aider un utilisateur à savoir **vers quel spécialiste médical s’orienter** à partir d’une description libre de ses symptômes.

### Exemple
Un utilisateur peut saisir :

> “J’ai une douleur thoracique avec essoufflement et palpitations depuis ce matin.”

Le système peut alors suggérer :

1. **Cardiologie**
2. **Pneumologie**

avec :
- un **score de pertinence**,
- une **explication textuelle**,
- les **symptômes reconnus**,
- une **alerte urgente** si des signaux critiques sont détectés.

---

## Fonctionnalités principales

### 1. Analyse sémantique des symptômes
Le système transforme les symptômes saisis en représentation vectorielle grâce à **Sentence-BERT** afin de comparer la requête utilisateur avec un référentiel de spécialités médicales.

### 2. Référentiel médical structuré
Le projet repose sur :
- un référentiel de **15 spécialités médicales**,
- un référentiel de **40+ symptômes de référence**,
- des **synonymes**,
- des **red flags**,
- des **zones anatomiques**,
- des **spécialités associées**.

### 3. Scoring hybride
Le classement final repose sur :
- un **score sémantique principal**,
- un **bonus de localisation**,
- un **bonus d’intensité**,
- un **bonus lié aux symptômes détectés**,
- un **bonus de red flags**.

### 4. Sécurité métier
Si certains signaux critiques sont détectés, l’application affiche une alerte renforcée :

> **Urgence détectée : Contactez immédiatement le SAMU (15)**

### 5. Explications générées par IA
OpenAI est utilisé pour :
- reformuler les saisies trop courtes,
- générer une explication pédagogique de la spécialité recommandée.

### 6. Cache IA
Les réponses générées sont mises en cache pour :
- réduire les coûts,
- améliorer les temps de réponse,
- éviter les appels redondants.

### 7. Monitoring avancé
Le panel administrateur permet de suivre :
- l’historique des requêtes,
- la latence,
- les hits/misses de cache,
- les jetons consommés,
- les alertes SAMU déclenchées.

---

## Architecture du projet

```text
AI_Medical_Orientation/
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.frontend
├── alembic.ini
├── pytest.ini
├── README.md
├── requirements.txt
├── requirements-frontend.txt
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── data/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── front/
│   └── app.py
├── scripts/
└── tests/
```

---

## Architecture technique

### Backend — FastAPI
Le backend expose les endpoints REST et orchestre toute la logique métier.

### Frontend — Streamlit
Le frontend offre :
- une interface utilisateur professionnelle,
- un formulaire dynamique,
- un affichage des recommandations,
- un affichage des symptômes reconnus,
- un panel d’administration sécurisé.

### Base de données — PostgreSQL
La base stocke :
- les réponses utilisateurs,
- les recommandations,
- le cache IA,
- les métriques et l’audit technique.

### IA sémantique — SBERT
Le modèle utilisé est :

```env
SBERT_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

Il permet une comparaison sémantique robuste en français.

### IA générative — OpenAI
Le modèle OpenAI est utilisé pour compléter le système sans remplacer la logique métier.

---

## Pipeline de traitement

Le workflow complet est le suivant :

1. **Saisie utilisateur**
2. **Prétraitement du texte**
3. **Enrichissement éventuel via OpenAI**
4. **Détection des symptômes structurés**
5. **Détection des red flags**
6. **Encodage sémantique avec SBERT**
7. **Calcul des similarités**
8. **Application du scoring hybride**
9. **Génération d’explication**
10. **Sauvegarde en base**
11. **Affichage dans l’interface**
12. **Mise à jour du monitoring**

---

## Logique de scoring

Le score final repose sur une combinaison entre similarité sémantique et bonus métier.

### Formule

```text
score_final = (semantic_similarity * 0.80)
            + location_bonus
            + intensity_bonus
            + red_flag_bonus
            + symptom_reference_bonus
```

### Détails
- **semantic_similarity** : proximité sémantique entre les symptômes et une spécialité,
- **location_bonus** : bonus si la zone anatomique est cohérente,
- **intensity_bonus** : bonus selon le niveau d’intensité,
- **red_flag_bonus** : bonus si un red flag de la spécialité est détecté,
- **symptom_reference_bonus** : bonus si des symptômes structurés liés à la spécialité sont reconnus.

Cette approche permet de produire un classement plus crédible qu’une simple similarité textuelle brute.

---

## Référentiel médical

### Spécialités intégrées
Le projet inclut 15 spécialités :

- Cardiologie
- Pneumologie
- Neurologie
- Gastro-entérologie
- Dermatologie
- ORL
- Ophtalmologie
- Rhumatologie
- Endocrinologie
- Néphrologie
- Urologie
- Gynécologie
- Psychiatrie
- Infectiologie
- Orthopédie

### Symptômes de référence
Le système détecte plus de 40 symptômes canoniques avec :
- synonymes,
- gravité,
- catégorie,
- zone du corps,
- spécialités associées,
- statut red flag.

---

## Red Flags et sécurité

Exemples de signaux critiques pris en charge :

- douleur thoracique intense,
- essoufflement au repos,
- convulsion,
- paralysie brutale,
- confusion aiguë,
- vomissements de sang,
- sang dans les selles,
- idées suicidaires,
- saignement vaginal abondant,
- impossibilité d’uriner.

Quand un signal urgent ou critique est détecté :
- l’alerte est affichée dans l’interface,
- l’événement est historisé,
- un compteur de sécurité est incrémenté dans le panel admin.

---

## Endpoints principaux

### Santé de l’API

```http
GET /api/v1/health
```

### Template du questionnaire

```http
GET /api/v1/questionnaire/template
```

### Recommandation principale

```http
POST /api/v1/recommendations/
```

### Administration

```http
GET /api/v1/admin/responses
GET /api/v1/admin/recommendations
GET /api/v1/admin/genai-cache
GET /api/v1/admin/history
GET /api/v1/admin/metrics
```

---

## Exemple de payload

```json
{
  "symptom_description": "J’ai une douleur thoracique intense avec essoufflement et palpitations",
  "intensity": "high",
  "duration": "depuis 30 minutes",
  "location": "poitrine",
  "additional_context": "aggravation rapide"
}
```

---

## Exemple de réponse

```json
{
  "enriched_input": null,
  "recommendations": [
    {
      "specialty_name": "Cardiology",
      "similarity_score": 0.7483,
      "explanation": "..."
    }
  ],
  "red_flags": [
    {
      "keyword": "chest pain",
      "severity": "high",
      "message": "Chest pain may require urgent medical attention."
    }
  ],
  "warning": "This result is an indicative orientation only and not a medical diagnosis. Some warning signs were detected and may require urgent medical attention.",
  "detected_symptoms": [
    {
      "canonical_name": "chest pain",
      "matched_terms": ["chest pain"],
      "category": "cardiovascular",
      "severity_hint": "high",
      "body_zone": "chest",
      "specialties": ["Cardiology", "Pulmonology"],
      "is_red_flag": true,
      "red_flag_message": "Chest pain may require urgent medical attention."
    }
  ]
}
```

---

## Installation et lancement

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd AI_Medical_Orientation
```

### 2. Configurer les variables d’environnement

Créer un fichier `.env` à la racine du projet :

```env
APP_NAME=MABOU
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1

HOST=0.0.0.0
PORT=8000

POSTGRES_DB=medical_orientation
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:postgres@db:5432/medical_orientation

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=gpt-4.1-mini

SBERT_MODEL=paraphrase-multilingual-MiniLM-L12-v2

GENAI_ENABLE=true
GENAI_MIN_WORDS_THRESHOLD=5

CACHE_ENABLED=true
TOP_K_RECOMMENDATIONS=3
SIMILARITY_THRESHOLD=0.35
ADMIN_PASSWORD=admin123
SAMU_PHONE_NUMBER=15
```

### 3. Lancer avec Docker

```bash
docker compose up --build
```

### 4. Accéder aux services

- **API FastAPI** : `http://localhost:8000/docs`
- **Interface Streamlit** : `http://localhost:8501`

---

## Exécution des tests

Lancer les tests backend :

```bash
docker compose exec api pytest
```

Les tests couvrent notamment :
- la santé de l’API,
- le questionnaire,
- les recommandations,
- le scoring,
- le cache IA.

---

## Cas de test recommandés

### Cas 1 — Cardiologie
**Entrée :**
> douleur thoracique, essoufflement, palpitations, aggravé à l’effort

**Attendu :**
- Top 1 : Cardiologie
- Red flags : oui
- Suggestion SAMU : possible selon la gravité

### Cas 2 — Gastro-entérologie
**Entrée :**
> constipation, ballonnements, douleur abdominale

**Attendu :**
- Top 1 : Gastro-entérologie
- Red flags : non

### Cas 3 — Psychiatrie
**Entrée :**
> tristesse persistante, anxiété, insomnie, perte d’intérêt

**Attendu :**
- Top 1 : Psychiatrie
- Red flags : non

### Cas 4 — Urgence neurologique
**Entrée :**
> faiblesse brutale du bras gauche, difficulté à parler, vertiges

**Attendu :**
- Top 1 : Neurologie
- Red flags : oui
- Suggestion SAMU : oui

### Cas 5 — Urgence psychiatrique
**Entrée :**
> j’ai envie de mourir, idées suicidaires, je ne me sens plus en sécurité

**Attendu :**
- Top 1 : Psychiatrie
- Red flags : critiques
- Suggestion SAMU : oui

---

## Panel administrateur

Le panel admin MABOU permet d’accéder à :

### KPIs
- nombre total de requêtes,
- temps de réponse moyen,
- jetons consommés,
- nombre d’entrées de cache,
- taux de cache hit,
- nombre d’alertes SAMU,
- nombre de red flags détectés.

### Historique
- requêtes récentes,
- spécialité top 1,
- latence,
- usage OpenAI,
- événements critiques.

### Visualisations
- latence des appels,
- consommation des jetons,
- hits / misses du cache,
- déclenchements d’alertes.

---

## Points forts du projet

- architecture modulaire propre,
- pipeline IA hybride réaliste,
- explications générées automatiquement,
- prise en compte de la sécurité métier,
- monitoring technique avancé,
- interface professionnelle démontrable,
- forte valeur académique pour un projet de master.

---

## Limites du projet

- l’application ne fournit **aucun diagnostic médical**,
- le système dépend de la qualité de la saisie utilisateur,
- le référentiel médical reste limité à un périmètre défini,
- la qualité des explications OpenAI dépend du modèle et du contexte,
- l’outil reste un assistant d’orientation, pas un dispositif médical.

---

## Perspectives d’amélioration

- enrichissement du référentiel médical,
- ajout d’un vrai système d’authentification admin,
- historisation plus fine des tokens et coûts,
- personnalisation par profil patient,
- export PDF des analyses,
- fine-tuning sur corpus médical spécialisé,
- déploiement cloud industrialisé.

---

## Avertissement

> **MABOU est un système d’orientation médicale indicative.**
>
> Il ne remplace ni un médecin, ni une consultation, ni une prise en charge d’urgence.
>
> En cas de symptômes graves ou de doute, contactez immédiatement les services d’urgence ou un professionnel de santé.

---

## Auteur / cadre académique

Projet réalisé dans le cadre d’un travail de **Master en IA Générative / Data / NLP**, avec pour objectif de démontrer :
- la maîtrise d’un pipeline sémantique moderne,
- l’intégration contrôlée d’IA générative,
- la conception d’une application complète,
- la prise en compte de la sécurité, de l’explicabilité et du monitoring.

---

## Licence

À définir selon votre cadre académique ou votre dépôt GitHub.
