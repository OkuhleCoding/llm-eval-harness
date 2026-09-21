from dataclasses import dataclass

@dataclass
class TestCase:
    id: str
    category: str
    prompt: str
    expected: str
    scoring_method: str

@dataclass
class EvalResult:
    test_id: str
    category: str
    prompt: str
    expected: str
    actual: str
    score: float
    passed: bool
    scoring_method: str