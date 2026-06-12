"""Flask app: chat UI + /api/ask endpoint."""
import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from claude_client import ask_claude
from retrieval import load_articles, search

load_dotenv()

MAX_QUESTION_LENGTH = 500

app = Flask(__name__)
ARTICLES = load_articles(os.path.join(os.path.dirname(__file__), "data", "gdpr_articles.json"))
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Bitte gib eine Frage ein."}), 400
    if len(question) > MAX_QUESTION_LENGTH:
        return jsonify({"error": f"Frage zu lang (max. {MAX_QUESTION_LENGTH} Zeichen)."}), 400

    top_articles = search(question, ARTICLES, top_k=3)
    if not top_articles:
        return jsonify({
            "answer": "Dazu habe ich in der DSGVO nichts gefunden.",
            "sources": [],
        })

    try:
        answer = ask_claude(question, top_articles)
    except Exception:
        logger.exception("Claude API call failed")
        return jsonify({"error": "Gerade nicht erreichbar, versuch's gleich nochmal."}), 502

    return jsonify({
        "answer": answer,
        "sources": [{"number": a.number, "title": a.title} for a in top_articles],
    })


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY fehlt. Kopiere .env.example nach .env und trag deinen Key ein.")
    app.run(debug=True)
