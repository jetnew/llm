from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup



def website_html(url):
    scheme = urlparse(url).scheme
    assert scheme == "https" or scheme == "http", f"URL must begin with 'https' or 'http': {url}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    return requests.get(url, headers=headers).text


def website_text(url, method="beautifulsoup"):
    if method == "beautifulsoup":
        text = BeautifulSoup(website_html(url), 'html.parser').get_text()
    return text


if __name__ == "__main__":
    print(website_html("https://news.ycombinator.com/item?id=37857521"))