import streamlit as st

from coach import generate_story_prompt, analyze_story
from trainer import generate_exercise, evaluate_exercise
from database import (
    init_db,
    save_session,
    get_recent_sessions,
    get_pending_drill,
    mark_drill_complete,
    save_training_session,
    get_recent_training_sessions,
    get_coaches_pick,
    get_auto_difficulty,
)

st.set_page_config(page_title="Podium", layout="wide")
init_db()

# ── Session state ─────────────────────────────────────────────────────────────

_DEFAULTS = {
    "c_stage": "select_track",
    "c_track": "Professional",
    "c_prompt": "",
    "c_story": "",
    "c_analysis": None,
    "t_stage": "start",
    "t_dimension": None,
    "t_difficulty": None,
    "t_exercise": None,
    "t_result": None,
    "t_is_drill": False,
    "t_drill_session_id": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_coach():
    for k in ["c_stage", "c_prompt", "c_story", "c_analysis"]:
        st.session_state[k] = _DEFAULTS[k]


def reset_training():
    for k in ["t_stage", "t_dimension", "t_difficulty", "t_exercise",
               "t_result", "t_is_drill", "t_drill_session_id"]:
        st.session_state[k] = _DEFAULTS[k]


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Podium")
    st.caption("AI Storytelling Coach")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("New Coach", use_container_width=True):
            reset_coach()
            st.rerun()
    with col2:
        if st.button("New Training", use_container_width=True):
            reset_training()
            st.rerun()

    st.divider()
    st.subheader("Recent Activity")

    coach_sessions = get_recent_sessions(3)
    training_sessions = get_recent_training_sessions(3)

    if not coach_sessions and not training_sessions:
        st.caption("No sessions yet.")
    for s in coach_sessions:
        st.markdown(
            f"Coach · **{s['track']}**  \n"
            f"{s['timestamp'][:10]} · Overall: **{s['scores']['overall']}/100**"
        )
    for ts in training_sessions:
        st.markdown(
            f"Training · **{ts['dimension']}**  \n"
            f"{ts['timestamp'][:10]} · Score: **{ts['score']}/100**"
        )


# ── Tabs ──────────────────────────────────────────────────────────────────────

tab_coach, tab_training = st.tabs(["Coach", "Training"])


# ─────────────────────────────────────────────────────────────────────────────
# COACH TAB
# ─────────────────────────────────────────────────────────────────────────────

with tab_coach:

    if st.session_state.c_stage == "select_track":
        st.title("Start a Practice Session")

        track = st.radio(
            "Choose your storytelling track:",
            ["Professional", "General Narrative"],
            captions=[
                "STAR framework — workplace situations, leadership moments, career challenges",
                "Story spine — personal experiences, emotional resonance, universal themes",
            ],
        )
        st.session_state.c_track = track

        if st.button("Get Story Prompt", type="primary", use_container_width=True):
            with st.spinner("Generating your prompt..."):
                st.session_state.c_prompt = generate_story_prompt(track)
                st.session_state.c_stage = "write_story"
                st.rerun()

    elif st.session_state.c_stage == "write_story":
        st.title(f"Practice — {st.session_state.c_track} Track")
        st.info(st.session_state.c_prompt)

        story = st.text_area("Write your story:", height=320, placeholder="Begin your story here...")
        ready = len(story.strip()) >= 50

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Submit", type="primary", disabled=not ready):
                with st.spinner("Analyzing your story..."):
                    analysis = analyze_story(
                        st.session_state.c_track, st.session_state.c_prompt, story
                    )
                    save_session(st.session_state.c_track, st.session_state.c_prompt, story, analysis)
                    st.session_state.c_story = story
                    st.session_state.c_analysis = analysis
                    st.session_state.c_stage = "view_results"
                    st.rerun()
        with col2:
            if not ready:
                st.caption(f"{len(story.strip())}/50 characters minimum")

    elif st.session_state.c_stage == "view_results":
        analysis = st.session_state.c_analysis

        st.title("Your Feedback")
        st.metric("Overall Score", f"{analysis['scores']['overall']} / 100")
        st.divider()

        st.subheader("Dimension Scores")
        cols = st.columns(4)
        for col, dim in zip(cols, ["structure", "language", "pacing", "emotion"]):
            with col:
                st.metric(dim.capitalize(), f"{analysis['scores'][dim]} / 100")
        st.divider()

        st.subheader("Strengths")
        for strength in analysis["strengths"]:
            st.markdown(f"- {strength}")
        st.divider()

        st.subheader("Dimension Feedback")
        for dim in ["structure", "language", "pacing", "emotion"]:
            with st.expander(dim.capitalize()):
                st.write(analysis["feedback"][dim])
        st.divider()

        st.subheader("Coach's Note")
        st.write(analysis["feedback"]["overall"])
        st.divider()

        st.subheader("Your Next Drill")
        st.info(analysis["drill"])
        st.caption("Head to the Training tab when you're ready to complete this drill.")

        if st.button("Start New Session", type="primary"):
            reset_coach()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TRAINING TAB
# ─────────────────────────────────────────────────────────────────────────────

with tab_training:

    # ── Check for pending drill ───────────────────────────────────────────────

    if st.session_state.t_stage == "start":
        pending = get_pending_drill()

        if pending:
            st.title("Before You Train...")
            st.markdown("Your last coaching session gave you this drill:")
            st.info(pending["drill"])
            st.caption(f"Dimension: **{pending['drill_dimension']}**")
            st.markdown("Did you complete it?")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Yes, I did it", type="primary", use_container_width=True):
                    mark_drill_complete(pending["id"])
                    st.session_state.t_stage = "select_dimension"
                    st.rerun()
            with col2:
                if st.button("Do it now", use_container_width=True):
                    st.session_state.t_is_drill = True
                    st.session_state.t_drill_session_id = pending["id"]
                    st.session_state.t_dimension = pending["drill_dimension"]
                    st.session_state.t_difficulty = get_auto_difficulty(pending["drill_dimension"])
                    st.session_state.t_exercise = {
                        "instruction": pending["drill"],
                        "source_material": "",
                        "tip": f"This is your assigned drill. Focus on the {pending['drill_dimension'].lower()} dimension.",
                    }
                    st.session_state.t_stage = "doing_exercise"
                    st.rerun()
            with col3:
                if st.button("Skip for now", use_container_width=True):
                    st.session_state.t_stage = "select_dimension"
                    st.rerun()
        else:
            st.session_state.t_stage = "select_dimension"
            st.rerun()

    # ── Select dimension ──────────────────────────────────────────────────────

    elif st.session_state.t_stage == "select_dimension":
        st.title("Training Session")

        st.subheader("What would you like to train?")
        dimension = st.radio(
            "Dimension:",
            ["Structure", "Language", "Pacing", "Emotion", "Coach's Pick"],
            horizontal=True,
            captions=[
                "Hook, conflict, resolution",
                "Specificity, vividness",
                "Rhythm, sentence variety",
                "Stakes, vulnerability",
                "Auto-selects your weakest",
            ],
        )

        st.subheader("Difficulty")
        difficulty = st.radio(
            "Level:",
            ["Beginner", "Intermediate", "Advanced", "Auto"],
            horizontal=True,
        )

        if st.button("Get Exercise", type="primary", use_container_width=True):
            resolved_dim = get_coaches_pick() if dimension == "Coach's Pick" else dimension
            resolved_diff = get_auto_difficulty(resolved_dim) if difficulty == "Auto" else difficulty
            with st.spinner(f"Generating {resolved_diff} {resolved_dim} exercise..."):
                exercise = generate_exercise(resolved_dim, resolved_diff)
                st.session_state.t_dimension = resolved_dim
                st.session_state.t_difficulty = resolved_diff
                st.session_state.t_exercise = exercise
                st.session_state.t_stage = "doing_exercise"
                st.rerun()

    # ── Exercise ──────────────────────────────────────────────────────────────

    elif st.session_state.t_stage == "doing_exercise":
        ex = st.session_state.t_exercise
        dim = st.session_state.t_dimension
        diff = st.session_state.t_difficulty

        st.title(f"{dim} Training — {diff}")
        st.subheader("Exercise")
        st.write(ex["instruction"])

        if ex.get("source_material"):
            st.markdown("**Work with this:**")
            st.markdown(f"> {ex['source_material']}")

        if ex.get("tip"):
            st.caption(f"Tip: {ex['tip']}")

        response = st.text_area("Your response:", height=200, placeholder="Write your response here...")
        ready = len(response.strip()) >= 20

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Submit", type="primary", disabled=not ready, key="t_submit"):
                with st.spinner("Evaluating..."):
                    result = evaluate_exercise(
                        dim,
                        ex["instruction"],
                        ex.get("source_material", ""),
                        response,
                    )
                    save_training_session(
                        dim, diff,
                        ex["instruction"], ex.get("source_material", ""),
                        response, result,
                    )
                    if st.session_state.t_is_drill and st.session_state.t_drill_session_id:
                        mark_drill_complete(st.session_state.t_drill_session_id)
                        st.session_state.t_is_drill = False
                    st.session_state.t_result = result
                    st.session_state.t_stage = "view_result"
                    st.rerun()
        with col2:
            if not ready:
                st.caption(f"{len(response.strip())}/20 characters minimum")

    # ── Result ────────────────────────────────────────────────────────────────

    elif st.session_state.t_stage == "view_result":
        result = st.session_state.t_result
        dim = st.session_state.t_dimension
        diff = st.session_state.t_difficulty

        st.title(f"{dim} Exercise Result")
        st.metric(f"{dim} Score", f"{result['score']} / 100")
        st.divider()

        st.subheader("What worked")
        st.success(result["what_worked"])

        st.subheader("Feedback")
        st.write(result["feedback"])

        st.subheader("Try instead")
        st.info(result["try_instead"])

        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Try Again", use_container_width=True):
                st.session_state.t_result = None
                st.session_state.t_stage = "doing_exercise"
                st.rerun()
        with col2:
            if st.button("New Exercise", use_container_width=True):
                with st.spinner("Generating new exercise..."):
                    new_ex = generate_exercise(dim, diff)
                    st.session_state.t_exercise = new_ex
                    st.session_state.t_result = None
                    st.session_state.t_stage = "doing_exercise"
                    st.rerun()
        with col3:
            if st.button("Change Dimension", use_container_width=True):
                reset_training()
                st.session_state.t_stage = "select_dimension"
                st.rerun()
