# Project Phases

## Phase 1 — Interactive Coach
**Status: In Progress**

A conversational practice environment. Session-based: receive a prompt, submit a story, get structured feedback, receive a drill.

### Scope
- Streamlit web UI with chat-style interface
- Track selection: Professional or General Narrative
- Claude-powered story analysis across 5 dimensions
- Personalized drill generation
- Session persistence to SQLite
- Score history per session

### Deliverables
- [ ] Streamlit app skeleton
- [ ] Claude integration (analysis prompt)
- [ ] Session manager
- [ ] SQLite schema
- [ ] Score normalization
- [ ] Drill generator
- [ ] Docker setup

---

## Phase 2 — Async Analysis Pipeline
**Status: Planned**

Deep analysis of recorded speeches, presentations, or drafted stories submitted outside of a live session.

### Scope
- n8n workflow orchestration
- Whisper (Docker) for audio/video transcription
- Claude + Gemini parallel analysis
- Unified scoring synthesis
- Markdown/HTML report output
- Postgres for scalable storage
- Delivery rate, filler word detection, pace metrics

### Deliverables
- [ ] n8n workflow design
- [ ] Whisper Docker container
- [ ] Gemini integration
- [ ] Report template
- [ ] Postgres schema migration from SQLite
- [ ] File watcher / webhook trigger

---

## Phase 3 — Progress Dashboard
**Status: Planned**

Visualize growth across skill dimensions over time.

### Scope
- Streamlit dashboard (separate from coach UI, or tabbed)
- Radar chart: current skill profile
- Line charts: each dimension over time
- Claude-narrated growth arc summary
- Session timeline with drill history

### Deliverables
- [ ] Dashboard UI skeleton
- [ ] Plotly radar + line chart components
- [ ] Claude growth arc prompt
- [ ] Data aggregation queries
