import re
import feedparser
import httpx

COMPANY_FEEDS = {
    "OpenAI":       "https://openai.com/news/rss.xml",
    "GitHub":       "https://github.blog/feed/",
    "Google AI":    "https://research.google/blog/rss/",
    "Apple ML":     "https://machinelearning.apple.com/rss.xml",
    "AWS":          "https://aws.amazon.com/blogs/aws/feed/",
    "Microsoft AI": "https://blogs.microsoft.com/ai/feed/",
    "Netflix Tech": "https://netflixtechblog.com/feed",
    "Meta Eng":     "https://engineering.fb.com/feed/",
    "NVIDIA":       "https://developer.nvidia.com/blog/feed/",
}

_SKIP_WORDS = {"curator", "webinar", "sponsor", "subscribe", "podcast", "hiring"}
_TITLE_SKIP = {"Announcements", "Products", "Research", "Company"}
_HTML_ENTITIES = {"&amp;": "&", "&#x27;": "'", "&quot;": '"', "&lt;": "<", "&gt;": ">"}


def _clean(text: str) -> str:
    for entity, char in _HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return re.sub(r"<[^>]+>", "", text).strip()


def _fetch_anthropic(max_posts: int = 8) -> list[dict]:
    try:
        html = httpx.get("https://www.anthropic.com/news", timeout=12, follow_redirects=True).text
    except Exception:
        return []

    paths = list(dict.fromkeys(re.findall(r'href="(/news/[a-z0-9-]+)"', html)))
    skip = {"Announcements", "Products", "Research", "Apr", "Jan", "Feb", "Mar", "May",
            "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Company", "All"}
    results = []
    for path in paths:
        idx = html.find(f'href="{path}"')
        snippet = html[idx:idx + 800]
        candidates = re.findall(r">([A-Z][^<]{14,120})<", snippet)
        title = next(
            (_clean(t) for t in candidates if not any(t.startswith(s) for s in skip)),
            path.split("/")[-1].replace("-", " ").title(),
        )
        results.append({
            "title": title,
            "url": f"https://www.anthropic.com{path}",
            "source": "Anthropic",
        })
        if len(results) >= max_posts:
            break
    return results


def fetch_bigtech_news(max_per_source: int = 5) -> list[dict]:
    articles = []

    # Anthropic (no RSS — scrape)
    articles.extend(_fetch_anthropic(max_per_source))

    # RSS-based sources
    for company, url in COMPANY_FEEDS.items():
        try:
            feed = feedparser.parse(url, request_headers={"User-Agent": "LooReads/1.0"})
            for entry in feed.entries[:max_per_source]:
                title = entry.get("title", "").strip()
                if not title or any(w in title.lower() for w in _SKIP_WORDS):
                    continue
                articles.append({
                    "title": title,
                    "url": entry.get("link", ""),
                    "source": company,
                })
        except Exception:
            continue

    return articles
