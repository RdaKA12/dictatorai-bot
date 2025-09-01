# dictatorai-bot

A minimal Reddit + Twitter (X) poster that **generates short, cryptic one-paragraph posts** with OpenAI and shares them on your accounts at random intervals. Safe-by-default thanks to *fail-closed* moderation and **DRY_RUN** mode.

![CI](https://img.shields.io/github/actions/workflow/status/RdaKA12/dictatorai-bot/ci.yml?branch=main&label=CI)
![python](https://img.shields.io/badge/python-3.11-blue)
![docker](https://img.shields.io/badge/docker-ready-blue)

>  **Heads-up**: Respect platform rules. Keep moderation **ON**. Default `DRY_RUN=1` prevents accidental posting.

---

## Features

-  OpenAI-powered text generation (short, mysterious style)
-  Auto-posts to **Reddit** (text post) and **Twitter (X)** (tweet)
-  Randomized schedule (min–max hours)
-  Built-in moderation (**blocklist** + model), **fail-closed**
-  Tests + CI, Docker-ready, pinned dependencies

---

## Quickstart

### 1) Clone & install
```bash
git clone https://github.com/yourname/dictatorai-bot.git
cd dictatorai-bot
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure env
Copy and edit the example:
```bash
cp .env.example .env
# fill in reddit/twitter creds if DRY_RUN=0
```

### 3) Run (default DRY_RUN)
```bash
python -m src.bot
```
You’ll see logs of what **would** be posted, but nothing is sent.

### 4) Run in Docker
```bash
docker build -t dictatorai-bot .
docker run --rm --env-file .env dictatorai-bot
```

---

## Live mode (post for real)

Set `DRY_RUN=0` in `.env`. **Required envs** then become:

- OpenAI: `OPENAI_API_KEY`
- Reddit: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_USER_AGENT`, `REDDIT_SUBREDDIT`
- Twitter: `TWITTER_BEARER_TOKEN`, `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`

If anything critical is missing, the app **exits with an error** early.

---

## Scheduling

Two knobs control the sleep window between posts:

- `POST_INTERVAL_MIN_HOURS` (default **2**)
- `POST_INTERVAL_MAX_HOURS` (default **3**)

The bot picks a random float between them each loop. Make it wider (e.g., `4`–`8`) to feel more organic and reduce rate-limit risks.

---

## Moderation & Safety

- `MODERATION=1` keeps content filtering **on**.
- Hard blocklist via `BLOCKLIST_WORDS` (comma-separated).
- Model moderation via `MODERATION_MODEL` (default `omni-moderation-latest`).
- **Fail-closed**: if moderation says *no* or errors, the text is **not** posted.

> You are responsible for complying with Reddit/Twitter rules and your local laws. This code is for educational purposes.

---

## Dev scripts

Formatting & lint:
```bash
pip install black ruff
black . && ruff check .
```

Run tests:
```bash
pip install pytest
pytest -q
```

GitHub Actions is pre-configured in `.github/workflows/ci.yml`.

---

## Project structure

```
src/
  bot.py          # main loop: generate -> moderate -> post -> sleep
  config.py       # Settings (env) + strict validation
  moderation.py   # blocklist + model moderation (fail-closed)
  prompts.py      # pool of creative prompts
tests/
  test_config.py  # minimal env validation tests
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Exits with “Missing env vars …” | `DRY_RUN=0` but creds empty | Fill `.env` or set `DRY_RUN=1` |
| 401/403 on Twitter | Wrong API keys or app permissions | Recreate keys, ensure write perms |
| Reddit post fails | Subreddit rules / title too long | Adjust `title` or subreddit config |
| Rate limited | Posting too often | Increase interval range |
| Nothing posts | Moderation blocked | Tweak prompts/blocklist, keep safe |

---

## License

MIT — see `LICENSE`.
