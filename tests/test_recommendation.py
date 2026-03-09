from unittest.mock import patch

from tests.conftest import create_test_client


client = create_test_client()


def test_recommendation_endpoint_success():
    payload = {
        "symptom_description": "I have chest pain and shortness of breath",
        "intensity": "high",
        "duration": "2 days",
        "location": "chest",
        "additional_context": "The pain increases when walking"
    }

    mocked_response = {
        "enriched_input": None,
        "recommendations": [
            {
                "specialty_name": "Cardiology",
                "similarity_score": 0.82,
                "explanation": "Cardiology may be relevant. This is not a medical diagnosis."
            },
            {
                "specialty_name": "Pulmonology",
                "similarity_score": 0.61,
                "explanation": "Pulmonology may be relevant. This is not a medical diagnosis."
            }
        ],
        "red_flags": [
            {
                "keyword": "chest pain",
                "severity": "high",
                "message": "Chest pain may require urgent medical attention."
            }
        ],
        "warning": "This result is an indicative orientation only and not a medical diagnosis."
    }

    with patch("app.api.v1.endpoints.recommendation.RecommendationService.recommend", return_value=mocked_response):
        response = client.post("/api/v1/recommendations/", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) == 2
    assert data["recommendations"][0]["specialty_name"] == "Cardiology"
    assert "warning" in data
    assert "red_flags" in data