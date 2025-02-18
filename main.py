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
    words = re.findall(r"\b[\w'-]+\b", text.lower())
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


def get_all_words_from_traversed_wikipedia(article, depth):
    visited = set()
    stack = [(article, depth)]
    words = []
    while stack:
        current_article, current_depth = stack.pop()
        if current_depth < 0 or current_article in visited:
            continue
        visited.add(current_article)
        content_soup = fetch_wikipedia_page(article)
        text = content_soup.get_text()
        words.extend(clean_text(text))
        for link in extract_links(content_soup):
            if link not in visited:
                stack.append((link, current_depth - 1))
    return words


@app.route("/word-frequency", methods=["GET"])
def word_frequency():
    if not all(param in request.args for param in ["article", "depth"]):
        return jsonify({"error": "article, depth parameters are required"}), 400
    article = request.args.get("article")
    depth = int(request.args.get("depth"))

    words = get_all_words_from_traversed_wikipedia(article, depth)
    word_freq = calculate_word_frequencies(words)

    return jsonify(word_freq)


@app.route("/keywords", methods=["POST"])
def keywords():
    data = request.get_json()
    if not all(param in data for param in ["article", "depth", "ignore_list", "percentile"]):
        return jsonify(
            {"error": "article, depth, ignore_list, percentile parameters are required"}), 400
    article = data.get("article")
    depth = int(data.get("depth"))
    ignore_list = set(data.get("ignore_list"))
    percentile = int(data.get("percentile"))

    words = get_all_words_from_traversed_wikipedia(article, depth)
    word_freq = calculate_word_frequencies(words)
    filtered_freq = {word: freq for word, freq in word_freq.items()
                     if word not in ignore_list and freq["percentage"] >= percentile}

    return jsonify(filtered_freq)


if __name__ == "__main__":
    app.run(debug=True)
