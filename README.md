# AI-Review-Insights
Python-based web scraper + LLM pipeline for automated sentiment analysis and structured insights generation.
📊 Product Review Scraper 
A Python application that scrapes product data (used as review-like content), analyzes it , and stores the results in a CSV file.

cat << 'EOF' > README.md


A Python project that scrapes product data and uses Google Gemini API to perform sentiment analysis and generate insights.

---

## 🚀 How to Run the Project

### 1. Clone the repository

git clone https://github.com/yourusername/gemini-review-analyzer.git
cd gemini-review-analyzer

---

### 2. Install dependencies

pip install -r requirements.txt

---

### 3. Set your Gemini API key

Windows (PowerShell):
$env:GEMINI_API_KEY="your_api_key_here"

Linux / Mac:
export GEMINI_API_KEY="your_api_key_here"

---

### 4. Run the application

python main.py

---

## 📦 Output

After running, a file will be generated:

output.csv

---

## 📊 What the Output Contains

Each row includes:
- review_id
- title
- body
- sentiment (positive / neutral / negative)
- score (0–1)
- summary

---

## ⚠️ Important Notes

- Make sure your API key is valid
- Do not share your API key publicly
- Ensure dependencies are installed

---

## 🛠 Requirements

- Python 3.8+
- Internet connection
- Gemini API key

---
Done by Satyam......

## ✅ Pipeline

Scraping → Data Processing → Gemini API → Sentiment Analysis → CSV Output

---

Simple and ready to run.
EOF
