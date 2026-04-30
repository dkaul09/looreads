import anthropic
from datetime import datetime
from src.config import ANTHROPIC_API_KEY

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


SYSTEM_PROMPT = (
    "You are the editor of LooReads — a no-BS morning tech digest for senior software engineers "
    "(10+ years). Sharp, time-poor, deeply technical reader. No hand-holding.\n\n"
    "Your job: produce exactly 7 items — 6 articles + 1 research paper — in ONE WhatsApp message.\n\n"
    "HARD LIMIT: total output MUST be under 1300 characters (count carefully — this is non-negotiable).\n\n"
    "Article selection (6 total):\n"
    "- Pick exactly the TOP 2 from the TLDR AI section. Take the first two that aren't fluff.\n"
    "- Pick 4 more from HN / RSS. AI is the priority — aim for 3 AI + 1 meaningful tech "
    "(language, IDE, OSS, engineering shift). No tutorials, no obvious product announcements, "
    "no duplicates of the TLDR picks.\n\n"
    "Paper (1 total):\n"
    "- Pick the single most interesting ArXiv paper. Prefer genuine novelty over benchmark climbing. "
    "Name what's new in one short clause.\n\n"
    "Tone: peer-to-peer. Dry wit welcome. No preamble, no filler.\n\n"
    "Format — exactly this, nothing else:\n"
    "\U0001f5de️ *LooReads* — {date}\n\n"
    "[emoji] *Title* — One sentence why it matters. URL\n"
    "[emoji] *Title* — One sentence. URL\n"
    "[emoji] *Title* — One sentence. URL\n"
    "[emoji] *Title* — One sentence. URL\n"
    "[emoji] *Title* — One sentence. URL\n"
    "[emoji] *Title* — One sentence. URL\n\n"
    "\U0001f4c4 *Paper: Title* — What's novel. URL\n\n"
    "_Read in the loo, not in a meeting._\n\n"
    "Emoji guide: \U0001f916 AI · \U0001f6e0️ tool/OSS · ⚡ perf · \U0001f3e2 industry · \U0001f52c engineering\n"
    "No section headers. URL inline. Each sentence under 110 chars."
)


def generate_digest(
    tldr: list[dict],
    hn_stories: list[dict],
    papers: list[dict],
    tech_news: list[dict],
) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")

    tldr_block = "\n".join(
        f"• {a['title']}\n  {a['url']}"
        for a in tldr[:10]
    )
    hn_block = "\n".join(
        f"• {s['title']} ({s.get('score', 0)} pts)\n  {s.get('url', '')}"
        for s in hn_stories[:40]
    )
    papers_block = "\n".join(
        f"• [{p['category']}] {p['title']}\n  {p['summary']}\n  {p['url']}"
        for p in papers[:30]
    )
    news_block = "\n".join(
        f"• [{a['source']}] {a['title']}\n  {a['url']}"
        for a in tech_news[:35]
    )

    user_content = (
        f"Date: {today}\n\n"
        f"=== TLDR AI (pick top 2) ===\n{tldr_block}\n\n"
        f"=== HACKER NEWS TOP STORIES ===\n{hn_block}\n\n"
        f"=== ARXIV RECENT PAPERS ===\n{papers_block}\n\n"
        f"=== TECH NEWS RSS ===\n{news_block}"
    )

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT.format(date=today),
        messages=[{"role": "user", "content": user_content}],
    )

    text = response.content[0].text
    start = text.find("\U0001f5de")
    text = text[start:] if start != -1 else text
    end = text.find("_Read in the loo")
    if end != -1:
        text = text[:end + len("_Read in the loo, not in a meeting._")]
    return text.strip()
