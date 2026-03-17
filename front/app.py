# score de coverage 
import os
from typing import Any

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

GENERIC_EXPLANATION_MARKERS = [
    "may be relevant based on the semantic similarity",
    "rule-based matching",
    "this is not a medical diagnosis",
]


def is_generic_explanation(text: str) -> bool:
    if not text:
        return True
    lowered = text.lower()
    return any(marker in lowered for marker in GENERIC_EXPLANATION_MARKERS)


def get_api_status() -> tuple[bool, str]:
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "API disponible"
        return False, f"API indisponible ({response.status_code})"
    except Exception:
        return False, "API non joignable"


def severity_label(severity: str) -> str:
    mapping = {
        "low": "Faible",
        "medium": "Moyen",
        "high": "Élevé",
        "critical": "Critique",
    }
    return mapping.get(severity.lower(), severity.title())


def intensity_to_api(value: str) -> str | None:
    mapping = {
        "Faible": "low",
        "Modérée": "medium",
        "Élevée": "high",
        "Très élevée": "high",
    }
    return mapping.get(value)


def format_score(score: float) -> str:
    return f"{int(score * 100)}%"


def render_styles() -> None:
    st.markdown(
        """
        <style>
            .main > div {
                padding-top: 1.5rem;
            }

            .block-container {
                max-width: 1100px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: white;
                padding: 1.8rem 1.8rem;
                border-radius: 18px;
                margin-bottom: 1.2rem;
                border: 1px solid rgba(255,255,255,0.08);
            }

            .hero-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .hero-subtitle {
                font-size: 1rem;
                opacity: 0.88;
                line-height: 1.6;
            }

            .section-title {
                font-size: 1.15rem;
                font-weight: 700;
                margin-top: 0.6rem;
                margin-bottom: 0.7rem;
            }

            .result-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 1rem 1rem 0.8rem 1rem;
                margin-bottom: 0.9rem;
                box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
            }

            .result-rank {
                display: inline-block;
                min-width: 32px;
                text-align: center;
                padding: 0.2rem 0.55rem;
                border-radius: 999px;
                background: #0f172a;
                color: white;
                font-weight: 700;
                font-size: 0.85rem;
                margin-right: 0.5rem;
            }

            .result-title {
                font-size: 1.08rem;
                font-weight: 700;
                color: #0f172a;
            }

            .result-score {
                font-size: 0.95rem;
                color: #475569;
                font-weight: 600;
                margin-top: 0.25rem;
            }

            .muted-text {
                color: #64748b;
                font-size: 0.95rem;
                line-height: 1.6;
            }

            .symptom-chip {
                display: inline-block;
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                border-radius: 999px;
                padding: 0.35rem 0.7rem;
                margin: 0.15rem 0.3rem 0.15rem 0;
                font-size: 0.85rem;
                color: #0f172a;
            }

            .sidebar-box {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                padding: 0.9rem;
                margin-bottom: 0.8rem;
            }

            .warning-box {
                background: #fff7ed;
                border: 1px solid #fdba74;
                border-radius: 14px;
                padding: 0.9rem 1rem;
                color: #9a3412;
                margin-top: 0.8rem;
                margin-bottom: 1rem;
            }

            .critical-box {
                background: #fef2f2;
                border: 1px solid #fca5a5;
                border-radius: 14px;
                padding: 0.9rem 1rem;
                color: #991b1b;
                margin-top: 0.8rem;
                margin-bottom: 1rem;
            }

            .info-box {
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                border-radius: 14px;
                padding: 0.9rem 1rem;
                color: #0f172a;
                margin-top: 0.8rem;
                margin-bottom: 1rem;
            }

            div[data-testid="stForm"] {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 1.2rem 1.2rem 0.4rem 1.2rem;
                box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stMetric"] {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                padding: 0.6rem 0.8rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.markdown("## Configuration")

    api_ok, api_message = get_api_status()
    if api_ok:
        st.sidebar.success(api_message)
    else:
        st.sidebar.error(api_message)

    st.sidebar.markdown(
        """
        <div class="sidebar-box">
            <strong>Objet</strong><br>
            Cette application fournit une orientation indicative vers les spécialités médicales
            les plus pertinentes à partir des symptômes saisis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div class="sidebar-box">
            <strong>Important</strong><br>
            Cette interface ne fournit pas de diagnostic médical et ne remplace pas un professionnel de santé.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("## Exemples de saisie")
    examples = [
        "Douleur thoracique, essoufflement, palpitations",
        "Maux de tête sévères, faiblesse d’un bras, vertiges",
        "Douleur pelvienne, saignements anormaux",
        "Tristesse persistante, anxiété, insomnie",
    ]
    for item in examples:
        st.sidebar.caption(f"• {item}")


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Orientation médicale assistée par IA</div>
            <div class="hero-subtitle">
                Décrivez vos symptômes pour obtenir une orientation vers les spécialités médicales
                les plus pertinentes, avec analyse sémantique, détection des signaux d’alerte
                et explications générées automatiquement.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning_box(red_flags: list[dict], warning_text: str) -> None:
    if red_flags:
        severities = {flag["severity"].lower() for flag in red_flags}
        is_critical = "critical" in severities

        box_class = "critical-box" if is_critical else "warning-box"
        title = "Alerte prioritaire" if is_critical else "Signaux d’alerte détectés"

        items = "".join(
            [
                f"<li><strong>{flag['keyword']}</strong> — {flag['message']} "
                f"(niveau : {severity_label(flag['severity'])})</li>"
                for flag in red_flags
            ]
        )

        st.markdown(
            f"""
            <div class="{box_class}">
                <strong>{title}</strong>
                <ul style="margin-top: 0.6rem; margin-bottom: 0.2rem;">
                    {items}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if warning_text:
        st.markdown(
            f"""
            <div class="info-box">
                <strong>Information</strong><br>
                {warning_text}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_detected_symptoms(detected_symptoms: list[dict]) -> None:
    st.markdown('<div class="section-title">Symptômes reconnus</div>', unsafe_allow_html=True)

    if not detected_symptoms:
        st.caption("Aucun symptôme structuré n’a été détecté dans le référentiel.")
        return

    for symptom in detected_symptoms:
        with st.container(border=True):
            cols = st.columns([2.2, 1.2, 1.2, 1.4])

            with cols[0]:
                st.markdown(f"**{symptom['canonical_name']}**")
                matched = ", ".join(symptom.get("matched_terms", []))
                st.caption(f"Termes reconnus : {matched if matched else '—'}")

            with cols[1]:
                st.caption("Catégorie")
                st.write(symptom.get("category", "—"))

            with cols[2]:
                st.caption("Gravité")
                st.write(severity_label(symptom.get("severity_hint", "medium")))

            with cols[3]:
                st.caption("Zone")
                st.write(symptom.get("body_zone") or "—")

            specialties = symptom.get("specialties", [])
            if specialties:
                st.caption("Spécialités associées")
                chips = "".join(
                    [f'<span class="symptom-chip">{sp}</span>' for sp in specialties]
                )
                st.markdown(chips, unsafe_allow_html=True)


def render_recommendations(recommendations: list[dict]) -> None:
    st.markdown('<div class="section-title">Spécialités recommandées</div>', unsafe_allow_html=True)

    if not recommendations:
        st.warning("Aucune recommandation n’a pu être générée.")
        return

    score_data = []
    for index, rec in enumerate(recommendations, start=1):
        score = float(rec.get("similarity_score", 0))
        score_data.append(
            {
                "rank": index,
                "specialty": rec.get("specialty_name", "Unknown"),
                "score": score,
            }
        )

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <span class="result-rank">{index}</span>
            <span class="result-title">{rec.get("specialty_name", "Spécialité inconnue")}</span>
            <div class="result-score">Niveau de correspondance : {format_score(score)}</div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(score)

        explanation = rec.get("explanation", "")
        if explanation and not is_generic_explanation(explanation):
            st.markdown(f'<div class="muted-text">{explanation}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="muted-text">
                    Cette spécialité apparaît parmi les correspondances les plus pertinentes
                    au regard des symptômes décrits et du scoring calculé.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    if score_data:
        st.markdown('<div class="section-title">Comparaison des scores</div>', unsafe_allow_html=True)
        chart_rows = [
            {
                "Spécialité": row["specialty"],
                "Score": int(row["score"] * 100),
            }
            for row in score_data
        ]
        st.bar_chart(chart_rows, x="Spécialité", y="Score", horizontal=True)


def call_recommendation_api(payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(f"{API_URL}/recommendations/", json=payload, timeout=90)
    response.raise_for_status()
    return response.json()


def main() -> None:
    st.set_page_config(
        page_title="Orientation Médicale IA",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_styles()
    render_sidebar()
    render_header()

    col_left, col_right = st.columns([1.2, 1.0], gap="large")

    with col_left:
        st.markdown('<div class="section-title">Formulaire d’analyse</div>', unsafe_allow_html=True)

        with st.form("medical_orientation_form", clear_on_submit=False):
            symptom_description = st.text_area(
                "Description des symptômes *",
                placeholder="Exemple : douleur thoracique, essoufflement et palpitations depuis ce matin...",
                height=160,
            )

            c1, c2 = st.columns(2)
            with c1:
                intensity_label = st.selectbox(
                    "Intensité",
                    ["", "Faible", "Modérée", "Élevée", "Très élevée"],
                )
                duration = st.text_input(
                    "Durée",
                    placeholder="Exemple : 2 jours, 1 semaine, depuis ce matin",
                )

            with c2:
                location = st.text_input(
                    "Localisation",
                    placeholder="Exemple : poitrine, tête, abdomen, bassin",
                )
                additional_context = st.text_input(
                    "Contexte additionnel",
                    placeholder="Exemple : enceinte, diabétique, après effort",
                )

            submitted = st.form_submit_button(
                "Lancer l’analyse",
                use_container_width=True,
            )

        if submitted:
            if len(symptom_description.strip()) < 3:
                st.error("Veuillez décrire les symptômes avec au moins 3 caractères.")
                return

            payload = {
                "symptom_description": symptom_description.strip(),
                "intensity": intensity_to_api(intensity_label),
                "duration": duration.strip() or None,
                "location": location.strip() or None,
                "additional_context": additional_context.strip() or None,
            }

            with st.spinner("Analyse en cours..."):
                try:
                    data = call_recommendation_api(payload)
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Impossible de joindre l’API. Vérifiez que le backend FastAPI est bien démarré."
                    )
                    return
                except requests.exceptions.Timeout:
                    st.error("Le délai de réponse de l’API a été dépassé.")
                    return
                except requests.exceptions.HTTPError as exc:
                    response_text = exc.response.text if exc.response is not None else str(exc)
                    st.error(f"Erreur HTTP côté API : {response_text}")
                    return
                except Exception as exc:
                    st.error(f"Erreur inattendue : {exc}")
                    return

            st.session_state["last_result"] = data

    with col_right:
        st.markdown('<div class="section-title">Vue synthétique</div>', unsafe_allow_html=True)

        last_result = st.session_state.get("last_result")

        if not last_result:
            st.markdown(
                """
                <div class="info-box">
                    <strong>Aucune analyse pour le moment</strong><br>
                    Remplissez le formulaire puis lancez l’analyse pour afficher les résultats,
                    les symptômes détectés, les recommandations et les éventuels signaux d’alerte.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            recommendations = last_result.get("recommendations", [])
            red_flags = last_result.get("red_flags", [])
            detected_symptoms = last_result.get("detected_symptoms", [])
            warning_text = last_result.get("warning", "")
            enriched_input = last_result.get("enriched_input")

            m1, m2, m3 = st.columns(3)
            m1.metric("Spécialités proposées", len(recommendations))
            m2.metric("Symptômes détectés", len(detected_symptoms))
            m3.metric("Signaux d’alerte", len(red_flags))

            if enriched_input:
                st.markdown(
                    f"""
                    <div class="info-box">
                        <strong>Reformulation automatique</strong><br>
                        {enriched_input}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            render_warning_box(red_flags, warning_text)

    last_result = st.session_state.get("last_result")
    if last_result:
        st.divider()
        bottom_left, bottom_right = st.columns([1.15, 0.85], gap="large")

        with bottom_left:
            render_recommendations(last_result.get("recommendations", []))

        with bottom_right:
            render_detected_symptoms(last_result.get("detected_symptoms", []))


if __name__ == "__main__":
    main()