# Podium

An AI-powered public speaking and storytelling coach. Practice, record, analyze, and track your growth across the core dimensions of great storytelling.

## What it does

- **Interactive Coach** — conversational practice sessions with story prompts, real-time feedback, and personalized drills
- **Async Analysis Pipeline** — submit audio/video recordings for deep transcription and multi-dimensional analysis
- **Progress Dashboard** — track improvement across five skill dimensions over time

## Skill Dimensions

| Dimension | What gets measured |
|---|---|
| Structure | Hook, tension, turning point, resolution, takeaway |
| Language | Specificity, sensory detail, active voice, vividness |
| Pacing | Sentence variety, rhythm, filler words |
| Emotion | Stakes, vulnerability, universal theme connection |
| Delivery | Speaking rate, pauses, vocal variety *(audio only)* |

## Tech Stack

| Layer | Technology |
|---|---|
| Coach UI | Python + Streamlit |
| Workflow orchestration | n8n |
| Transcription | Whisper (Docker) |
| AI Analysis | Claude (Anthropic) + Gemini (Google) |
| Storage | SQLite (Phase 1) → Postgres (Phase 2+) |
| Infrastructure | Docker Compose |

## Tracks

- **Professional** — STAR framework, Problem→Stakes→Solution→Proof, "So what?" discipline
- **General Narrative** — Pixar story spine, specificity, emotional stakes, the unexpected detail

## Project Structure

```
podium/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── phases.md
│   ├── skill-dimensions.md
│   └── setup.md
├── app/                    # Phase 1: Streamlit interactive coach
├── pipeline/               # Phase 2: n8n + Whisper + analysis
├── dashboard/              # Phase 3: progress tracking
├── docker-compose.yml
└── .env.example
```

## Quick Start

See [docs/setup.md](docs/setup.md) for full setup instructions.

## Roadmap

See [docs/phases.md](docs/phases.md) for current phase status and upcoming work.
