import json
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_articles(count_articles, search_query):
    try:

        dictionary = {}
        id = 0
        current_page = 1

        while id < count_articles:


            URL = f'https://habr.com/ru/search/page{current_page}/?q={search_query}'
            try:
                html = urlopen(URL)
            except HTTPError as e:
                return e

            bsObj = BeautifulSoup(html.read(), 'html.parser')
            articles = bsObj.find_all('div', {'class': 'tm-article-snippet'})
            current_page += 1

            for i in range(len(articles)):
                article = articles[i]
                id += 1
                dictionary[id] = {}

                title = article.find('h2', {'class': 'tm-article-snippet__title tm-article-snippet__title_h2'}).text
                author = article.find('a', {'class': 'tm-user-info__username'}).text
                link = article.find('a', {'class': 'tm-article-snippet__title-link'}).get('href')

                dictionary[id]["title"] = title
                dictionary[id]["author"] = author[7:][:-5]
                dictionary[id]["link"] = 'https://habr.com' + link

                if id == count_articles:
                    with open("result.json", "w", encoding='utf-8') as write_file:
                        json.dump(dictionary, write_file, ensure_ascii=False)
                    return json.dumps(dictionary, indent=4, ensure_ascii=False)

    except AttributeError as e:
        return e


if __name__ == "__main__":

    # количество статей
    count_articles = 30
    # поисковый запрос (тематика)
    search_query = 'react'
    articles = get_articles(count_articles, search_query)
    if articles:
        print(articles)

