# 📄 AI-Powered Invoice Risk Analyzer

An intelligent web application that analyzes invoices using AI to detect risk levels and automatically trigger email alerts using workflow automation.

---

## 🚀 Live Demo

(https://invoice-risk-analyzer.streamlit.app/)

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
* **Programming Language:** Python
* **AI Processing:** Google Gemini API (gemini-2.5-flash)
* **Workflow Automation:** n8n
* **API Communication:** REST (requests library)
* **Data Processing & Dashboard:** Pandas
* **PDF Parsing:** pdfplumber

---

## 🔄 End-to-End Workflow

1. **User uploads invoice (PDF/TXT)** in Streamlit UI
2. **Text extraction** is performed using pdfplumber
3. **Gemini API** analyzes invoice and returns structured JSON
4. **Risk Level is determined** (Low / Medium / High)
5. **Result is cached** to avoid reprocessing on reruns
6. **User triggers email alert** from UI
7. **Payload sent to n8n webhook**
8. **n8n IF node evaluates risk**

   * If High → Generate email + send via Gmail
   * Else → Return safe response
9. **Response sent back to Streamlit** and displayed to user

---

## 🔗 Workflow Automation (n8n)

* Receives structured invoice data from Streamlit
* Uses **IF node** to evaluate `risk` field
* Generates dynamic email content using AI node
* Sends email alerts via Gmail node
* Returns response back to Streamlit app

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
2. Connect repository to Streamlit Cloud
3. Add secrets in deployment settings
4. Deploy 🚀

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

* Prevented duplicate invoice processing (Streamlit rerun issue)
* Ensured consistent AI output using caching
* Fixed webhook data mismatch between Streamlit & n8n
* Stabilized risk classification across interactions

---

## 📌 Future Improvements

* 📥 Download reports (PDF/Excel)
* 🔐 User authentication
* 📊 Advanced analytics dashboard
* 🌍 Multi-language support

---



---
