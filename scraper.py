import requests
import os

from string import punctuation

from bs4 import BeautifulSoup

no_pages = int(input())
article_type = input()
links = []

for page_num in range(1, no_pages + 1):
    page_dir = f'Page_{page_num}'
    os.mkdir(page_dir)
    r = requests.get('https://www.nature.com/nature/articles?sort=PubDate&year=2020',
                     params={'page': page_num})
    if r.status_code != 200:
        print(f'The URL returned {r.status_code}.')
    else:
        links.append(r.url)
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            article_links = []
            articles = soup.find_all('article')
            for article in articles:
                if article.find('span', 'c-meta__type').text == article_type:
                    article_links.append(article.find('a')['href'])

            for i in article_links:
                url = 'https://www.nature.com' + i
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                string = soup.find('h1').text
                for char in punctuation:
                    string = string.replace(char, '')
                string = string.replace(' ', '_')
                article_filename = f'{string}.txt'
                with open(os.path.join(os.getcwd(), page_dir, article_filename), 'wb') as file:
                    file.write(soup.find('div', {'class': 'c-article-body'}).text.strip()
                               .encode())
        print('Saved all articles.')






























