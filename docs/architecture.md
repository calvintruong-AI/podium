# Architecture

## System Overview

Podium operates on two parallel paths that share a common storage layer and scoring model.

```
┌─────────────────────────────────────────────────────────┐
│                        USER                              │
└────────────┬────────────────────────┬───────────────────┘
             │ text / session          │ audio / video / draft
             ▼                         ▼
    ┌─────────────────┐      ┌──────────────────────┐
    │  Interactive    │      │   Async Pipeline     │
    │  Coach          │      │   n8n orchestration  │
    │  Streamlit UI   │      │                      │
    └────────┬────────┘      └──────────┬───────────┘
             │                          │
             │               ┌──────────▼───────────┐
             │               │  Whisper (Docker)    │
             │               │  Transcription       │
             │               └──────────┬───────────┘
             │                          │
             ▼                          ▼
    ┌─────────────────────────────────────────────┐
    │              Analysis Layer                  │
    │   Claude (Anthropic)   Gemini (Google)       │
    │   - story structure    - language quality    │
    │   - emotional arc      - pacing analysis     │
    │   - coaching response  - delivery feedback   │
    └─────────────────────┬───────────────────────┘
                          │
             ┌────────────▼────────────┐
             │     Scoring Engine      │
             │     Python              │
             │     5-dimension score   │
             └────────────┬────────────┘
                          │
             ┌────────────▼────────────┐
             │       Storage           │
             │  SQLite → Postgres      │
             │  sessions, scores,      │
             │  transcripts, drills    │
             └────────────┬────────────┘
                          │
             ┌────────────▼────────────┐
             │  Progress Dashboard     │
             │  Streamlit + Plotly     │
             └─────────────────────────┘
```

## Component Responsibilities

### Interactive Coach (Phase 1)
- Manages practice sessions (context selection, prompt delivery, submission)
- Sends story text to Claude for analysis
- Returns structured feedback and a personalized drill
- Persists session data to SQLite

### Async Pipeline (Phase 2)
- n8n workflow triggered by file drop or webhook
- Whisper handles audio/video → transcript
- Claude and Gemini run analysis in parallel on the transcript
- Python synthesizes scores and generates a Markdown/HTML report

### Analysis Layer

Claude and Gemini are used for different strengths:

| Model | Primary responsibilities |
|---|---|
| Claude | Narrative structure, emotional arc, coaching voice, drill generation |
| Gemini | Language quality, pacing metrics, delivery feedback from transcript |

### Scoring Engine
- Normalizes Claude and Gemini outputs into 5-dimension scores (0–100)
- Tracks score history per dimension per session
- Feeds trend data to the dashboard

### Progress Dashboard (Phase 3)
- Radar chart showing current skill profile
- Line charts showing each dimension over time
- Claude-narrated growth arc summary

---

## Data Flow — Interactive Session

```
1. User selects track (professional / general)
2. Coach generates a story prompt via Claude
3. User submits story text
4. Claude analyzes across 5 dimensions
5. Scores normalized and saved to SQLite
6. Feedback + next drill returned to UI
```

## Data Flow — Async Analysis

```
1. User drops audio/video file into watched folder (or webhook)
2. n8n triggers Whisper transcription
3. Transcript sent to Claude + Gemini in parallel
4. Results synthesized into unified score
5. Markdown report generated and saved
6. Score appended to Postgres for dashboard
```

---

## Key Design Decisions

- **SQLite in Phase 1, Postgres in Phase 2+** — SQLite removes infrastructure friction during development. Postgres is introduced with the async pipeline when multi-service access to storage is needed.
- **Claude + Gemini in parallel** — Each model has distinct strengths. Running them in parallel on the same transcript and synthesizing results produces richer feedback than either alone.
- **n8n for orchestration** — Provides a visual workflow editor, built-in retry logic, and easy webhook/file trigger support without custom queue infrastructure.
- **Streamlit for UI** — Python-native, no frontend build toolchain, Dockerizable. Fast to iterate on during Phase 1.
