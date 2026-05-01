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
    from src.fetchers.tldr import fetch_todays_articles
    from src.fetchers.yc import fetch_yc_blog, fetch_show_hn, fetch_ask_hn
    from src.fetchers.bigtech import fetch_bigtech_news
    from src.digest import generate_digest, generate_yc_hn_digest, generate_bigtech_digest
    from src.whatsapp import send_digest

    # Fetch all sources
    log.info("Fetching TLDR AI...")
    tldr = fetch_todays_articles(10)
    log.info(f"  → {len(tldr)} articles")

    log.info("Fetching Hacker News...")
    hn_stories = fetch_top_stories(50)
    log.info(f"  → {len(hn_stories)} stories")

    log.info("Fetching ArXiv papers...")
    papers = fetch_recent_papers(8)
    log.info(f"  → {len(papers)} papers")

    log.info("Fetching tech news RSS...")
    tech_news = fetch_tech_news(6)
    log.info(f"  → {len(tech_news)} articles")

    log.info("Fetching YC blog + Show HN + Ask HN...")
    yc_blog = fetch_yc_blog(8)
    show_hn = fetch_show_hn(20)
    ask_hn = fetch_ask_hn(10)
    log.info(f"  → {len(yc_blog)} YC posts, {len(show_hn)} Show HN, {len(ask_hn)} Ask HN")

    log.info("Fetching big tech company news...")
    bigtech = fetch_bigtech_news(5)
    log.info(f"  → {len(bigtech)} posts")

    # Generate the three digests
    log.info("Generating Message 1: AI & Tech digest...")
    msg1 = generate_digest(tldr, hn_stories, papers, tech_news)
    log.info(f"  → {len(msg1)} chars")

    log.info("Generating Message 2: YC & HN digest...")
    msg2 = generate_yc_hn_digest(yc_blog, show_hn, ask_hn)
    log.info(f"  → {len(msg2)} chars")

    log.info("Generating Message 3: Big Tech digest...")
    msg3 = generate_bigtech_digest(bigtech, hn_stories, tech_news)
    log.info(f"  → {len(msg3)} chars")

    # Send all three
    log.info("Sending via WhatsApp...")
    send_digest(msg1)
    send_digest(msg2)
    send_digest(msg3)
    log.info("All three LooReads messages delivered.")


if __name__ == "__main__":
    run()
