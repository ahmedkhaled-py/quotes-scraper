# quotes-scraper

A polite web scraper that collects quotes from
[quotes.toscrape.com](https://quotes.toscrape.com) (a sandbox site made for
scraping practice) and saves them to CSV and JSON.

## Features

- Follows pagination automatically up to a page limit
- Extracts quote text, author, and tags
- Writes both `quotes.csv` (Excel-ready) and `quotes.json` (nested, tags as a list)
- 1-second delay between pages and a descriptive User-Agent
- Clear errors on HTTP failures via `requests.raise_for_status`

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scraper.py                # 3 pages -> quotes.csv / quotes.json
python scraper.py --pages 10 --out data/all_quotes
```

Requires Python 3.9+.
