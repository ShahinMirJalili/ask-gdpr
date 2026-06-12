from unittest.mock import MagicMock

from claude_client import MAX_TOKENS, MODEL, SYSTEM_PROMPT, ask_claude, build_context
from retrieval import Article


def make_articles():
    return [
        Article(17, "Recht auf Löschung", "Die betroffene Person hat das Recht auf Löschung.", 3),
        Article(6, "Rechtmäßigkeit der Verarbeitung", "Verarbeitung nur mit Einwilligung.", 2),
    ]


def test_build_context_contains_numbers_titles_texts():
    context = build_context(make_articles())
    assert "Artikel 17" in context
    assert "Recht auf Löschung" in context
    assert "Einwilligung" in context


def test_system_prompt_enforces_guardrails():
    lower = SYSTEM_PROMPT.lower()
    assert "nur" in lower            # answer ONLY from context
    assert "artikel" in lower        # cite article numbers
    assert "steht nicht" in lower    # refusal phrase


def test_ask_claude_calls_api_with_context_and_caps_tokens():
    fake_client = MagicMock()
    fake_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="Antwort laut Artikel 17.")]
    )
    answer = ask_claude("Was ist das Recht auf Löschung?", make_articles(), client=fake_client)

    assert answer == "Antwort laut Artikel 17."
    kwargs = fake_client.messages.create.call_args.kwargs
    assert kwargs["model"] == MODEL
    assert kwargs["max_tokens"] == MAX_TOKENS <= 1024
    assert kwargs["system"] == SYSTEM_PROMPT
    assert "Artikel 17" in kwargs["messages"][0]["content"]
    assert "Recht auf Löschung?" in kwargs["messages"][0]["content"]
