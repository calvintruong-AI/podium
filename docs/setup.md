# Setup Guide

## Prerequisites

- Python 3.11+
- Docker + Docker Compose
- Git
- Anthropic API key (Claude)
- Google AI API key (Gemini) — required for Phase 2+

---

## 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/podium.git
cd podium
```

## 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys. Never commit the `.env` file.

---

## 3. Local Development (Phase 1)

```bash
cd app
pip install -r requirements.txt
streamlit run main.py
```

The coach UI will be available at `http://localhost:8501`.

---

## 4. Linux Server Deployment

### Option A: Docker Compose (recommended)

```bash
docker compose up -d
```

Services started:

| Service | Port | Phase |
|---|---|---|
| `app` | 8501 | Phase 1+ |
| `pipeline` (n8n) | 5678 | Phase 2+ |
| `whisper` | 9000 | Phase 2+ |
| `db` (Postgres) | 5432 | Phase 2+ |

### Option B: Manual

Run each component individually. See component READMEs in `app/`, `pipeline/`, and `dashboard/`.

---

## 5. Environment Variables

See `.env.example` for all required variables.

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Phase 1+ | Claude API key |
| `GOOGLE_API_KEY` | Phase 2+ | Gemini API key |
| `DB_URL` | Phase 2+ | Postgres connection string |
| `DB_PASSWORD` | Phase 2+ | Postgres password |
| `WHISPER_MODEL` | Phase 2+ | Model size: base / small / medium / large |
| `STREAMLIT_PORT` | Optional | Default: 8501 |
| `N8N_PORT` | Optional | Default: 5678 |

---

## 6. Data Privacy

Story submissions, session transcripts, and recordings are stored **locally only** and are excluded from version control via `.gitignore`.

The `data/` directory is never committed to the repo. Keep all practice material there.

---

## 7. Whisper Model Size Guide

| Model | Size | Speed | Accuracy | Recommended for |
|---|---|---|---|---|
| `base` | ~150MB | Fast | Good | Quick iteration, short clips |
| `small` | ~500MB | Moderate | Better | Default for most use |
| `medium` | ~1.5GB | Slow | High | Important recordings |
| `large` | ~3GB | Slowest | Best | Final analysis, presentations |

Start with `small` on the Linux server unless storage is constrained.
