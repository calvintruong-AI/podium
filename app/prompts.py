SYSTEM_PROMPT = """You are Podium, an expert public speaking and storytelling coach. You combine the narrative instincts of a seasoned author with the precision of a professional speech coach. Your feedback is direct, specific, and actionable — never vague. Every note points to something the speaker can change in their next attempt."""

_TRACK_CONTEXT = {
    "Professional": {
        "description": "workplace situations, leadership moments, career challenges, or professional achievements",
        "framework": "STAR (Situation → Task → Action → Result)",
        "note": "The story should have a clear professional takeaway or lesson.",
    },
    "General Narrative": {
        "description": "personal, universal human experiences — moments of failure, unexpected kindness, decisions that changed direction, or formative memories",
        "framework": "Story Spine (And... But... Therefore...)",
        "note": "The story should connect to something the audience universally recognizes.",
    },
}


def build_prompt_request(track: str) -> str:
    ctx = _TRACK_CONTEXT[track]
    return (
        f"Generate a story prompt for a {track} storytelling practice session.\n\n"
        f"The prompt should invite stories about: {ctx['description']}.\n"
        f"Guiding framework: {ctx['framework']}.\n"
        f"{ctx['note']}\n\n"
        "Return only the prompt itself — 2 to 3 sentences maximum. No preamble, no labels."
    )


def build_analysis_request(track: str, prompt: str, story: str) -> str:
    return f"""Analyze this story submission from a {track} storytelling practice session.

PROMPT GIVEN: {prompt}

STORY SUBMITTED:
{story}

Score the story across 5 dimensions (0-100) and provide specific, actionable feedback.

Return valid JSON only, with this exact structure:
{{
  "scores": {{
    "structure": <integer 0-100>,
    "language": <integer 0-100>,
    "pacing": <integer 0-100>,
    "emotion": <integer 0-100>,
    "overall": <integer 0-100>
  }},
  "feedback": {{
    "structure": "<2-3 sentences of specific feedback>",
    "language": "<2-3 sentences of specific feedback>",
    "pacing": "<2-3 sentences of specific feedback>",
    "emotion": "<2-3 sentences of specific feedback>",
    "overall": "<3-4 sentence overall coaching note>"
  }},
  "strengths": ["<strength 1>", "<strength 2>"],
  "drill": "<one specific, actionable practice drill targeting the weakest dimension>"
}}"""
