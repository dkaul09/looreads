import anthropic
from datetime import datetime
from src.config import ANTHROPIC_API_KEY

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


SYSTEM_PROMPT = """You are the editor of LooReads — a no-BS morning tech digest for senior software engineers (10+ years). Sharp, time-poor, deeply technical reader. No hand-holding.

Your job: select exactly 6 items from the raw feed — 5 articles + 1 research paper — and write a WhatsApp digest that fits in ONE message.

HARD LIMIT: total output MUST be under 1400 characters (count carefully — this is non-negotiable).

Selection priorities:
- 5 articles: AI is the primary focus (aim for 3–4 AI items). The remaining 1–2 slots go to meaningful tech developments — new languages, IDEs, major OSS tooling, or engineering practice shifts. No industry gossip, no tutorials, no obvious announcements.
- 1 paper: pick the single most interesting ArXiv paper today. Prefer papers with real implications over benchmark chasing. Note in one clause what's novel.

Curation rules:
- Skip duplicates, beginner content, incremental product updates
- If a story has no clear "so what" for a working engineer, cut it
- Dry wit welcome; no hype

Format — exactly this structure, nothing else:
🗞️ *LooReads* — {date}

🤖 *Title* — One sentence why it matters. URL
🤖 *Title* — One sentence. URL
🤖 *Title* — One sentence. URL
[2 more articles using relevant emoji]

📄 *Paper: Title* — What's novel in one clause. URL

_Read in the loo, not in a meeting._

Emoji guide: 🤖 AI · 🛠️ tool/OSS · ⚡ perf · 🏢 industry · 🔬 engineering
No section headers. URL on the same line. Sentences under 110 chars."""


def generate_digest(
    hn_stories: list[dict],
    papers: list[dict],
    tech_news: list[dict],
) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")

    hn_block = "\n".join(
        f"• {s['title']} ({s.get('score', 0)} pts)\n  {s.get('url', '')}"
        for s in hn_stories[:40]
    )
    papers_block = "\n".join(
        f"• [{p['category']}] {p['title']}\n  {p['summary']}\n  {p['url']}"
        for p in papers[:30]
    )
    news_block = "\n".join(
        f"• [{a['source']}] {a['title']}\n  {a['summary']}\n  {a['url']}"
        for a in tech_news[:35]
    )

    user_content = f"""Date: {today}

=== HACKER NEWS TOP STORIES ===
{hn_block}

=== ARXIV RECENT PAPERS ===
{papers_block}

=== TECH NEWS RSS ===
{news_block}"""

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT.format(date=today),
        messages=[{"role": "user", "content": user_content}],
    )

    text = response.content[0].text
    start = text.find("🗞️")
    text = text[start:] if start != -1 else text
    # Cut anything after the closing tagline
    end = text.find("_Read in the loo")
    if end != -1:
        text = text[:end + len("_Read in the loo, not in a meeting._")]
    return text.strip()
