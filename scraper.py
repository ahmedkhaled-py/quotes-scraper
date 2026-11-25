#!/usr/bin/env python3
"""Scrape quotes from quotes.toscrape.com (a site built for scraping practice)
and save them to CSV and JSON.

Usage:
    python scraper.py [--pages N] [--out quotes]
"""
import argparse
import csv
import json
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"


def scrape_page(session: requests.Session, url: str) -> tuple[list[dict], str | None]:
    """Scrape one page; return (quotes, next-page-path or None)."""
    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    quotes = []
    for block in soup.select("div.quote"):
        quotes.append({
            "text": block.select_one("span.text").get_text(strip=True),
            "author": block.select_one("small.author").get_text(strip=True),
            "tags": [t.get_text(strip=True) for t in block.select("a.tag")],
        })

    next_link = soup.select_one("li.next > a")
    return quotes, (next_link["href"] if next_link else None)


def scrape(pages: int) -> list[dict]:
    session = requests.Session()
    session.headers["User-Agent"] = "quotes-scraper/1.0 (portfolio demo)"
    url, collected = BASE_URL, []
    for _ in range(pages):
        quotes, next_path = scrape_page(session, url)
        collected.extend(quotes)
        if not next_path:
            break
        url = BASE_URL + next_path
        time.sleep(1)  # be polite
    return collected


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape quotes to CSV/JSON.")
    parser.add_argument("--pages", type=int, default=3, help="Max pages to scrape")
    parser.add_argument("--out", default="quotes", help="Output file stem")
    args = parser.parse_args()

    quotes = scrape(args.pages)

    csv_path = f"{args.out}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        for q in quotes:
            writer.writerow({**q, "tags": ", ".join(q["tags"])})

    json_path = f"{args.out}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    print(f"saved {len(quotes)} quotes -> {csv_path}, {json_path}")


if __name__ == "__main__":
    main()
