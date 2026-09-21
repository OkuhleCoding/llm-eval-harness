from harness.scoring import score_exact_match

def test_exact_match_passes_when_expected_present():
    score, passed = score_exact_match("The answer is 9.", "9")
    assert passed is True
    assert score == 1.0

def test_exact_match_fails_when_expected_absent():
    score, passed = score_exact_match("The answer is 10.", "9")
    assert passed is False
    assert score == 0.0

def test_exact_match_is_case_insensitive():
    score, passed = score_exact_match("The Answer Is FIVE MINUTES.", "five minutes")
    assert passed is True

def test_exact_match_known_limitation_substring_collision():
    """
    Documents a known blind spot: '9' is found inside '19', so a wrong
    numeric answer can score as a false positive. This test exists to
    make the limitation explicit and trackable, not to pretend it's fixed.
    """
    score, passed = score_exact_match("The farmer had 19 sheep.", "9")
    assert passed is True  # known false positive, tracked intentionally