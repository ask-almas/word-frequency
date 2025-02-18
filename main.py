from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re


app = Flask(__name__)


WIKI_API_URL = "https://en.wikipedia.org/wiki/"
HTTP_BAD_REQUEST = 400
PARAM_ARTICLE = "article"
PARAM_DEPTH = "depth"
PARAM_IGNORE_LIST = "ignore_list"
PARAM_PERCENTILE = "percentile"
WORD_PATTERN = r"\b[\w'-]+\b"


def fetch_wikipedia_page(article):
    try:
        response = requests.get(WIKI_API_URL + article)
        article_soup = BeautifulSoup(response.text, "html.parser")
        return article_soup
    except requests.RequestException:
        return None


def clean_text(text):
    return re.findall(WORD_PATTERN, text.lower())


def calculate_word_frequencies(words):
    total_words = len(words)
    counter = Counter(words)
    word_frequencies = {word: {"count": count, "percentage": (count / total_words) * 100}
                        for word, count in counter.items()}
    return word_frequencies


def filter_word_frequencies(word_frequencies, ignore_list, min_percentage):
    filtered_word_frequencies = {
        word: freq for word, freq in word_frequencies.items()
        if word not in ignore_list and freq["percentage"] >= min_percentage
    }
    return filtered_word_frequencies


def extract_links(article_soup):
    links = set()
    for a in article_soup.find_all("a", href=True):
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
        article_soup = fetch_wikipedia_page(article)
        if not article_soup:
            continue
        text = article_soup.get_text()
        words.extend(clean_text(text))
        for link in extract_links(article_soup):
            if link not in visited:
                stack.append((link, current_depth - 1))
    return words

def validate_params(required_params, request_data, is_json=False):
    missing = [param for param in required_params if
               param not in (request_data if is_json else request.args)]
    if missing:
        return {"error": f"Missing required parameters: {', '.join(missing)}"}, HTTP_BAD_REQUEST
    return None

@app.route("/word-frequency", methods=["GET"])
def word_frequency():
    validation_error = validate_params([PARAM_ARTICLE, PARAM_DEPTH], request.args)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    article = request.args.get("article")
    depth = int(request.args.get("depth"))
    words = get_all_words_from_traversed_wikipedia(article, depth)
    filtered_frequencies = calculate_word_frequencies(words)
    return jsonify(filtered_frequencies)


@app.route("/keywords", methods=["POST"])
def keywords():
    data = request.get_json()
    validation_error = validate_params(
        [PARAM_ARTICLE, PARAM_DEPTH, PARAM_IGNORE_LIST, PARAM_PERCENTILE], data, is_json=True)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    article = data.get("article")
    depth = int(data.get("depth"))
    ignore_list = set(data.get("ignore_list"))
    percentile = int(data.get("percentile"))

    words = get_all_words_from_traversed_wikipedia(article, depth)
    word_frequencies = calculate_word_frequencies(words)
    filtered_frequencies = filter_word_frequencies(word_frequencies, ignore_list, percentile)

    return jsonify(filtered_frequencies)


if __name__ == "__main__":
    app.run(debug=True)
