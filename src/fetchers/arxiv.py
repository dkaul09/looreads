import feedparser

ARXIV_CATEGORIES = [
    ("cs.AI", "AI"),
    ("cs.LG", "ML"),
    ("cs.CL", "NLP"),
    ("cs.CV", "Vision"),
    ("cs.RO", "Robotics"),
]


def fetch_recent_papers(max_per_category: int = 8) -> list[dict]:
    papers = []
    for cat, label in ARXIV_CATEGORIES:
        try:
            feed = feedparser.parse(
                f"https://rss.arxiv.org/rss/{cat}",
                request_headers={"User-Agent": "LooReads/1.0"},
            )
            for entry in feed.entries[:max_per_category]:
                # Strip HTML tags from summary
                summary = entry.get("summary", "")
                if "<" in summary:
                    import re
                    summary = re.sub(r"<[^>]+>", "", summary)
                papers.append({
                    "title": entry.get("title", "").replace("\n", " "),
                    "summary": summary[:400].strip(),
                    "url": entry.get("link", ""),
                    "category": label,
                })
        except Exception:
            continue
    return papers
