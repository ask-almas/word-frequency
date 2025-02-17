from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = Flask(__name__)
WIKI_API_URL = "https://en.wikipedia.org/api/rest_v1/page/html/"

def get_wikipedia_content(article):
    try:
        response = requests.get(WIKI_API_URL + article)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except requests.RequestException:
        return ""

def clean_text(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower())  # Match words of any length
    return words

def calculate_word_frequencies(words):
    total_words = len(words)
    counter = Counter(words)
    frequency = {word: {"count": count, "percentage": (count / total_words) * 100}
                 for word, count in counter.items()}
    return frequency

@app.route("/word-frequency", methods=["GET"])
def word_frequency():
    if "article" not in request.args or "depth" not in request.args:
        return jsonify({"error": "Article and depth parameters are required"}), 400
    article = request.args.get("article")
    depth = int(request.args.get("depth", 1))
    text = get_wikipedia_content(article)
    words = clean_text(text)
    word_freq = calculate_word_frequencies(words)
    return jsonify(word_freq)

if __name__ == "__main__":
    app.run(debug=True)
