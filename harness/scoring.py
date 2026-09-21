def score_exact_match(actual: str, expected: str) -> tuple[float, bool]:
    """
    Loose match: checks if the expected answer appears in the response,
    case-insensitive. Real answers often come wrapped in extra text
    (like Gemini's explanation), so literal equality is too strict.
    """
    actual_normalized = actual.lower()
    expected_normalized = expected.lower()
    passed = expected_normalized in actual_normalized
    score = 1.0 if passed else 0.0
    return score, passed
import json
from google import genai

from dotenv import load_dotenv
load_dotenv()


JUDGE_PROMPT_TEMPLATE = """You are grading an AI system's response to a task.

ORIGINAL TASK:
{prompt}

CRITERIA FOR A GOOD RESPONSE:
{expected}

THE AI'S ACTUAL RESPONSE:
{actual}

Grade the response against the criteria. Respond with ONLY a JSON object,
no other text, in exactly this format:
{{"passed": true or false, "score": 0.0 to 1.0, "reasoning": "one sentence explanation"}}
"""

def score_llm_judge(prompt: str, actual: str, expected: str, model: str = "gemini-3.6-flash") -> tuple[float, bool]:
    judge_client = genai.Client()
    judge_prompt = JUDGE_PROMPT_TEMPLATE.format(prompt=prompt, expected=expected, actual=actual)

    response = judge_client.models.generate_content(
        model=model,
        contents=judge_prompt,
    )

    raw_text = response.text.strip()
    # Judges sometimes wrap JSON in markdown fences despite instructions — strip if present
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").removeprefix("json").strip()

    try:
        verdict = json.loads(raw_text)
        return float(verdict["score"]), bool(verdict["passed"])
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  [judge parse failed: {e}] raw output: {raw_text[:200]}")
        return 0.0, False