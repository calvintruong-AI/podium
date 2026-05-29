import json
import os

import anthropic
from dotenv import load_dotenv

from training_prompts import build_exercise_request, build_evaluation_request

load_dotenv()

_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
_MODEL = "claude-sonnet-4-6"
_SYSTEM = "You are Podium, an expert storytelling coach. Be specific, direct, and actionable."


def _parse_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])


def generate_exercise(dimension: str, difficulty: str) -> dict:
    response = _client.messages.create(
        model=_MODEL,
        max_tokens=512,
        system=_SYSTEM,
        messages=[{"role": "user", "content": build_exercise_request(dimension, difficulty)}],
    )
    return _parse_json(response.content[0].text)


def evaluate_exercise(
    dimension: str, instruction: str, source_material: str, response: str
) -> dict:
    result = _client.messages.create(
        model=_MODEL,
        max_tokens=512,
        system=_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": build_evaluation_request(dimension, instruction, source_material, response),
            }
        ],
    )
    return _parse_json(result.content[0].text)
