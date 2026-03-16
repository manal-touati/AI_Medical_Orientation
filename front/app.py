import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

GENERIC_EXPLANATION_MARKERS = [
    "may be relevant based on the semantic similarity",
    "rule-based matching",
    "This is not a medical diagnosis",
]

def is_generic_explanation(text: str) -> bool:
    return any(marker.lower() in text.lower() for marker in GENERIC_EXPLANATION_MARKERS)

st.set_page_config(page_title="AI Medical Orientation", page_icon="🏥", layout="centered")
st.title("🏥 AI Medical Orientation")
st.caption("Describe your symptoms to get guidance toward the most relevant medical specialty.")
st.warning("⚠️ This tool is for informational purposes only and does not replace a medical diagnosis.")

with st.form("form"):
    symptom_description = st.text_area("Symptom description *", placeholder="e.g. chest pain and difficulty breathing since this morning...", height=120)
    col1, col2 = st.columns(2)
    with col1:
        intensity = st.selectbox("Intensity", ["", "mild", "moderate", "high", "very high"])
        duration = st.text_input("Duration", placeholder="e.g. 2 days, 1 week...")
    with col2:
        location = st.text_input("Location", placeholder="e.g. chest, head, leg...")
        additional_context = st.text_input("Additional context", placeholder="e.g. diabetic, pregnant...")
    submitted = st.form_submit_button("🔍 Get orientation", use_container_width=True)

if submitted:
    if len(symptom_description.strip()) < 3:
        st.error("Please describe your symptoms (minimum 3 characters).")
    else:
        payload = {
            "symptom_description": symptom_description.strip(),
            "intensity": intensity or None,
            "duration": duration.strip() or None,
            "location": location.strip() or None,
            "additional_context": additional_context.strip() or None,
        }
        with st.spinner("Analyzing your symptoms..."):
            try:
                resp = requests.post(f"{API_URL}/recommendations", json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the API. Make sure the server is running on localhost:8000.")
                st.stop()
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                st.stop()

        if data.get("red_flags"):
            st.error("🚨 Warning signs detected — seek emergency care if needed!")
            for flag in data["red_flags"]:
                icon = "🔴" if flag["severity"] == "critical" else "🟠"
                st.markdown(f"{icon} **{flag['keyword']}** — {flag['message']}")
            st.divider()

        st.subheader("📋 Recommended specialties")
        for i, rec in enumerate(data.get("recommendations", [])):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "•"
            score = int(rec["similarity_score"] * 100)
            with st.expander(f"{medal} {rec['specialty_name']} — {score}% match", expanded=(i == 0)):
                st.progress(rec["similarity_score"])
                explanation = rec.get("explanation", "")
                if explanation and not is_generic_explanation(explanation):
                    st.markdown(explanation)
                else:
                    st.markdown(
                        f"Based on your symptoms, **{rec['specialty_name']}** is among the most relevant specialties "
                        f"with a match score of **{score}%**. Consider consulting a specialist in this field."
                    )

        if data.get("warning"):
            st.info(f"ℹ️ {data['warning']}")
