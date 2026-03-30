import os
import time
import json
import logging
import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
import pandas as pd
from google import genai   # ✅ NEW SDK

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("scraper.log")],
)
log = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
RATE_LIMIT_DELAY = 2.0
REQUEST_DELAY = 2.0
MAX_RETRIES = 3

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]

def _make_headers(index: int = 0) -> dict:
    return {"User-Agent": USER_AGENTS[index % len(USER_AGENTS)]}

# ─────────────────────────────────────────────────────────────────────────────
# Base scraper
# ─────────────────────────────────────────────────────────────────────────────

class BaseScraper:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self._ua_idx = 0

    def _get(self, url: str) -> Optional[BeautifulSoup]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.session.headers.update(_make_headers(self._ua_idx))
                self._ua_idx += 1
                r = self.session.get(url, timeout=15)
                r.raise_for_status()
                time.sleep(REQUEST_DELAY)
                return BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                log.warning(f"Retry {attempt}: {e}")
                time.sleep(2 ** attempt)
        return None

    def scrape(self, max_pages: int = 3):
        raise NotImplementedError

# ─────────────────────────────────────────────────────────────────────────────
# Books Scraper
# ─────────────────────────────────────────────────────────────────────────────

class BooksScraper(BaseScraper):
    BASE = "https://books.toscrape.com"

    def scrape(self, max_pages=3):
        all_books = []
        url = self.url
        page = 1

        while page <= max_pages:
            soup = self._get(url)
            if not soup:
                break

            for article in soup.select("article.product_pod"):
                title = article.select_one("h3 a")["title"]
                price = article.select_one("p.price_color").text
                availability = article.select_one("p.availability").text.strip()

                body = f"{title}. Price: {price}. Availability: {availability}"

                all_books.append({
                    "review_id": title,
                    "author": "catalogue",
                    "rating": None,
                    "title": title,
                    "date": datetime.now().date().isoformat(),
                    "verified": False,
                    "body": body
                })

            next_btn = soup.select_one("li.next a")
            if not next_btn:
                break

            url = f"{self.BASE}/catalogue/{next_btn['href']}"
            page += 1

        return all_books

def get_scraper(url: str):
    return BooksScraper(url)

# ─────────────────────────────────────────────────────────────────────────────
# Gemini LLM Analyser (FIXED)
# ─────────────────────────────────────────────────────────────────────────────

class LLMAnalyser:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)

    def analyse(self, text: str):
        prompt = f"""
Analyze this review and return JSON:
sentiment: positive | neutral | negative
score: 0 to 1
summary: one sentence
key_points: max 3

Review:
{text}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",   # ✅ WORKING MODEL
                contents=prompt
            )

            raw = response.text

            # Extract JSON safely
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group(0))

        except Exception as e:
            log.warning(f"Gemini error: {e}")

        return {
            "sentiment": "neutral",
            "score": 0.5,
            "summary": "N/A",
            "key_points": []
        }

# ─────────────────────────────────────────────────────────────────────────────
# Pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run(url: str):
    scraper = get_scraper(url)
    reviews = scraper.scrape()

    if not reviews:
        log.error("No data scraped")
        return

    analyser = LLMAnalyser()

    results = []
    for i, r in enumerate(reviews, 1):
        log.info(f"Processing {i}/{len(reviews)}")

        analysis = analyser.analyse(r["body"])

        r.update({
            "sentiment": analysis["sentiment"],
            "score": analysis["score"],
            "summary": analysis["summary"]
        })

        results.append(r)

    df = pd.DataFrame(results)
    df.to_csv("output.csv", index=False)

    print("\n✅ Done! Saved to output.csv")

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run("https://books.toscrape.com/catalogue/page-1.html")