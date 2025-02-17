from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = Flask(__name__)
WIKI_API_URL = "https://en.wikipedia.org/wiki/"

def fetch_wikipedia_page(article):
    try:
        response = requests.get(WIKI_API_URL + article)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.RequestException:
        return None

def clean_text(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower())  # Match words of any length
    return words

def calculate_word_frequencies(words):
    total_words = len(words)
    counter = Counter(words)
    frequency = {word: {"count": count, "percentage": (count / total_words) * 100}
                 for word, count in counter.items()}
    return frequency

def extract_links(content_soup):
    links = set()
    for a in content_soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/wiki/") and not (":" in href):
            links.add(href.split("/")[-1])
    return list(links)

@app.route("/word-frequency", methods=["GET"])
def word_frequency():
    if "article" not in request.args or "depth" not in request.args:
        return jsonify({"error": "Article and depth parameters are required"}), 400
    article = request.args.get("article")
    depth = int(request.args.get("depth"))
    content_soup = fetch_wikipedia_page(article)
    if not content_soup: return jsonify({"error": "Article not found"}), 404
    text = content_soup.get_text()
    words = clean_text(text)
    word_freq = calculate_word_frequencies(words)
    links = extract_links(content_soup)
    return jsonify(word_freq)

if __name__ == "__main__":
    app.run(debug=True)
