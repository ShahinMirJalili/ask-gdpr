import json

GERMAN_STOP_WORDS = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer", "eines",
    "einem", "einen", "und", "oder", "aber", "ist", "sind", "war", "waren",
    "wird", "werden", "wurde", "wurden", "hat", "haben", "hatte", "hatten",
    "ich", "du", "er", "sie", "es", "wir", "ihr", "mich", "mir", "sich",
    "was", "wer", "wie", "wann", "wo", "warum", "welche", "welcher", "welches",
    "kann", "muss", "darf", "soll", "will", "auch", "noch", "nur", "schon",
    "auf", "aus", "bei", "mit", "nach", "von", "vor", "zu", "zum", "zur",
    "für", "über", "unter", "gegen", "ohne", "durch", "wenn", "dass", "als",
    "nicht", "kein", "keine", "sein", "ihre", "ihren", "man", "mein", "meine",
}


class Article:
    def __init__(self, number, title, text, chapter):
        self.number = number
        self.title = title
        self.text = text
        self.chapter = chapter

    def score(self, question_words):
        article_words = set((self.title + " " + self.text).lower().split())
        treffer = 0
        for word in question_words:
            if word in article_words:
                treffer += 1
        return treffer


def load_articles(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    articles = []
    for item in data:
        articles.append(Article(item["number"], item["title"], item["text"], item["chapter"]))
    return articles


def extract_words(question):
    words = set()
    for word in question.lower().split():
        word = word.strip("?,.!:;()\"'")
        if len(word) <= 2:
            continue
        if word in GERMAN_STOP_WORDS:
            continue
        words.add(word)
    return words


def search(question, articles, top_k=3):
    question_words = extract_words(question)
    scored = []
    for article in articles:
        punkte = article.score(question_words)
        if punkte > 0:
            scored.append((punkte, article))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [article for punkte, article in scored[:top_k]]
