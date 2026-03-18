import os
from typing import Any

import altair as alt
import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
ADMIN_PASSWORD = os.getenv("MABOU_ADMIN_PASSWORD", "admin123")

GENERIC_EXPLANATION_MARKERS = [
    "may be relevant based on the semantic similarity",
    "rule-based matching",
    "this is not a medical diagnosis",
    "similarité sémantique",
    "orientation indicative",
]


def is_generic_explanation(text: str) -> bool:
    if not text:
        return True
    lowered = text.lower()
    return any(marker in lowered for marker in GENERIC_EXPLANATION_MARKERS)


def api_get(path: str) -> Any:
    response = requests.get(f"{API_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict[str, Any]) -> Any:
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=90)
    response.raise_for_status()
    return response.json()


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
    return mapping.get((severity or "").lower(), severity.title() if severity else "—")


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
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"], .stApp {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
            }

            .block-container {
                max-width: 1280px;
                padding-top: 1.2rem;
                padding-bottom: 2.8rem;
            }

            .mabou-logo {
                display: inline-flex;
                align-items: center;
                gap: 0.85rem;
                font-weight: 800;
                font-size: 1.7rem;
                letter-spacing: 0.08rem;
                color: #0f172a;
            }

            .mabou-badge {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 800;
                box-shadow: 0 12px 24px rgba(37, 99, 235, 0.24);
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1d4ed8 100%);
                color: white;
                padding: 2rem 2rem;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: 0 20px 50px rgba(15, 23, 42, 0.18);
                margin-bottom: 1.2rem;
            }

            .hero-title {
                font-size: 2.2rem;
                font-weight: 800;
                margin-bottom: 0.45rem;
                line-height: 1.15;
            }

            .hero-subtitle {
                font-size: 1rem;
                line-height: 1.7;
                color: rgba(255,255,255,0.88);
            }

            .glass-card {
                background: rgba(255,255,255,0.86);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(226,232,240,0.85);
                border-radius: 22px;
                padding: 1.25rem 1.25rem;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            }

            .section-title {
                font-size: 1.12rem;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 0.6rem;
                margin-top: 0.2rem;
            }

            .micro-title {
                font-size: 0.83rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08rem;
                color: #64748b;
                margin-bottom: 0.35rem;
            }

            .result-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 1rem 1rem 0.85rem 1rem;
                margin-bottom: 0.9rem;
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
            }

            .result-rank {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 34px;
                height: 34px;
                border-radius: 999px;
                background: #0f172a;
                color: white;
                font-size: 0.88rem;
                font-weight: 800;
                margin-right: 0.55rem;
            }

            .result-title {
                font-size: 1.05rem;
                font-weight: 700;
                color: #0f172a;
            }

            .result-score {
                color: #475569;
                font-size: 0.94rem;
                font-weight: 600;
                margin-top: 0.25rem;
            }

            .muted-text {
                color: #475569;
                font-size: 0.95rem;
                line-height: 1.65;
            }

            .chip {
                display: inline-block;
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                color: #0f172a;
                border-radius: 999px;
                padding: 0.34rem 0.72rem;
                margin: 0.12rem 0.28rem 0.12rem 0;
                font-size: 0.83rem;
            }

            .admin-link {
                text-align: right;
                font-size: 0.88rem;
                color: #334155;
                margin-bottom: 0.6rem;
            }

            .blinking-alert {
                background: linear-gradient(90deg, #7f1d1d 0%, #b91c1c 45%, #ef4444 100%);
                color: white;
                border-radius: 18px;
                padding: 1rem 1.2rem;
                border: 1px solid rgba(255,255,255,0.18);
                box-shadow: 0 16px 30px rgba(185, 28, 28, 0.28);
                animation: pulseDanger 1.25s infinite;
                margin-bottom: 1rem;
            }

            @keyframes pulseDanger {
                0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0.45); }
                50% { transform: scale(1.01); box-shadow: 0 0 0 10px rgba(239,68,68,0.08); }
                100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239,68,68,0.00); }
            }

            .warning-box {
                background: #fff7ed;
                color: #9a3412;
                border-radius: 16px;
                padding: 1rem 1.05rem;
                border: 1px solid #fdba74;
                margin-bottom: 1rem;
            }

            .info-box {
                background: #f8fafc;
                color: #0f172a;
                border-radius: 16px;
                padding: 1rem 1.05rem;
                border: 1px solid #cbd5e1;
                margin-bottom: 1rem;
            }

            div[data-testid="stForm"] {
                background: rgba(255,255,255,0.88);
                border: 1px solid #e2e8f0;
                border-radius: 22px;
                padding: 1.2rem 1.2rem 0.4rem 1.2rem;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
            }

            div[data-testid="metric-container"] {
                background: rgba(255,255,255,0.88);
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 0.7rem 0.9rem;
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
            }

            .small-note {
                color: #64748b;
                font-size: 0.88rem;
                line-height: 1.55;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    col_logo, col_admin = st.columns([0.78, 0.22], gap="small")

    with col_logo:
        st.markdown(
            """
            <div class="mabou-logo">
                <span class="mabou-badge">M</span>
                <span>MABOU</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_admin:
        st.markdown('<div class="admin-link">Accès supervision</div>', unsafe_allow_html=True)
        with st.popover("Connexion admin"):
            password = st.text_input("Mot de passe", type="password", key="admin_password_input")
            if st.button("Se connecter", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state["admin_authenticated"] = True
                    st.success("Connexion admin réussie.")
                else:
                    st.error("Mot de passe invalide.")

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Orientation médicale intelligente et supervision avancée</div>
            <div class="hero-subtitle">
                MABOU analyse les symptômes saisis, identifie les signaux d’alerte, propose les spécialités
                les plus pertinentes et fournit une supervision avancée des performances, du cache IA
                et de l’activité de sécurité.
            </div>
        </div>
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
        <div class="glass-card">
            <div class="micro-title">Objet</div>
            <div class="small-note">
                Application d’orientation médicale indicative basée sur un moteur sémantique,
                des règles métier et des signaux d’alerte.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div class="glass-card">
            <div class="micro-title">Avertissement</div>
            <div class="small-note">
                Cette interface n’établit pas de diagnostic. En cas d’urgence ou de doute important,
                contactez immédiatement un professionnel de santé.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("## Exemples")
    examples = [
        "Douleur thoracique, essoufflement, palpitations",
        "Constipation avec ballonnements et douleurs abdominales",
        "Tristesse persistante, anxiété, insomnie",
        "Douleur pelvienne et saignement inhabituel",
    ]
    for item in examples:
        st.sidebar.caption(f"• {item}")


def render_red_flag_alert(red_flags: list[dict], warning_text: str) -> None:
    if not red_flags:
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
        return

    severities = {flag["severity"].lower() for flag in red_flags}
    samu = "high" in severities or "critical" in severities

    if samu:
        st.markdown(
            """
            <div class="blinking-alert">
                <div style="font-size:1.08rem;font-weight:800;margin-bottom:0.3rem;">
                    Urgence détectée : Contactez immédiatement le SAMU (15)
                </div>
                <div style="font-size:0.96rem;line-height:1.55;">
                    Un ou plusieurs signaux d’alerte forts ont été identifiés dans la description fournie.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    items = "".join(
        [
            f"<li><strong>{flag['keyword']}</strong> — {flag['message']} "
            f"(niveau : {severity_label(flag['severity'])})</li>"
            for flag in red_flags
        ]
    )
    st.markdown(
        f"""
        <div class="warning-box">
            <strong>Signaux d’alerte détectés</strong>
            <ul style="margin-top:0.55rem;margin-bottom:0.15rem;">
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
                <strong>Message système</strong><br>
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
            cols = st.columns([2.4, 1.25, 1.15, 1.35])

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
                chips = "".join([f'<span class="chip">{sp}</span>' for sp in specialties])
                st.markdown(chips, unsafe_allow_html=True)


def render_recommendations(recommendations: list[dict]) -> None:
    st.markdown('<div class="section-title">Spécialités recommandées</div>', unsafe_allow_html=True)

    if not recommendations:
        st.warning("Aucune recommandation n’a pu être générée.")
        return

    score_rows = []
    for index, rec in enumerate(recommendations, start=1):
        score = float(rec.get("similarity_score", 0))
        score_rows.append(
            {
                "Rang": index,
                "Spécialité": rec.get("specialty_name", "Inconnue"),
                "Score": round(score * 100, 2),
            }
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div>
                    <span class="result-rank">{index}</span>
                    <span class="result-title">{rec.get("specialty_name", "Spécialité inconnue")}</span>
                </div>
                <div class="result-score">Niveau de correspondance : {format_score(score)}</div>
            </div>
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
                    Cette spécialité ressort comme l’une des plus pertinentes selon l’analyse
                    sémantique et les règles métier appliquées.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("<br>", unsafe_allow_html=True)

    df = pd.DataFrame(score_rows)
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("Spécialité:N", sort=None, title="Spécialité"),
            y=alt.Y("Score:Q", title="Score (%)"),
            tooltip=["Spécialité", "Score"]
        )
        .properties(height=280)
    )
    st.altair_chart(chart, use_container_width=True)


def render_meta(meta: dict[str, Any]) -> None:
    if not meta:
        return

    st.markdown('<div class="section-title">Indicateurs d’exécution</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temps de réponse", f"{meta.get('response_time_ms', 0)} ms")
    c2.metric("Jetons consommés", meta.get("total_tokens", 0))
    c3.metric("Cache hits", meta.get("cache_hits", 0))
    c4.metric("Cache misses", meta.get("cache_misses", 0))


def render_admin_panel() -> None:
    st.markdown('<div class="section-title">Panel Admin — Monitoring avancé</div>', unsafe_allow_html=True)

    metrics_data = api_get("/admin/metrics")
    history = api_get("/admin/history")
    cache_rows = api_get("/admin/genai-cache")

    kpis = metrics_data["kpis"]
    history_df = pd.DataFrame(history)
    if not history_df.empty:
        history_df["created_at"] = pd.to_datetime(history_df["created_at"])
        history_df = history_df.sort_values("created_at")

    top1, top2, top3, top4, top5 = st.columns(5)
    top1.metric("Requêtes totales", kpis["total_requests"])
    top2.metric("Latence moyenne", f"{kpis['average_response_time_ms']} ms")
    top3.metric("Jetons totaux", kpis["total_tokens"])
    top4.metric("Entrées cache", kpis["cache_entries"])
    top5.metric("Alertes SAMU", kpis["samu_alert_count"])

    mid1, mid2, mid3 = st.columns(3)
    mid1.metric("Prompt tokens", kpis["prompt_tokens"])
    mid2.metric("Completion tokens", kpis["completion_tokens"])
    mid3.metric("Taux cache hit", f"{kpis['cache_hit_ratio_percent']} %")

    if history_df.empty:
        st.info("Aucune donnée de monitoring disponible pour le moment.")
        return

    col_chart_1, col_chart_2 = st.columns(2, gap="large")

    with col_chart_1:
        latency_chart = (
            alt.Chart(history_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("created_at:T", title="Horodatage"),
                y=alt.Y("response_time_ms:Q", title="Latence (ms)"),
                tooltip=["created_at:T", "response_time_ms:Q", "top_specialty:N"]
            )
            .properties(height=300, title="Évolution de la latence")
        )
        st.altair_chart(latency_chart, use_container_width=True)

    with col_chart_2:
        token_chart = (
            alt.Chart(history_df)
            .mark_bar()
            .encode(
                x=alt.X("created_at:T", title="Horodatage"),
                y=alt.Y("total_tokens:Q", title="Jetons"),
                color=alt.Color("samu_advised:N", title="SAMU conseillé"),
                tooltip=["created_at:T", "total_tokens:Q", "prompt_tokens:Q", "completion_tokens:Q"]
            )
            .properties(height=300, title="Consommation de jetons")
        )
        st.altair_chart(token_chart, use_container_width=True)

    cache_df = pd.DataFrame(
        [
            {"Type": "Cache hits", "Valeur": int(history_df["cache_hits"].sum())},
            {"Type": "Cache misses", "Valeur": int(history_df["cache_misses"].sum())},
        ]
    )
    security_df = pd.DataFrame(
        [
            {"Type": "Red flags détectés", "Valeur": int(history_df["red_flag_triggered"].sum())},
            {"Type": "SAMU conseillé", "Valeur": int(history_df["samu_advised"].sum())},
        ]
    )

    col_chart_3, col_chart_4 = st.columns(2, gap="large")

    with col_chart_3:
        cache_chart = (
            alt.Chart(cache_df)
            .mark_arc(innerRadius=55)
            .encode(
                theta="Valeur:Q",
                color="Type:N",
                tooltip=["Type", "Valeur"]
            )
            .properties(height=300, title="Répartition cache IA")
        )
        st.altair_chart(cache_chart, use_container_width=True)

    with col_chart_4:
        security_chart = (
            alt.Chart(security_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x="Type:N",
                y="Valeur:Q",
                color="Type:N",
                tooltip=["Type", "Valeur"]
            )
            .properties(height=300, title="Suivi sécurité")
        )
        st.altair_chart(security_chart, use_container_width=True)

    st.markdown('<div class="section-title">Historique des requêtes</div>', unsafe_allow_html=True)
    display_cols = [
        "id",
        "created_at",
        "symptom_description",
        "top_specialty",
        "response_time_ms",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "cache_hits",
        "cache_misses",
        "red_flag_triggered",
        "samu_advised",
    ]
    st.dataframe(history_df[display_cols], use_container_width=True, height=360)

    st.markdown('<div class="section-title">État du cache IA</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(cache_rows), use_container_width=True, height=240)


def build_dynamic_hints(profile: str) -> tuple[list[str], str]:
    if profile == "Cardio-respiratoire":
        return (
            ["poitrine", "thorax", "respiration"],
            "Exemple : douleur thoracique, palpitations, essoufflement à l'effort."
        )
    if profile == "Digestif":
        return (
            ["abdomen", "ventre", "estomac"],
            "Exemple : constipation, ballonnements, douleurs abdominales, nausées."
        )
    if profile == "Neurologique":
        return (
            ["tête", "visage", "bras", "jambe"],
            "Exemple : maux de tête, vertiges, faiblesse d'un bras, trouble de la parole."
        )
    if profile == "Psychique":
        return (
            ["général", "sommeil", "humeur"],
            "Exemple : tristesse persistante, anxiété, insomnie, perte d'intérêt."
        )
    if profile == "Uro-gynécologique":
        return (
            ["bassin", "bas ventre", "urinaire"],
            "Exemple : douleur pelvienne, brûlures urinaires, saignement anormal."
        )
    return (
        ["poitrine", "tête", "abdomen", "bassin", "général"],
        "Exemple : décrivez le symptôme principal, sa durée, son intensité et son contexte."
    )


def main() -> None:
    st.set_page_config(
        page_title="MABOU",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    render_styles()
    render_sidebar()
    render_header()

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None

    if "form_profile" not in st.session_state:
        st.session_state["form_profile"] = "Général"

    left, right = st.columns([1.18, 0.82], gap="large")

    with left:
        st.markdown('<div class="section-title">Formulaire dynamique d’analyse</div>', unsafe_allow_html=True)

        profile = st.selectbox(
            "Famille de symptômes dominante",
            ["Général", "Cardio-respiratoire", "Digestif", "Neurologique", "Psychique", "Uro-gynécologique"],
            key="form_profile",
        )
        suggested_locations, placeholder = build_dynamic_hints(profile)

        with st.form("medical_orientation_form", clear_on_submit=False):
            symptom_description = st.text_area(
                "Description des symptômes *",
                placeholder=placeholder,
                height=165,
            )

            c1, c2 = st.columns(2)

            with c1:
                intensity_label = st.selectbox("Intensité", ["", "Faible", "Modérée", "Élevée", "Très élevée"])
                duration = st.text_input("Durée", placeholder="Exemple : depuis 2 jours, depuis ce matin")

            with c2:
                location = st.selectbox(
                    "Localisation suggérée",
                    [""] + suggested_locations + ["autre"],
                )
                location_free = st.text_input("Localisation libre", placeholder="Exemple : poitrine, abdomen, bassin")
                additional_context = st.text_input(
                    "Contexte additionnel",
                    placeholder="Exemple : enceinte, diabétique, après effort, fièvre",
                )

            submitted = st.form_submit_button("Lancer l’analyse", use_container_width=True)

        if submitted:
            if len(symptom_description.strip()) < 3:
                st.error("Veuillez décrire les symptômes avec au moins 3 caractères.")
            else:
                final_location = location_free.strip() if location == "autre" else (location or location_free.strip() or None)

                payload = {
                    "symptom_description": symptom_description.strip(),
                    "intensity": intensity_to_api(intensity_label),
                    "duration": duration.strip() or None,
                    "location": final_location,
                    "additional_context": additional_context.strip() or None,
                }

                with st.spinner("Analyse MABOU en cours..."):
                    try:
                        data = api_post("/recommendations/", payload)
                    except requests.exceptions.ConnectionError:
                        st.error("Impossible de joindre l’API. Vérifiez que le backend FastAPI est démarré.")
                        data = None
                    except requests.exceptions.Timeout:
                        st.error("Le délai de réponse de l’API a été dépassé.")
                        data = None
                    except requests.exceptions.HTTPError as exc:
                        response_text = exc.response.text if exc.response is not None else str(exc)
                        st.error(f"Erreur HTTP côté API : {response_text}")
                        data = None
                    except Exception as exc:
                        st.error(f"Erreur inattendue : {exc}")
                        data = None

                st.session_state["last_result"] = data

    with right:
        st.markdown('<div class="section-title">Vue synthétique</div>', unsafe_allow_html=True)
        last_result = st.session_state.get("last_result")

        if not last_result:
            st.markdown(
                """
                <div class="info-box">
                    <strong>Aucune analyse en cours</strong><br>
                    Saisissez un cas clinique, lancez l’analyse, puis consultez ici la synthèse,
                    les red flags, les symptômes détectés et les indicateurs techniques.
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
            meta = last_result.get("meta", {})

            m1, m2, m3 = st.columns(3)
            m1.metric("Spécialités", len(recommendations))
            m2.metric("Symptômes détectés", len(detected_symptoms))
            m3.metric("Red flags", len(red_flags))

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

            render_red_flag_alert(red_flags, warning_text)
            render_meta(meta)

    last_result = st.session_state.get("last_result")
    if last_result:
        st.divider()
        bottom_left, bottom_right = st.columns([1.12, 0.88], gap="large")

        with bottom_left:
            render_recommendations(last_result.get("recommendations", []))

        with bottom_right:
            render_detected_symptoms(last_result.get("detected_symptoms", []))

    if st.session_state.get("admin_authenticated"):
        st.divider()
        render_admin_panel()


if __name__ == "__main__":
    main()