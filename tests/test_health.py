from tests.conftest import create_test_client


client = create_test_client()


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}