KEYWORDS = ['python', 'API']
URL_BASE = 'https://habr.com'
URL = '/ru/all/'
HEADERS = {'Accept': '*/*',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
           'Accept-Language': 'en-US;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1'}

import requests
from bs4 import BeautifulSoup
import re


if __name__ == "__main__":
    res = requests.get(URL_BASE + URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    posts = soup.find_all('article', class_='tm-articles-list__item')
    pattern = '[\w]+'
    for post in posts:
        href = post.find('a', class_='tm-article-snippet__title-link').attrs["href"]
        res2 = requests.get(URL_BASE + href, headers=HEADERS)
        soup2 = BeautifulSoup(res2.text, 'html.parser')
        texts = soup2.find('div', class_='article-formatted-body').text
        result = re.findall(pattern, texts, re.U)
        set_KEY = set(KEYWORDS)
        set_TEXT = set(result)

        if not set_TEXT.isdisjoint(set_KEY):
            date = post.find('span', class_='tm-article-snippet__datetime-published').find('time').attrs["datetime"]
            title = post.find('h2', class_='tm-article-snippet__title').text
            href = post.find('a', class_='tm-article-snippet__title-link').attrs["href"]
            href = URL_BASE + href
            print(f"{date[0:10]} - {title} - {href}")

