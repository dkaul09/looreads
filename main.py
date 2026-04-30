#!/usr/bin/env python3
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("looreads")


def run():
    from src.fetchers.hackernews import fetch_top_stories
    from src.fetchers.arxiv import fetch_recent_papers
    from src.fetchers.rss import fetch_tech_news
    from src.digest import generate_digest
    from src.whatsapp import send_digest

    log.info("Fetching Hacker News top stories...")
    hn_stories = fetch_top_stories(50)
    log.info(f"  → {len(hn_stories)} stories")

    log.info("Fetching ArXiv papers...")
    papers = fetch_recent_papers(8)
    log.info(f"  → {len(papers)} papers")

    log.info("Fetching tech news RSS feeds...")
    tech_news = fetch_tech_news(6)
    log.info(f"  → {len(tech_news)} articles")

    log.info("Generating digest with Claude...")
    digest = generate_digest(hn_stories, papers, tech_news)
    log.info(f"  → {len(digest)} chars")

    log.info("Sending via WhatsApp...")
    send_digest(digest)
    log.info("LooReads delivered. Enjoy the read.")


if __name__ == "__main__":
    run()
