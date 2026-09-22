from app.analyzer import (
    find_vague_words,
    find_missing_constraints,
    find_missing_quantitative_info,
    find_conflicts
)

from app.reqlens import (
    analyze_requirement,
    get_prediction_details
)


# ==================================================
# TEST VAGUE WORD DETECTION
# ==================================================

def test_vague_word_detection():

    requirement = (
        "The website should be very easy to use."
    )

    vague_words = find_vague_words(
        requirement
    )

    assert "easy" in vague_words


# ==================================================
# TEST MISSING CONSTRAINT DETECTION
# ==================================================

def test_missing_upload_constraints():

    requirement = (
        "Users should be able to upload reports."
    )

    missing = find_missing_constraints(
        requirement
    )

    assert len(missing) > 0


# ==================================================
# TEST MISSING QUANTITATIVE INFORMATION
# ==================================================

def test_missing_performance_target():

    requirement = (
        "The system should provide efficient performance."
    )

    missing = find_missing_quantitative_info(
        requirement
    )

    assert len(missing) > 0


# ==================================================
# TEST CLEAR REQUIREMENT
# ==================================================

def test_clear_requirement():

    requirement = (
        "The application must respond within 2 seconds."
    )

    (
        category,
        severity,
        issue,
        vague_words,
        suggestions
    ) = analyze_requirement(
        requirement
    )

    assert category == "CLEAR"
    assert severity == "LOW"
    assert len(vague_words) == 0


# ==================================================
# TEST VAGUE REQUIREMENT
# ==================================================

def test_vague_requirement():

    requirement = (
        "The website should be very easy to use."
    )

    (
        category,
        severity,
        issue,
        vague_words,
        suggestions
    ) = analyze_requirement(
        requirement
    )

    assert category == "VAGUE"
    assert severity == "HIGH"
    assert "easy" in vague_words
    assert len(suggestions) > 0


# ==================================================
# TEST ML PREDICTION
# ==================================================

def test_ml_prediction():

    requirement = (
        "The website should be very easy to use."
    )

    (
        prediction,
        confidence,
        probabilities
    ) = get_prediction_details(
        requirement
    )

    assert prediction in [
        "CLEAR",
        "MISSING_CONSTRAINT",
        "VAGUE"
    ]

    assert 0 <= confidence <= 1

    assert "CLEAR" in probabilities
    assert "MISSING_CONSTRAINT" in probabilities
    assert "VAGUE" in probabilities


# ==================================================
# TEST RESPONSE-TIME CONFLICT
# ==================================================

def test_response_time_conflict():

    requirements = [

        "The application must respond within 2 seconds.",

        "The application must respond at least 5 seconds."
    ]

    conflicts = find_conflicts(
        requirements
    )

    assert len(conflicts) > 0


# ==================================================
# TEST CAPACITY CONFLICT
# ==================================================

def test_capacity_conflict():

    requirements = [

        "The system must support at most 1000 users.",

        "The system must support at least 2000 users."
    ]

    conflicts = find_conflicts(
        requirements
    )

    assert len(conflicts) > 0