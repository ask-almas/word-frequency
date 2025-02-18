from bs4 import BeautifulSoup
from services.scraper import extract_links
from services.text_processing import clean_text, calculate_word_frequencies, filter_word_frequencies
from utils.helpers import validate_params


def test_clean_text_valid_string():
    text = "Hello, world! Python3 is great."
    expected = ["hello", "world", "python3", "is", "great"]

    result = clean_text(text)
    assert result == expected


def test_clean_text_empty_string():
    text = ""
    expected = []

    result = clean_text(text)
    assert result == expected


def test_clean_text_special_characters():
    text = "#$$ Python!! Rocks **123!!"
    expected = ["python", "rocks", "123"]

    result = clean_text(text)
    assert result == expected


def test_calculate_word_frequencies_valid_words():
    words = ["python", "flask", "python", "api"]
    expected = {
        "python": {"count": 2, "percentage": 50.0},
        "flask": {"count": 1, "percentage": 25.0},
        "api": {"count": 1, "percentage": 25.0},
    }

    result = calculate_word_frequencies(words)
    assert result == expected


def test_calculate_word_frequencies_empty_list():
    words = []
    expected = {}

    result = calculate_word_frequencies(words)
    assert result == expected


def test_filter_word_frequencies_no_filtering():
    word_frequencies = {
        "python": {"count": 3, "percentage": 30.0},
        "flask": {"count": 1, "percentage": 10.0},
        "api": {"count": 2, "percentage": 20.0},
    }
    ignore_list = []
    min_percentage = 0

    expected = word_frequencies

    result = filter_word_frequencies(word_frequencies, ignore_list, min_percentage)
    assert result == expected


def test_filter_word_frequencies_ignore_list():
    word_frequencies = {
        "python": {"count": 3, "percentage": 30.0},
        "flask": {"count": 1, "percentage": 10.0},
        "api": {"count": 2, "percentage": 20.0},
    }
    ignore_list = ["python"]
    min_percentage = 0

    expected = {
        "flask": {"count": 1, "percentage": 10.0},
        "api": {"count": 2, "percentage": 20.0},
    }

    result = filter_word_frequencies(word_frequencies, ignore_list, min_percentage)
    assert result == expected


def test_filter_word_frequencies_min_percentage():
    word_frequencies = {
        "python": {"count": 3, "percentage": 30.0},
        "flask": {"count": 1, "percentage": 10.0},
        "api": {"count": 2, "percentage": 20.0},
    }
    ignore_list = []
    min_percentage = 15.0

    expected = {"python": {"count": 3, "percentage": 30.0}, "api": {"count": 2, "percentage": 20.0}}

    result = filter_word_frequencies(word_frequencies, ignore_list, min_percentage)
    assert result == expected


def test_extract_links_valid_html():
    html = """
    <html>
        <body>
            <a href="/wiki/Python_(programming_language)">Python</a>
            <a href="/wiki/Flask">Flask</a>
            <a href="/other/Page">Invalid</a>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    expected = ["Python_(programming_language)", "Flask"]

    result = extract_links(soup)
    assert sorted(result) == sorted(expected)


def test_extract_links_empty_html():
    html = "<html></html>"
    soup = BeautifulSoup(html, "html.parser")

    result = extract_links(soup)
    assert result == []


def test_validate_params_valid():
    required_params = ["name", "age"]
    request_args = {"name": "John", "age": "30"}

    result = validate_params(required_params, request_args)
    assert result is None


def test_validate_params_missing_params():
    required_params = ["name", "age"]
    request_args = {"name": "John"}

    result = validate_params(required_params, request_args)
    assert result[0]["error"] == "Missing required parameters: age"
    assert result[1] == 400
