import feedparser
from src.fetchers.utils import clean_url

TECH_FEEDS = {
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "TechCrunch": "https://techcrunch.com/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "IEEE Spectrum": "https://spectrum.ieee.org/feeds/feed.rss",
}


def fetch_tech_news(max_per_feed: int = 6) -> list[dict]:
    articles = []
    for source, url in TECH_FEEDS.items():
        try:
            feed = feedparser.parse(
                url,
                request_headers={"User-Agent": "LooReads/1.0"},
            )
            for entry in feed.entries[:max_per_feed]:
                summary = entry.get("summary", "")
                if "<" in summary:
                    import re
                    summary = re.sub(r"<[^>]+>", "", summary)
                articles.append({
                    "title": entry.get("title", "").strip(),
                    "summary": summary[:300].strip(),
                    "url": clean_url(entry.get("link", "")),
                    "source": source,
                })
        except Exception:
            continue
    return articles
