DIMENSION_DESCRIPTIONS = {
    "Structure": "narrative structure: hook, conflict/tension, turning point, resolution, and takeaway",
    "Language": "language quality: specificity, sensory detail, active voice, vivid word choice, and conciseness",
    "Pacing": "pacing and rhythm: sentence length variety, natural flow, and density",
    "Emotion": "emotional resonance: stakes, vulnerability, universal theme connection, and emotional arc",
}

_DIFFICULTY_GUIDANCE = {
    "Beginner": "Short, clear task with a concrete sentence or scenario provided. Response should be 1-3 sentences. Forgiving standards — build confidence first.",
    "Intermediate": "More nuanced task combining 2+ elements of the dimension. Response 3-6 sentences. Clear right/wrong.",
    "Advanced": "Complex, high-standards task. Response 4-10 sentences. Expect subtlety and mastery.",
}


def build_exercise_request(dimension: str, difficulty: str) -> str:
    return f"""Generate a {difficulty} training exercise for the {dimension} dimension of storytelling.

DIMENSION covers: {DIMENSION_DESCRIPTIONS[dimension]}
DIFFICULTY guidance: {_DIFFICULTY_GUIDANCE[difficulty]}

Generate a focused, realistic exercise. Return valid JSON only:
{{
  "instruction": "<clear task — exactly what the learner should do>",
  "source_material": "<a specific sentence, paragraph, or scenario to work with — make it realistic and concrete>",
  "tip": "<one actionable coaching tip directly relevant to this dimension>"
}}"""


def build_evaluation_request(
    dimension: str, instruction: str, source_material: str, response: str
) -> str:
    return f"""Evaluate this {dimension} training exercise response.

DIMENSION being trained: {dimension}
What {dimension} covers: {DIMENSION_DESCRIPTIONS[dimension]}

EXERCISE INSTRUCTION: {instruction}
SOURCE MATERIAL: {source_material}
LEARNER'S RESPONSE: {response}

Score ONLY the {dimension} dimension (0-100). Do not penalize for weaknesses in other storytelling dimensions — focus exclusively on how well the response demonstrates {dimension} skills.

Return valid JSON only:
{{
  "score": <integer 0-100>,
  "feedback": "<2-3 sentences of specific feedback on the {dimension} dimension only>",
  "what_worked": "<one specific strength in the response>",
  "try_instead": "<one concrete alternative approach or rewritten example that would score higher>"
}}"""
