import json
import os

import anthropic
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT, build_prompt_request, build_analysis_request

load_dotenv()

_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
_MODEL = "claude-sonnet-4-6"


def generate_story_prompt(track: str) -> str:
    response = _client.messages.create(
        model=_MODEL,
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt_request(track)}],
    )
    return response.content[0].text.strip()


def analyze_story(track: str, prompt: str, story: str) -> dict:
    response = _client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_analysis_request(track, prompt, story)}],
    )
    raw = response.content[0].text.strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])
