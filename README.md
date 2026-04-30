# 🚽 LooReads

> *Because your best reading happens in a 3-minute window with the door locked.*

LooReads is a daily AI-curated tech digest delivered to your WhatsApp every morning at 7:30 AM — timed perfectly for your morning constitutional. No app to open, no feed to doom-scroll, no algorithm trying to keep you engaged. Just the 5 most important things happening in tech today and one research paper, waiting for you before you've even washed your hands.

## Why does this exist?

There are approximately 4,000 tech newsletters, 12 RSS readers, and one Hacker News that will happily consume your entire morning if you let them. LooReads doesn't want your morning. It wants 3 minutes of your time in the one room where you're guaranteed to be alone.

It's written for engineers who've been around long enough to know the difference between a genuine architectural shift and a Medium post with a clickbait title. No tutorials. No "10 things you didn't know about Python". No hype. Just signal.

## What's in it

Every morning you get:

- **5 articles** — AI-first, with a slot or two for meaningful developments in languages, tooling, or engineering practice. If it wouldn't make a senior engineer raise an eyebrow, it's cut.
- **1 research paper** — one ArXiv paper worth knowing about. Flagged for what's genuinely novel vs. yet another benchmark claim.

Curated by Claude, delivered by Twilio, read in the loo.

## Stack

- **News sources**: Hacker News API, ArXiv (cs.AI, cs.LG, cs.CL, cs.CV, cs.RO), and RSS feeds from Ars Technica, The Verge, MIT Tech Review, Wired, TechCrunch, VentureBeat, IEEE Spectrum
- **Curation**: Claude Sonnet via the Anthropic API
- **Delivery**: Twilio WhatsApp API
- **Scheduling**: GitHub Actions (runs in the cloud — your laptop can be off, closed, or also in the loo)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/dkaul09/looreads.git
cd looreads
```

### 2. Get your credentials

**Anthropic API key** — [console.anthropic.com](https://console.anthropic.com)

**Twilio WhatsApp** — [twilio.com](https://twilio.com)
1. Create a free account and navigate to Messaging → Try it out → Send a WhatsApp message
2. Follow the sandbox setup: text `join <your-keyword>` from your WhatsApp to the Twilio sandbox number
3. Grab your Account SID and Auth Token from the Console dashboard

### 3. Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `ANTHROPIC_API_KEY` | your Anthropic key |
| `TWILIO_ACCOUNT_SID` | from Twilio Console |
| `TWILIO_AUTH_TOKEN` | from Twilio Console |
| `TWILIO_WHATSAPP_FROM` | `whatsapp:+14155238886` (sandbox) |
| `RECIPIENT_PHONE` | `whatsapp:+1xxxxxxxxxx` |

### 4. Set your timezone

The cron in `.github/workflows/daily-digest.yml` defaults to **7:30 AM PDT**. Adjust for your timezone:

```yaml
- cron: "30 14 * * *"  # 7:30 AM PDT (UTC-7)
```

Some common ones:

| Timezone | Cron |
|----------|------|
| PST / UTC-8 | `30 15 * * *` |
| PDT / UTC-7 | `30 14 * * *` |
| EST / UTC-5 | `30 12 * * *` |
| GMT / UTC+0 | `30 7 * * *`  |
| BST / UTC+1 | `30 6 * * *`  |
| IST / UTC+5:30 | `0 2 * * *`  |

### 5. Test it

Go to **Actions → LooReads Daily Digest → Run workflow** to fire it manually and confirm the WhatsApp message lands.

That's it. Enjoy your morning read.

---

> ⚠️ **Twilio sandbox note**: the free sandbox connection expires after 72 hours of inactivity. If you miss a morning, just text the join keyword again. For a permanent setup, a dedicated Twilio number costs ~$1/month.

---

*Built with Claude Code. Inspired by a universal human experience.*
