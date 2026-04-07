# 📄 AI Invoice Risk Analyzer

A production-style AI application that analyzes invoices, detects financial risk, and automatically triggers alert workflows.

---

## 🚀 Live Application

(https://invoice-risk-analyzer.streamlit.app/)

---

## 💡 What This Project Does

This tool helps identify risky invoices by extracting key financial details using AI and classifying them into **Low, Medium, or High risk**.

For high-risk invoices, it automatically triggers an email alert using workflow automation.

---

## 🔍 Problem It Solves

Manual invoice review is:

* Time-consuming
* Error-prone
* Hard to scale

This project automates:
✔ Data extraction
✔ Risk detection
✔ Alerting system

---

## ⚙️ How It Works

1. Upload invoice (PDF/TXT)
2. AI extracts structured data
3. Risk level is determined
4. Dashboard updates instantly
5. Email alert is triggered (via n8n)

---

## 🧠 Key Features

* 📄 Multi-file invoice upload
* 🤖 AI-powered data extraction (Gemini)
* ⚠️ Risk classification system
* 📊 Real-time dashboard
* 📧 Automated email alerts
* 🔁 Smart caching to avoid duplicate processing

---

## 🏗️ Architecture Overview

Streamlit App → Gemini API → Risk Detection → n8n Webhook → Email Alert

---

## 📊 Sample Output

```json
{
  "Invoice ID": "INV-2024-001",
  "Vendor Name": "XYZ Traders",
  "Amount": "₹1,20,000",
  "Due Date": "2026-04-15",
  "Risk Level": "High"
}
```

---

## 🧪 Key Challenges & Solutions

### 1. Duplicate Invoice Processing

**Issue:** Streamlit reruns caused repeated processing
**Fix:** Implemented session-based caching

---

### 2. Inconsistent Risk Classification

**Issue:** AI returned different results on rerun
**Fix:** Stored AI output per file

---

### 3. n8n Risk Mismatch

**Issue:** Workflow recalculated risk incorrectly
**Fix:** Passed risk explicitly from Streamlit

---

## 📁 Project Structure

```
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone repo

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add secrets

Create `.streamlit/secrets.toml`:

```
GEMINI_API_KEY = "your_key"
N8N_WEBHOOK_URL = "your_webhook"
```

### 4. Run app

```
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using Streamlit Community Cloud.

---

## 🚀 Future Improvements

* Export reports (PDF/Excel)
* Advanced fraud detection logic
* User authentication
* Invoice history tracking

---

