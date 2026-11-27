
import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(
    page_title="PromptLens | AI Security Lab",
    page_icon="🛡️",
    layout="centered"
)

@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "promptlens_v2_filtered.joblib"
    return joblib.load(model_path)

model = load_model()

st.title(" PromptLens")
st.subheader("AI Security Detection & Evaluation Lab")

st.write(
    "Analyze text using a machine-learning classifier "
    "trained to identify potentially malicious prompts."
)

prompt = st.text_area(
    "Enter a prompt to analyze:",
    height=180,
    placeholder="Paste your prompt here..."
)

if st.button("Analyze Prompt", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        prediction = int(model.predict([prompt])[0])
        score = float(model.decision_function([prompt])[0])

        if prediction == 1:
            st.error("Prediction: Potentially Malicious")
        else:
            st.success("Prediction: Benign")

        st.metric("Decision Score", f"{score:.4f}")

        st.caption(
            "Positive scores favor the malicious class; "
            "negative scores favor the benign class. "
            "Decision scores are not probabilities."
        )

st.divider()

st.markdown("### V2 Validation Performance")

col1, col2, col3 = st.columns(3)

col1.metric("Validation F1", "95.70%")
col2.metric("Malicious Recall", "95.88%")
col3.metric("False Positive Rate", "5.90%")
st.info(
    "PromptLens v2 is an experimental research prototype. "
    "Its reported performance comes from validation data. "
    "False positives and missed attacks remain possible. "
    "It is not suitable as a standalone security control."
)

st.caption("PromptLens v2.0 (Experimental) | TF-IDF + LinearSVC")
