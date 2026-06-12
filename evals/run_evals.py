"""Retrieval eval: is an expected article in the top-3? Prints hit-rate table."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from retrieval import load_articles, search  # noqa: E402

BASE = Path(__file__).parent


def main():
    articles = load_articles(BASE.parent / "data" / "gdpr_articles.json")
    questions = json.loads((BASE / "questions.json").read_text(encoding="utf-8"))

    hits = 0
    print(f"{'OK':<4} {'expected':<12} {'got top-3':<16} question")
    print("-" * 80)
    for item in questions:
        result = search(item["question"], articles, top_k=3)
        got = [a.number for a in result]
        hit = any(n in got for n in item["expected_articles"])
        hits += hit
        mark = "✓" if hit else "✗"
        print(f"{mark:<4} {str(item['expected_articles']):<12} {str(got):<16} {item['question'][:50]}")

    rate = hits / len(questions) * 100
    print("-" * 80)
    print(f"Hit-rate (expected article in top-3): {hits}/{len(questions)} = {rate:.0f}%")


if __name__ == "__main__":
    main()
