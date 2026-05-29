import streamlit as st

from coach import generate_story_prompt, analyze_story
from database import init_db, save_session, get_recent_sessions

st.set_page_config(page_title="Podium", layout="wide")

init_db()

# Session state defaults
for key, default in [
    ("stage", "select_track"),
    ("track", "Professional"),
    ("prompt", ""),
    ("story", ""),
    ("analysis", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def reset():
    st.session_state.stage = "select_track"
    st.session_state.prompt = ""
    st.session_state.story = ""
    st.session_state.analysis = None


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Podium")
    st.caption("AI Storytelling Coach")

    if st.button("New Session", use_container_width=True):
        reset()
        st.rerun()

    st.divider()
    st.subheader("Recent Sessions")
    sessions = get_recent_sessions(5)
    if sessions:
        for s in sessions:
            overall = s["scores"]["overall"]
            date = s["timestamp"][:10]
            st.markdown(f"**{s['track']}** — {date}  \nOverall: **{overall}/100**")
            st.divider()
    else:
        st.caption("No sessions yet.")


# ── Stage: select track ───────────────────────────────────────────────────────

if st.session_state.stage == "select_track":
    st.title("Start a Practice Session")

    track = st.radio(
        "Choose your storytelling track:",
        ["Professional", "General Narrative"],
        captions=[
            "STAR framework — workplace situations, leadership moments, career challenges",
            "Story spine — personal experiences, emotional resonance, universal themes",
        ],
    )
    st.session_state.track = track

    if st.button("Get Story Prompt", type="primary", use_container_width=True):
        with st.spinner("Generating your prompt..."):
            st.session_state.prompt = generate_story_prompt(track)
            st.session_state.stage = "write_story"
            st.rerun()


# ── Stage: write story ────────────────────────────────────────────────────────

elif st.session_state.stage == "write_story":
    st.title(f"Practice — {st.session_state.track} Track")

    st.info(st.session_state.prompt)

    story = st.text_area(
        "Write your story:",
        height=320,
        placeholder="Begin your story here...",
    )

    ready = len(story.strip()) >= 50
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Submit", type="primary", disabled=not ready):
            with st.spinner("Analyzing your story..."):
                analysis = analyze_story(
                    st.session_state.track, st.session_state.prompt, story
                )
                save_session(st.session_state.track, st.session_state.prompt, story, analysis)
                st.session_state.story = story
                st.session_state.analysis = analysis
                st.session_state.stage = "view_results"
                st.rerun()
    with col2:
        if not ready:
            st.caption(f"{len(story.strip())}/50 characters minimum")


# ── Stage: view results ───────────────────────────────────────────────────────

elif st.session_state.stage == "view_results":
    analysis = st.session_state.analysis

    st.title("Your Feedback")

    # Overall score
    overall = analysis["scores"]["overall"]
    st.metric("Overall Score", f"{overall} / 100")

    st.divider()

    # Dimension scores
    st.subheader("Dimension Scores")
    cols = st.columns(4)
    for col, dim in zip(cols, ["structure", "language", "pacing", "emotion"]):
        with col:
            st.metric(dim.capitalize(), f"{analysis['scores'][dim]} / 100")

    st.divider()

    # Strengths
    st.subheader("Strengths")
    for strength in analysis["strengths"]:
        st.markdown(f"- {strength}")

    st.divider()

    # Dimension feedback
    st.subheader("Dimension Feedback")
    for dim in ["structure", "language", "pacing", "emotion"]:
        with st.expander(dim.capitalize()):
            st.write(analysis["feedback"][dim])

    st.divider()

    # Coach's note
    st.subheader("Coach's Note")
    st.write(analysis["feedback"]["overall"])

    st.divider()

    # Drill
    st.subheader("Your Next Drill")
    st.info(analysis["drill"])

    if st.button("Start New Session", type="primary"):
        reset()
        st.rerun()
