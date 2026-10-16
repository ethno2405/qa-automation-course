"""Smoke tests of the course shop. They check only that the shop starts and answers.

Run them in the sut/ directory:

    uv run --with-requirements requirements.txt --with pytest --with httpx pytest tests

These tests are not an example of a complete test suite. You write the real tests in the course.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_answers_ok() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_catalog_page_loads() -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert "Catalog" in response.text


def test_openapi_document_exists() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Course Shop API"
