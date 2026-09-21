import json
import os
from dotenv import load_dotenv
from google import genai
from .models import TestCase

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_test_cases(path: str) -> list[TestCase]:
    with open(path, "r") as f:
        raw = json.load(f)
    return [TestCase(**item) for item in raw]

def run_prompt(prompt: str, model: str = "gemini-3.6-flash") -> str:
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text

def run_suite(test_cases: list[TestCase]) -> list[dict]:
    outputs = []
    for tc in test_cases:
        print(f"Running {tc.id}...")
        actual = run_prompt(tc.prompt)
        outputs.append({"test_case": tc, "actual": actual})
    return outputs