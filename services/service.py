from scraper import fetch_wikipedia_page, extract_links
from text_processing import clean_text


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
