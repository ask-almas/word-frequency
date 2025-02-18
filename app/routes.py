from flask import request, jsonify
from services.service import get_all_words_from_traversed_wikipedia
from services.text_processing import calculate_word_frequencies, filter_word_frequencies
from utils.helpers import validate_params
from app import app


PARAM_ARTICLE = "article"
PARAM_DEPTH = "depth"
PARAM_IGNORE_LIST = "ignore_list"
PARAM_PERCENTILE = "percentile"


@app.route("/word-frequency", methods=["GET"])
def word_frequency():
    validation_error = validate_params([PARAM_ARTICLE, PARAM_DEPTH], request.args)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    article = request.args.get(PARAM_ARTICLE)
    depth = int(request.args.get(PARAM_DEPTH))
    words = get_all_words_from_traversed_wikipedia(article, depth)
    filtered_frequencies = calculate_word_frequencies(words)
    return jsonify(filtered_frequencies)


@app.route("/keywords", methods=["POST"])
def keywords():
    data = request.get_json()
    validation_error = validate_params(
        [PARAM_ARTICLE, PARAM_DEPTH, PARAM_IGNORE_LIST, PARAM_PERCENTILE], data)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    article = data.get(PARAM_ARTICLE)
    depth = int(data.get(PARAM_DEPTH))
    ignore_list = set(data.get(PARAM_IGNORE_LIST))
    percentile = int(data.get(PARAM_PERCENTILE))

    words = get_all_words_from_traversed_wikipedia(article, depth)
    word_frequencies = calculate_word_frequencies(words)
    filtered_word_frequencies = filter_word_frequencies(word_frequencies, ignore_list, percentile)

    return jsonify(filtered_word_frequencies)
