"""Builds the grounded prompt and calls the Claude API."""
import anthropic

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = (
    "Du bist ein DSGVO-Assistent. Beantworte Fragen NUR auf Basis der "
    "mitgelieferten DSGVO-Artikel. Zitiere immer die Artikel-Nummern, "
    "auf die du dich stützt (z.B. 'laut Artikel 17'). Wenn die Antwort "
    "nicht in den mitgelieferten Artikeln steht, antworte genau: "
    "'Das steht nicht in den mir vorliegenden DSGVO-Artikeln.' "
    "Erfinde nichts. Antworte auf Deutsch, kurz und verständlich, "
    "in normalem Fließtext ohne Markdown-Formatierung. "
    "Weise darauf hin, dass dies keine Rechtsberatung ist, wenn die Frage "
    "nach einer konkreten rechtlichen Einschätzung klingt."
)


def build_context(articles):
    parts = []
    for article in articles:
        parts.append(f"Artikel {article.number} — {article.title}\n{article.text}")
    return "\n\n---\n\n".join(parts)


def ask_claude(question, articles, client=None):
    if client is None:
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"DSGVO-Artikel als Kontext:\n\n{build_context(articles)}\n\n"
                f"Frage: {question}"
            ),
        }],
    )
    if not message.content:
        return "Keine Antwort erhalten, versuch's nochmal."
    return message.content[0].text
