# 📄 AI-Powered Invoice Risk Analyzer

An intelligent web application that analyzes invoices using AI to detect risk levels and automatically trigger email alerts using workflow automation.

---

## 🚀 Live Demo

👉 (Add your Streamlit app link here after deployment)

---

## 🧠 Features

* 📁 Upload PDF/TXT invoices
* 🤖 AI-powered data extraction using Gemini
* ⚠️ Automatic Risk Classification (Low / Medium / High)
* 📊 Interactive Risk Dashboard
* 📧 Email Alerts via n8n automation
* 🔁 Smart caching to avoid duplicate processing

---

## 🏗️ Tech Stack

* **Frontend & App Framework:** Streamlit
* **AI Processing:** Google Gemini API
* **Automation:** n8n
* **Backend Logic:** Python
* **Data Handling:** Pandas

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add secrets

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
N8N_WEBHOOK_URL = "your_n8n_webhook_url"
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This app is deployed using **Streamlit Community Cloud**.

### Steps:

1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Add secrets in deployment settings
4. Deploy 🚀

---

## 🔗 Workflow Automation (n8n)

* Receives invoice data from Streamlit
* Uses IF node for risk detection
* Sends alert emails for high-risk invoices

---

## 📊 Example Output

```json
{
  "Invoice ID": "INV-1023",
  "Vendor Name": "ABC Pvt Ltd",
  "Amount": "₹75,000",
  "Due Date": "2026-04-10",
  "Risk Level": "High"
}
```

---

## 🚨 Challenges Solved

* Prevented duplicate invoice processing
* Ensured consistent AI results using caching
* Fixed webhook data mismatch between Streamlit & n8n
* Handled Streamlit rerun issues

---

## 📌 Future Improvements

* 📥 Download reports (PDF/Excel)
* 🔐 User authentication
* 📊 Advanced analytics dashboard
* 🌍 Multi-language support

---
