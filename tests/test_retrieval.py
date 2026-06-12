import json

import pytest

from retrieval import Article, GERMAN_STOP_WORDS, extract_words, load_articles, search


@pytest.fixture
def articles(tmp_path):
    data = [
        {"number": 6, "title": "Rechtmäßigkeit der Verarbeitung",
         "text": "Die Verarbeitung ist nur rechtmäßig wenn die betroffene Person ihre Einwilligung gegeben hat", "chapter": 2},
        {"number": 17, "title": "Recht auf Löschung",
         "text": "Die betroffene Person hat das Recht zu verlangen dass personenbezogene Daten unverzüglich gelöscht werden", "chapter": 3},
        {"number": 33, "title": "Meldung von Verletzungen des Schutzes personenbezogener Daten",
         "text": "Im Falle einer Verletzung meldet der Verantwortliche binnen 72 Stunden der Aufsichtsbehörde", "chapter": 4},
    ]
    path = tmp_path / "articles.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return load_articles(path)


def test_article_has_attributes(articles):
    art = articles[0]
    assert art.number == 6
    assert art.title == "Rechtmäßigkeit der Verarbeitung"
    assert art.chapter == 2


def test_article_score_counts_overlap(articles):
    art = articles[1]  # Löschung
    assert art.score({"löschung", "daten"}) == 2
    assert art.score({"quantencomputer"}) == 0


def test_extract_words_drops_stop_words_and_short_words():
    words = extract_words("Wie ist die Meldung an die Aufsichtsbehörde?")
    assert "meldung" in words
    assert "aufsichtsbehörde" in words
    assert "wie" not in words
    assert "die" not in words
    assert "an" not in words


def test_search_returns_best_match_first(articles):
    result = search("Muss ich eine Verletzung der Aufsichtsbehörde melden?", articles)
    assert result[0].number == 33


def test_search_excludes_zero_scores(articles):
    result = search("Quantencomputer Raumschiff Bananenbrot", articles)
    assert result == []


def test_search_respects_top_k(articles):
    result = search("Verarbeitung personenbezogener Daten der betroffenen Person", articles, top_k=2)
    assert len(result) <= 2


def test_stop_word_list_is_substantial():
    assert len(GERMAN_STOP_WORDS) >= 40


def test_search_with_empty_question_returns_nothing(articles):
    assert search("", articles) == []
