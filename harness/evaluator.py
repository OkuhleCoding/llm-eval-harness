from .runner import load_test_cases, run_suite
from .scoring import score_exact_match, score_llm_judge
from .models import EvalResult

def evaluate_suite(benchmark_path: str) -> list[EvalResult]:
    test_cases = load_test_cases(benchmark_path)
    outputs = run_suite(test_cases)

    results = []
    for o in outputs:
        tc = o["test_case"]
        actual = o["actual"]

        if tc.scoring_method == "exact_match":
            score, passed = score_exact_match(actual, tc.expected)
        elif tc.scoring_method == "llm_judge":
            score, passed = score_llm_judge(tc.prompt, actual, tc.expected)
        else:
            score, passed = 0.0, False

        results.append(EvalResult(
            test_id=tc.id,
            category=tc.category,
            prompt=tc.prompt,
            expected=tc.expected,
            actual=actual,
            score=score,
            passed=passed,
            scoring_method=tc.scoring_method,
        ))
    return results