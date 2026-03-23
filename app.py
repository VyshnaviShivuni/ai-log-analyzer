# ============================================
# AI Log Analyzer - Streamlit Application
# ============================================

# -------------------------------
# Imports
# -------------------------------
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Log Analyzer", layout="wide")

# -------------------------------
# Custom Styling (Premium UI)
# -------------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.main { background-color: #0e1117; }

h1 { color: #ffffff; font-weight: 700; }

textarea {
    background-color: #1e1e1e !important;
    color: white !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
}

[data-testid="stFileUploader"] {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 12px;
}

.card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key not found. Please configure the .env file.")
    st.stop()

# -------------------------------
# Initialize Client
# -------------------------------
client = Groq(api_key=api_key)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.title("AI Log Analyzer")
    st.markdown("### Controls")
    st.markdown("Upload logs and analyze issues using AI")
    st.caption("AI-powered debugging assistant")

# -------------------------------
# Main Title
# -------------------------------
st.title("AI Log Analyzer")
st.caption("Upload logs and generate AI-powered root cause analysis")

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload log file (.txt/.log)", type=["txt", "log"])

with col2:
    mode = st.selectbox("Analysis Mode", [
        "Standard",
        "Root Cause Only",
        "Concise"
    ])

# -------------------------------
# Read File
# -------------------------------
logs = ""

if uploaded_file is not None:
    logs = uploaded_file.read().decode("utf-8")
    st.markdown("### Log Preview")
    st.code(logs, language="bash")

# -------------------------------
# User Instructions
# -------------------------------
user_instruction = st.text_input(
    "Additional Instructions (Optional)",
    placeholder="e.g., Focus on database errors, analyze deeply"
)

# -------------------------------
# Analyze Button
# -------------------------------
st.markdown("### Ready to Analyze?")
if st.button("Analyze Logs"):

    if not logs:
        st.warning("Please upload a log file before proceeding.")
        st.stop()

    # -------------------------------
    # Dynamic Prompt
    # -------------------------------
    if mode == "Root Cause Only":
        prompt = f"""
        You are a senior production support engineer.

        Provide ONLY the root cause.

        Do NOT include anything else.

        Logs:
        {logs}

        Instructions:
        {user_instruction}
        """

    elif mode == "Concise":
        prompt = f"""
        Analyze logs and give:
        - Error
        - Root Cause

        Keep it short.

        Logs:
        {logs}

        Instructions:
        {user_instruction}
        """

    else:
        prompt = f"""
        Analyze logs and provide:

        Error:
        Severity:
        Root Cause:
        Suggested Fix:
        Client Message:

        Logs:
        {logs}

        Instructions:
        {user_instruction}
        """

    # -------------------------------
    # Call LLM
    # -------------------------------
    with st.spinner("Analyzing logs..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

    # -------------------------------
    # Output Card
    # -------------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Analysis Results")

    if "ERROR" in logs:
        st.markdown("**Warning:** Errors detected in logs.")

    # Save history
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(result)

    # Download button
    st.download_button(
        "Download Report",
        result,
        file_name="log_analysis.txt"
    )

    # Display output
    if "High" in result:
        st.error(result)
    elif "Medium" in result:
        st.warning(result)
    else:
        st.success(result)

    st.markdown('</div>', unsafe_allow_html=True)