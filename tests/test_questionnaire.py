from tests.conftest import create_test_client


client = create_test_client()


def test_questionnaire_template():
    response = client.get("/api/v1/questionnaire/template")

    assert response.status_code == 200

    data = response.json()
    assert "fields" in data
    assert isinstance(data["fields"], list)

    expected_fields = [
        "symptom_description",
        "intensity",
        "duration",
        "location",
        "additional_context"
    ]

    assert data["fields"] == expected_fields