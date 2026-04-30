import re
from datetime import datetime
import feedparser
import httpx
from src.fetchers.utils import clean_url

_FEED_URL = "https://tldr.tech/api/rss/ai"
_SKIP = {"Headlines", "Deep Dives", "Engineering", "Quick Links",
         "Analysis", "Research", "Miscellaneous", "Launches"}
_HTML_ENTITIES = {"&#x27;": "'", "&amp;": "&", "&#x2F;": "/", "&quot;": '"'}


def _clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip()
    for entity, char in _HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text


def fetch_todays_articles(max_articles: int = 10) -> list[dict]:
    feed = feedparser.parse(_FEED_URL)
    if not feed.entries:
        return []

    today = datetime.now().strftime("%Y-%m-%d")
    edition_url = feed.entries[0].get("link", f"https://tldr.tech/ai/{today}")

    try:
        html = httpx.get(edition_url, timeout=15, follow_redirects=True).text
    except Exception:
        return []

    h3s = [
        (m.start(), m.end(), _clean(m.group(1)))
        for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", html, re.DOTALL)
    ]

    articles = []
    for i, (start, end, title) in enumerate(h3s):
        if (any(s in title for s in _SKIP)
                or "Sponsor" in title
                or "curator" in title.lower()
                or not title):
            continue

        title = re.sub(r"\s*\(\d+ minute read\)", "", title)

        prev_end = h3s[i - 1][1] if i > 0 else 0
        before_block = html[prev_end:start]
        hrefs = re.findall(r'href="(https?://(?!pages\.aws)[^"&]+)', before_block)
        url = hrefs[0] if hrefs else ""

        if not url or "tldr.tech" in url:
            continue

        articles.append({"title": title, "url": clean_url(url), "source": "TLDR AI"})
        if len(articles) >= max_articles:
            break

    return articles
