import streamlit as st
import pdfplumber
import requests
import json
import re
import pandas as pd

# ------------------------------
# CONFIG
# ------------------------------
st.set_page_config(
    page_title="Invoice Risk Analyzer",
    layout="wide",
    page_icon="📊"
)

# ------------------------------
# TITLE
# ------------------------------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>📄 AI-Powered Invoice Risk Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ------------------------------
# LOAD SECRETS
# ------------------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]

# ------------------------------
# SESSION STATE INIT
# ------------------------------
if "results" not in st.session_state:
    st.session_state.results = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}

# ------------------------------
# EMAIL VALIDATION
# ------------------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ------------------------------
# GEMINI API FUNCTION
# ------------------------------
def call_gemini_api(document_text, question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}

    prompt = f"""
    You are an AI Invoice Analyst.

    Extract 5–8 key-value pairs from the invoice to answer:
    {question}

    Also include:
    - Invoice ID
    - Vendor Name
    - Amount
    - Due Date
    - Risk Level (Low/Medium/High)

    Respond ONLY in valid JSON.

    Invoice:
    {document_text}
    """

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw_text)
        except:
            return {"raw_output": raw_text}

    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")
        return None

# ------------------------------
# INPUT SECTION
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_files = st.file_uploader(
        "📁 Upload Invoice Files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

with col2:
    user_question = st.text_input(
        "❓ Ask a Question",
        placeholder="e.g., Identify high-risk invoices"
    )

st.markdown("---")

# ------------------------------
# PROCESS FILES
# ------------------------------
if uploaded_files and user_question:

    for uploaded_file in uploaded_files:

        file_id = uploaded_file.name

        st.markdown(f"### 📄 Processing: {file_id}")

        # Extract text
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join(
                    [page.extract_text() for page in pdf.pages if page.extract_text()]
                )
        else:
            text = str(uploaded_file.read(), "utf-8")

        # Preview
        with st.expander("📄 Document Preview"):
            st.write(text[:1000] + "...")

        # ------------------------------
        # CACHE GEMINI RESULT
        # ------------------------------
        if file_id not in st.session_state.analysis_cache:
            with st.spinner("🤖 Analyzing with AI..."):
                gemini_response = call_gemini_api(text, user_question)
                st.session_state.analysis_cache[file_id] = gemini_response
        else:
            gemini_response = st.session_state.analysis_cache[file_id]

        # ------------------------------
        # DISPLAY RESULTS
        # ------------------------------
        if gemini_response:

            st.success("✅ Analysis Complete")

            colA, colB = st.columns([2, 1])

            with colA:
                st.subheader("📊 Extracted Data")
                st.json(gemini_response)

            # ------------------------------
            # RISK DETECTION
            # ------------------------------
            risk = (gemini_response.get("Risk Level") or 
                    gemini_response.get("risk_level") or "").strip().capitalize()

            with colB:
                st.subheader("⚠️ Risk Status")

                if risk:
                    if risk == "High":
                        st.error("🚨 HIGH RISK")
                    elif risk == "Medium":
                        st.warning("⚠️ MEDIUM RISK")
                    else:
                        st.success("✅ LOW RISK")

                    # Avoid duplicates
                    if file_id not in [r["file"] for r in st.session_state.results]:
                        st.session_state.results.append({"file": file_id, "risk": risk})
                else:
                    st.info("Risk not found")

            # ------------------------------
            # EMAIL SECTION
            # ------------------------------
            st.markdown("### 📧 Send Alert")

            email = st.text_input(f"Recipient Email ({file_id})", key=f"email_{file_id}")
            send_btn = st.button(f"Send Email for {file_id}", key=f"btn_{file_id}")

            if send_btn:

                if not email:
                    st.warning("Enter email")
                elif not is_valid_email(email):
                    st.warning("Invalid email")
                else:

                    payload = {
                        "document_text": text,
                        "extracted_json": gemini_response,
                        "risk": risk,  # ✅ FIXED
                        "user_question": user_question,
                        "recipient_email": email
                    }

                    try:
                        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=20)
                        response.raise_for_status()

                        webhook_response = response.json()

                        st.success("✅ Email Sent!")

                        st.write("🧠 Final Answer:", webhook_response.get("final_answer", "N/A"))
                        st.write("📨 Email Body:", webhook_response.get("email_body", "N/A"))
                        st.write("📡 Status:", webhook_response.get("status", "N/A"))

                    except Exception as e:
                        st.error(f"❌ n8n Error: {e}")

        st.markdown("---")

# ------------------------------
# DASHBOARD
# ------------------------------
st.markdown("## 📊 Risk Dashboard")

if st.session_state.results:

    df = pd.DataFrame(st.session_state.results)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Risk Distribution")
        st.bar_chart(df["risk"].value_counts())

    with col2:
        st.subheader("📊 Summary")

        total = len(df)
        high = (df["risk"] == "High").sum()
        medium = (df["risk"] == "Medium").sum()
        low = (df["risk"] == "Low").sum()

        st.metric("Total Invoices", total)
        st.metric("High Risk", high)
        st.metric("Medium Risk", medium)
        st.metric("Low Risk", low)

else:
    st.info("Upload invoices to see dashboard")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("---")
st.markdown(
    "<center>🚀 Built with Streamlit | Gemini AI | n8n Automation</center>",
    unsafe_allow_html=True
)