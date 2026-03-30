# AI-Review-Insights
Python-based web scraper + LLM pipeline for automated sentiment analysis and structured insights generation.
📊 Product Review Scraper with Gemini Sentiment Analysis
A Python application that scrapes product data (used as review-like content), analyzes it using Google Gemini API, and stores the results in a CSV file.

🌐 Data Source
https://books.toscrape.com/catalogue/page-1.html

This site is used because:

It is stable and scraping-friendly
No bot protection (unlike Amazon)
Ideal for demonstrating scraping + LLM pipeline
📁 Project Structure
review_scraper/ ├── main.py # Main script (scraper + Gemini analysis) ├── requirements.txt # Dependencies ├── README.md # Documentation ├── scraper.log # Logs (auto-generated) └── output.csv # Output file

⚙️ Setup
1. Install dependencies
pip install -r requirements.txt

2. Set API Key (IMPORTANT)
Windows PowerShell: $env:GEMINI_API_KEY="your_api_key_here"

Linux / Mac: export GEMINI_API_KEY="your_api_key_here"

▶️ Run the Project
python main.py

📦 Output
output.csv

📊 Output Columns
review_id → Book title
author → Source (catalogue)
rating → None
title → Book title
date → Scraped date
verified → False
body → Generated text
sentiment → positive / neutral / negative
score → 0–1
summary → One-line summary

🧠 Gemini Integration
Uses Google Gemini API (google-genai)
Model: gemini-2.0-flash
Converts text → structured JSON
Extracts sentiment, score, summary
🛠️ Features
Web scraping using BeautifulSoup
Retry mechanism for failed requests
User-agent rotation
Structured LLM output
CSV export using pandas
⚠️ Limitations
Data is simulated (books instead of real reviews)
Gemini may sometimes return invalid JSON
Processing is sequential (can be slow)
🔒 Security
Never hardcode API keys
Always use environment variables
Regenerate key if exposed
🚀 Future Improvements
Add charts (matplotlib / seaborn)
Streamlit dashboard
Async scraping
Real e-commerce scraping with proxies
✅ Pipeline Overview
Scraper → Data → Gemini API → Sentiment Analysis → CSV Output

Simple, clean, and ready for extension. EOF
