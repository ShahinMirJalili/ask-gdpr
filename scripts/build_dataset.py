"""One-off script: fetch the German GDPR text and build data/gdpr_articles.json.

Source: https://dsgvo-gesetz.de (per-article pages). Run once; the JSON is
committed so the app never needs network access at runtime.
"""
import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dsgvo-gesetz.de/art-{n}-dsgvo/"
OUT_PATH = Path(__file__).parent.parent / "data" / "gdpr_articles.json"

# GDPR chapter boundaries: chapter number -> first article number
CHAPTER_STARTS = {1: 1, 2: 5, 3: 12, 4: 24, 5: 44, 6: 51, 7: 60, 8: 77, 9: 85, 10: 92, 11: 94}

# Non-article elements inside entry-content (verified against the real HTML)
JUNK_SELECTORS = (
    ".empfehlung-erwaegungsgruende, .page-navigation, .link-to-overview, "
    ".feedback, nav, aside, footer"
)


def chapter_for(article_number):
    chapter = 1
    for chap, start in sorted(CHAPTER_STARTS.items()):
        if article_number >= start:
            chapter = chap
    return chapter


def fetch_article(n):
    response = requests.get(BASE_URL.format(n=n), timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", class_="entry-title").find("span", class_="dsgvo-title").get_text(strip=True)
    body = soup.find("div", class_="entry-content")
    for junk in body.select(JUNK_SELECTORS):
        junk.decompose()
    text = body.get_text(" ", strip=True)
    return {"number": n, "title": title, "text": text, "chapter": chapter_for(n)}


def main():
    articles = []
    for n in range(1, 100):
        try:
            articles.append(fetch_article(n))
            print(f"fetched article {n}")
        except requests.RequestException as error:
            print(f"SKIPPED article {n}: {error}")
        time.sleep(0.5)  # be polite
    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(articles)} articles to {OUT_PATH}")


if __name__ == "__main__":
    main()
