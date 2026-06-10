# ask-gdpr — Design Spec (v1)

**Date:** 2026-06-11
**Status:** Approved by Shahin (brainstorming session)
**Repo:** github.com/ShahinMirJalili/ask-gdpr (public, portfolio)
**Local path:** `~/projects/github-portfolio/ask-gdpr/`

## What

A RAG (Retrieval-Augmented Generation) web app that answers questions about the GDPR (DSGVO). User asks a question in German, the app retrieves the most relevant GDPR articles, and Claude answers **only** from those articles, citing article numbers.

## Why

1. **Portfolio piece #1** for Shahin's AI-developer portfolio (Masterschool "AI for Developers" track, started 2026-06-09). Research (June 2026) shows hiring managers want production signals: evals, error handling, guardrails, decision documentation — not "completed a course".
2. **Learning vehicle:** v1 architecture is deliberately matched to Shahin's current level (Python OOP week 1: classes, `__init__`, lists, for-loops). The repo grows with the course ("mitwachsend").

## Core decisions (with reasoning — these go into the README)

| Decision | Choice | Why |
|---|---|---|
| Build mode | Grows with learning level | v1 fully explainable in interviews; evolution documented in README is itself a hiring signal |
| Corpus | GDPR legal text, all 99 articles | Public domain, cleanly structured (perfect chunks), no privacy issues in a public repo, instantly understandable use case |
| Retrieval v1 | Keyword scoring (lowercase word overlap, loop over list) | Matches week-1 Python level; measurable baseline for the v2 embeddings comparison |
| LLM | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | Cheap, fast, sufficient for context-grounded answering; cost cap via `max_tokens` |
| Evals | From day 1: retrieval hit-rate (expected article in top-3) | Eval literacy = hiring signal #1; this eval is simple enough to fully understand and defend |
| Guardrail | System prompt: answer ONLY from provided articles, cite numbers, else say "not covered by the GDPR" | Anti-hallucination; demonstrable guardrail thinking |
| Repo language | English README + code comments (simple, clear English) | Portfolio standard. App UI itself is German (German users, German law) |
| Repo name | `ask-gdpr` | Short, says what it does |
| Deployment v1 | Local only; demo GIF + screenshots in README | A public deployment would spend Shahin's API key on strangers; live deploy is a later milestone with rate limiting |
| Git identity | `shahinmirjalili5@gmail.com` (repo-local config) | Verified primary email of the ShahinMirJalili account — commits must count in the contribution graph |

## Architecture

```
ask-gdpr/
├── app.py                      # Flask app: GET / (chat UI), POST /api/ask
├── retrieval.py                # Article class + keyword-scoring search
├── claude_client.py            # Claude API call: builds prompt with context articles
├── data/
│   └── gdpr_articles.json      # 99 articles: {number, title, text, chapter}
├── scripts/
│   └── build_dataset.py        # one-off: fetch + parse GDPR text into the JSON
├── evals/
│   ├── questions.json          # ~30 test questions + expected article numbers
│   └── run_evals.py            # measures retrieval hit-rate (top-3), prints score table
├── templates/index.html        # chat UI (vanilla HTML/CSS/JS, no framework)
├── static/style.css
├── tests/test_retrieval.py     # pytest: Article class, scoring, edge cases
├── .env.example                # ANTHROPIC_API_KEY=...
├── .gitignore                  # .env, __pycache__, venv
├── requirements.txt            # flask, anthropic, python-dotenv, pytest
└── README.md                   # decisions, eval scores, architecture, roadmap
```

### Components

**`retrieval.py`** — the learning core.
- `Article` class: `__init__(number, title, text, chapter)`, attributes, a `score(question_words)` method that counts keyword overlap (lowercased word set intersection). Mirrors the `Product` class pattern from Shahin's OOP course.
- `load_articles(path)` → list of `Article` (mirrors the `Store` list pattern).
- `search(question, articles, top_k=3)` → top-k articles by score; for-loop + sort. Stop-word list (German) to avoid scoring on "der/die/das".

**`claude_client.py`**
- `ask_claude(question, articles)` → builds a prompt: system rules (German answer, cite article numbers, refuse if not in context), user question + the top-3 article texts. Calls Messages API, `max_tokens` capped (~1024). Returns answer text.

**`app.py`**
- `GET /` renders chat page.
- `POST /api/ask` — JSON `{question}`: validate (non-empty, length ≤ 500 chars), retrieve, call Claude, return `{answer, sources: [{number, title}]}`.

**`evals/run_evals.py`**
- Loads `questions.json` (each: `{question, expected_articles: [..]}`).
- For each question: run retrieval, check if any expected article is in top-3.
- Prints: per-question hit/miss + overall hit-rate %. This number goes into the README. When v2 (embeddings) lands, the same eval produces the comparison table keyword vs. embeddings.

### Data flow

```
question (German)
  → retrieval.search() scores all 99 articles, returns top 3
  → claude_client.ask_claude() with the 3 article texts as context
  → Claude Haiku answers, citing article numbers (or refuses)
  → UI shows answer + source articles
```

### Dataset

`scripts/build_dataset.py` fetches the German GDPR text (public domain, e.g. from gesetze-im-internet.de / EUR-Lex) once and parses it into `gdpr_articles.json`. The JSON is committed so the app works without network/scraping at runtime.

## Error handling

- API error / timeout → HTTP 502 with friendly German message ("Gerade nicht erreichbar, versuch's gleich nochmal."), logged server-side. No stack traces to the user.
- Empty/too-long question → HTTP 400 with message.
- Retrieval finds nothing relevant (all scores 0) → skip the API call, answer "Dazu habe ich in der DSGVO nichts gefunden." (saves cost, honest behavior).
- Missing `ANTHROPIC_API_KEY` → clear startup error, app refuses to run.

## Security / privacy

- API key only via `.env` (gitignored); `.env.example` documents it.
- Input length limit (500 chars), `max_tokens` cap → cost control.
- No user data stored, no tracking, no cookies → the GDPR app is itself GDPR-compliant (README selling point).
- No deployment in v1 → no public abuse surface.

## Testing

- `pytest` for `retrieval.py`: Article construction, scoring (known question → known top article), edge cases (empty question, umlauts, stop words).
- Evals (`run_evals.py`) are the behavioral test of retrieval quality.
- Manual verification: run Flask locally, ask 5 known questions, screenshot for README.

## Roadmap (documented in README, built as the course progresses)

| Version | What | When (course alignment) |
|---|---|---|
| **v1** | Keyword retrieval + Claude + evals + chat UI | now (OOP week 1-2) |
| v2 | Embeddings + cosine similarity (in-memory, numpy); eval comparison v1 vs v2 | ~OOP weeks 3-4 / advanced |
| v3 | pgvector/Supabase, promptfoo evals, PDF upload for own documents | Term 2 (LLM & GenAI courses) |
| later | Live deployment with rate limiting | when v2/v3 stable |

## Out of scope (v1)

- User accounts, sessions, history
- PDF upload / own documents
- Embeddings, vector DB
- Deployment
- Multi-language UI

## Learning protocol

Shahin writes the `Article` class and the search loop himself (weekend repetition exercise, Claude guides only). Claude builds dataset script, Flask wiring, UI, and evals scaffold — each explained in simple German during the build.
