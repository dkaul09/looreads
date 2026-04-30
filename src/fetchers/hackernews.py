import httpx
from concurrent.futures import ThreadPoolExecutor

HN_API = "https://hacker-news.firebaseio.com/v0"


def fetch_top_stories(limit: int = 50) -> list[dict]:
    with httpx.Client(timeout=15) as client:
        ids = client.get(f"{HN_API}/topstories.json").json()[:limit]

        def fetch_item(item_id):
            try:
                return client.get(f"{HN_API}/item/{item_id}.json", timeout=5).json()
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=15) as executor:
            items = list(executor.map(fetch_item, ids))

    return [
        s for s in items
        if s and s.get("type") == "story" and s.get("url") and s.get("score", 0) > 10
    ]
