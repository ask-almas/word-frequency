import re
from collections import Counter

WORD_PATTERN = r"\b[\w'-]+\b"


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
