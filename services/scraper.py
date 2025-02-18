import requests
from bs4 import BeautifulSoup


WIKI_API_URL = "https://en.wikipedia.org/wiki/"


def fetch_wikipedia_page(article):
    try:
        response = requests.get(WIKI_API_URL + article)
        article_soup = BeautifulSoup(response.text, "html.parser")
        return article_soup
    except requests.RequestException:
        return None


def extract_links(article_soup):
    links = set()
    for a in article_soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/wiki/") and not (":" in href):
            links.add(href.split("/")[-1])
    return list(links)
