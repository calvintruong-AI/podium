# Project Phases

## Phase 1 — Interactive Coach + Training Mode
**Status: Complete**

A full practice environment with two modes: a coaching session that scores full stories across 5 dimensions, and a training mode with targeted micro-exercises and drill accountability.

### Coach Scope
- Streamlit web UI with tab-based interface
- Track selection: Professional or General Narrative
- Claude-powered story analysis across 5 dimensions
- Personalized drill generation (drill targets weakest dimension)
- Session persistence to SQLite
- Score history per session

### Training Scope
- Dimension-targeted micro-exercises (Structure, Language, Pacing, Emotion)
- Dynamic exercise generation via Claude — always fresh, never repetitive
- Three difficulty levels: Beginner, Intermediate, Advanced
- **Coach's Pick** — auto-selects weakest dimension from recent sessions
- **Auto difficulty** — sets level based on recent average score for the dimension
- **Drill accountability check** — prompts completion of pending coaching drill before each training session
- Three accountability responses: mark complete, do it now, skip
- Try Again / New Exercise / Change Dimension options after each result
- Training session persistence to SQLite

### Deliverables
- [x] Streamlit app skeleton (tabbed: Coach + Training)
- [x] Claude integration (analysis prompt)
- [x] Session manager
- [x] SQLite schema (sessions + training_sessions tables)
- [x] Score normalization
- [x] Drill generator with dimension tracking
- [x] Docker setup
- [x] Training exercise generation (training_prompts.py + trainer.py)
- [x] Exercise evaluation (dimension-focused scoring)
- [x] Drill accountability flow
- [x] Coach's Pick + Auto difficulty logic

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
- Line charts: each dimension over time (coach and training sessions combined)
- Claude-narrated growth arc summary
- Session timeline with drill completion history

### Deliverables
- [ ] Dashboard UI skeleton
- [ ] Plotly radar + line chart components
- [ ] Claude growth arc prompt
- [ ] Data aggregation queries (coach + training sessions)
