import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_text_name(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    text_name = soup.find('table').find('h1').text.split('::')[0]
    return text_name


def get_image_link(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    image_link = soup.find(class_='bookimage').find('img')['src']
    valid_link = urljoin('https://tululu.org/', image_link)
    return valid_link


def parse_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_name = soup.find('table').find('h1').text.split('::')[0].strip()
    author = soup.find('table').find('h1').text.split('::')[1].strip()
    parse_comments = soup.find('table').find_all('div', class_='texts')
    comments = []
    for comment in parse_comments:
        comments.append(comment.text.split(')')[1])
    genre = soup.find_all('span', class_='d_book')[0].text.split(':')
    book_information = {'Автор: ': author,
                        'Название: ': book_name,
                        'Жанр: ': genre[1].strip(),
                        'Комментарии: ': comments}

    return book_information
