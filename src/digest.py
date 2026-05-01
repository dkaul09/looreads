import anthropic
from datetime import datetime
from src.config import ANTHROPIC_API_KEY

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def _trim(text: str) -> str:
    start = text.find("\U0001f5de")
    text = text[start:] if start != -1 else text
    end = text.find("_Read in the loo")
    if end != -1:
        text = text[:end + len("_Read in the loo, not in a meeting._")]
    return text.strip()


# ── Message 1: AI & Tech digest ──────────────────────────────────────────────

_DIGEST_PROMPT = (
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

    user_content = (
        f"Date: {today}\n\n"
        f"=== TLDR AI (pick top 2) ===\n"
        + "\n".join(f"• {a['title']}\n  {a['url']}" for a in tldr[:10])
        + f"\n\n=== HACKER NEWS TOP STORIES ===\n"
        + "\n".join(f"• {s['title']} ({s.get('score',0)} pts)\n  {s.get('url','')}" for s in hn_stories[:40])
        + f"\n\n=== ARXIV RECENT PAPERS ===\n"
        + "\n".join(f"• [{p['category']}] {p['title']}\n  {p['summary']}\n  {p['url']}" for p in papers[:30])
        + f"\n\n=== TECH NEWS RSS ===\n"
        + "\n".join(f"• [{a['source']}] {a['title']}\n  {a['url']}" for a in tech_news[:35])
    )

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=_DIGEST_PROMPT.format(date=today),
        messages=[{"role": "user", "content": user_content}],
    )
    return _trim(response.content[0].text)


# ── Message 2: YC + Hacker News digest ───────────────────────────────────────

_YC_HN_PROMPT = (
    "You are the editor of LooReads — daily digest for senior software engineers.\n\n"
    "This is Message 2: YC & Hacker News.\n\n"
    "HARD LIMIT: total output MUST be under 1300 characters.\n\n"
    "Your job: pick the 5–7 most interesting items from YC blog posts, Show HN launches, "
    "and Ask HN threads. Prioritise:\n"
    "- New YC blog posts on fundraising, hiring, or company building with genuine insight\n"
    "- Show HN launches that are technically interesting or solve a real problem\n"
    "- Ask HN threads with unusually good signal (high engagement, expert discussion)\n"
    "Skip anything generic, motivational, or obviously self-promotional.\n\n"
    "Tone: peer-to-peer. No preamble, no filler.\n\n"
    "Format — exactly this:\n"
    "\U0001f5de️ *LooReads: YC & HN* — {date}\n\n"
    "[emoji] *Title* — One sentence on why it's worth reading. URL\n"
    "... 5–7 items total ...\n\n"
    "_Read in the loo, not in a meeting._\n\n"
    "Emoji guide: \U0001f680 launch · \U0001f4ac discussion · \U0001f4dd YC blog · \U0001f4a1 insight\n"
    "No section headers. URL inline. Sentences under 110 chars."
)


def generate_yc_hn_digest(
    yc_blog: list[dict],
    show_hn: list[dict],
    ask_hn: list[dict],
) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")

    user_content = (
        f"Date: {today}\n\n"
        f"=== YC BLOG ===\n"
        + "\n".join(f"• {a['title']}\n  {a['url']}" for a in yc_blog[:8])
        + f"\n\n=== SHOW HN (new launches) ===\n"
        + "\n".join(f"• {s['title']} ({s.get('score',0)} pts, {s.get('comments',0)} comments)\n  {s['url']}" for s in show_hn[:20])
        + f"\n\n=== ASK HN (discussions) ===\n"
        + "\n".join(f"• {s['title']} ({s.get('score',0)} pts, {s.get('comments',0)} comments)\n  {s['url']}" for s in ask_hn[:10])
    )

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=_YC_HN_PROMPT.format(date=today),
        messages=[{"role": "user", "content": user_content}],
    )
    return _trim(response.content[0].text)


# ── Message 3: Big Tech digest ────────────────────────────────────────────────

_BIGTECH_PROMPT = (
    "You are the editor of LooReads — daily digest for senior software engineers.\n\n"
    "This is Message 3: Big Tech & AI Companies.\n\n"
    "HARD LIMIT: total output MUST be under 1300 characters.\n\n"
    "Your job: pick 5–7 items about meaningful developments from major tech companies — "
    "Meta, Apple, Netflix, Google/DeepMind, Amazon/AWS, Microsoft, OpenAI, Anthropic, GitHub, NVIDIA. "
    "Sources include official blog posts AND third-party news articles about these companies.\n\n"
    "Rules:\n"
    "- Only include a company if something genuinely new happened — don't force coverage of every company\n"
    "- Prioritise: new model releases, API changes, research breakthroughs, significant product shifts\n"
    "- Skip: routine partnerships, executive hires, funding rounds without technical substance, "
    "anything already covered in today's main digest\n"
    "- If it's a slow news day for a company, omit them — don't pad\n\n"
    "Tone: peer-to-peer. No preamble, no filler.\n\n"
    "Format — exactly this:\n"
    "\U0001f5de️ *LooReads: Big Tech* — {date}\n\n"
    "[emoji] *Company — Title* — One sentence on the implication. URL\n"
    "... 5–7 items total ...\n\n"
    "_Read in the loo, not in a meeting._\n\n"
    "Emoji guide: \U0001f916 AI/model · \U0001f6e0️ product · \U0001f4c8 business · \U0001f52c research\n"
    "No section headers. URL inline. Sentences under 110 chars."
)


def generate_bigtech_digest(
    bigtech_posts: list[dict],
    hn_stories: list[dict],
    tech_news: list[dict],
) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")

    user_content = (
        f"Date: {today}\n\n"
        f"=== OFFICIAL COMPANY BLOGS ===\n"
        + "\n".join(f"• [{a['source']}] {a['title']}\n  {a['url']}" for a in bigtech_posts[:50])
        + f"\n\n=== HACKER NEWS (for company coverage) ===\n"
        + "\n".join(f"• {s['title']} ({s.get('score',0)} pts)\n  {s.get('url','')}" for s in hn_stories[:40])
        + f"\n\n=== TECH NEWS RSS (for company coverage) ===\n"
        + "\n".join(f"• [{a['source']}] {a['title']}\n  {a['url']}" for a in tech_news[:35])
    )

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=_BIGTECH_PROMPT.format(date=today),
        messages=[{"role": "user", "content": user_content}],
    )
    return _trim(response.content[0].text)
