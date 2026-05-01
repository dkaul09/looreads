import feedparser
import httpx
from concurrent.futures import ThreadPoolExecutor

HN_API = "https://hacker-news.firebaseio.com/v0"
YC_BLOG_RSS = "https://www.ycombinator.com/blog.rss"


def _fetch_hn_item(item_id: int) -> dict | None:
    try:
        with httpx.Client(timeout=5) as client:
            return client.get(f"{HN_API}/item/{item_id}.json").json()
    except Exception:
        return None


def fetch_yc_blog(max_posts: int = 8) -> list[dict]:
    try:
        feed = feedparser.parse(YC_BLOG_RSS)
        return [
            {"title": e.get("title", ""), "url": e.get("link", ""), "source": "YC Blog"}
            for e in feed.entries[:max_posts]
            if e.get("title") and e.get("link")
        ]
    except Exception:
        return []


def fetch_show_hn(limit: int = 20) -> list[dict]:
    try:
        with httpx.Client(timeout=10) as client:
            ids = client.get(f"{HN_API}/showstories.json").json()[:limit]
        with ThreadPoolExecutor(max_workers=10) as ex:
            items = list(ex.map(_fetch_hn_item, ids))
        return [
            {"title": s["title"], "url": s.get("url", f"https://news.ycombinator.com/item?id={s['id']}"),
             "score": s.get("score", 0), "comments": s.get("descendants", 0), "source": "Show HN"}
            for s in items if s and s.get("title")
        ]
    except Exception:
        return []


def fetch_ask_hn(limit: int = 10) -> list[dict]:
    try:
        with httpx.Client(timeout=10) as client:
            ids = client.get(f"{HN_API}/askstories.json").json()[:limit]
        with ThreadPoolExecutor(max_workers=8) as ex:
            items = list(ex.map(_fetch_hn_item, ids))
        return [
            {"title": s["title"], "url": f"https://news.ycombinator.com/item?id={s['id']}",
             "score": s.get("score", 0), "comments": s.get("descendants", 0), "source": "Ask HN"}
            for s in items if s and s.get("title")
        ]
    except Exception:
        return []
