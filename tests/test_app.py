import pytest

import app as app_module
from retrieval import Article


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        app_module, "search",
        lambda q, articles, top_k=3: [Article(17, "Recht auf Löschung", "Text.", 3)],
    )
    monkeypatch.setattr(
        app_module, "ask_claude",
        lambda q, articles: "Antwort laut Artikel 17.",
    )
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_index_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ask-gdpr" in response.data.lower()


def test_ask_returns_answer_and_sources(client):
    response = client.post("/api/ask", json={"question": "Was ist das Recht auf Löschung?"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["answer"] == "Antwort laut Artikel 17."
    assert data["sources"] == [{"number": 17, "title": "Recht auf Löschung"}]


def test_ask_rejects_empty_question(client):
    response = client.post("/api/ask", json={"question": "   "})
    assert response.status_code == 400


def test_ask_rejects_too_long_question(client):
    response = client.post("/api/ask", json={"question": "x" * 501})
    assert response.status_code == 400


def test_ask_without_match_skips_api(client, monkeypatch):
    monkeypatch.setattr(app_module, "search", lambda q, articles, top_k=3: [])

    def boom(q, articles):
        raise AssertionError("API must not be called when retrieval is empty")

    monkeypatch.setattr(app_module, "ask_claude", boom)
    response = client.post("/api/ask", json={"question": "Bananenbrot Raumschiff"})
    assert response.status_code == 200
    assert "nichts gefunden" in response.get_json()["answer"]


def test_ask_handles_api_error(client, monkeypatch):
    def boom(q, articles):
        raise RuntimeError("api down")

    monkeypatch.setattr(app_module, "ask_claude", boom)
    response = client.post("/api/ask", json={"question": "Was ist Einwilligung?"})
    assert response.status_code == 502
    assert "nochmal" in response.get_json()["error"]
