from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "ReqLens API is running"


def test_analyze_endpoint():

    requirement = (
        "The website should be very easy to use."
    )

    response = client.post(
        "/analyze",
        json={
            "requirement": requirement
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["requirement"] == requirement

    assert data["category"] in [
        "CLEAR",
        "VAGUE",
        "MISSING_CONSTRAINT"
    ]

    assert data["severity"] in [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]

    assert "detected_issue" in data

    assert "vague_words" in data

    assert "suggestions" in data

    assert "explanation" in data

    assert "improved_requirement" in data

    assert "machine_learning" in data

    assert "prediction" in data["machine_learning"]

    assert "confidence" in data["machine_learning"]

    assert "probability_distribution" in data["machine_learning"]


def test_analyze_clear_requirement():

    response = client.post(
        "/analyze",
        json={
            "requirement":
                "The application must respond within 2 seconds."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "CLEAR"

    assert data["severity"] == "LOW"


def test_analyze_empty_requirement():

    response = client.post(
        "/analyze",
        json={
            "requirement": ""
        }
    )

    assert response.status_code == 422


def test_analyze_whitespace_requirement():

    response = client.post(
        "/analyze",
        json={
            "requirement": "   "
        }
    )

    assert response.status_code == 422


def test_analyze_batch_endpoint():

    requirements = [
        "The application must respond within 2 seconds.",
        "The website should be very easy to use.",
        "Users should be able to upload reports."
    ]

    response = client.post(
        "/analyze-batch",
        json={
            "requirements": requirements
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_requirements"] == 3

    assert len(data["results"]) == 3

    assert "potential_conflicts" in data

    for result in data["results"]:

        assert "requirement" in result

        assert "category" in result

        assert "severity" in result

        assert "detected_issue" in result

        assert "suggestions" in result

        assert "explanation" in result

        assert "improved_requirement" in result

        assert "machine_learning" in result


def test_analyze_batch_empty_list():

    response = client.post(
        "/analyze-batch",
        json={
            "requirements": []
        }
    )

    assert response.status_code == 422


def test_analyze_batch_conflict_detection():

    requirements = [
        "The application must respond within 2 seconds.",
        "The application must respond at least 5 seconds."
    ]

    response = client.post(
        "/analyze-batch",
        json={
            "requirements": requirements
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(
        data["potential_conflicts"]
    ) > 0