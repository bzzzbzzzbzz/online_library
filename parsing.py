import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_name = soup.find('table').find('h1').text.split('::')[0].strip()
    author = soup.find('table').find('h1').text.split('::')[1].strip()
    parse_comments = soup.find('table').find_all('div', class_='texts')
    comments = [comment.text.split(')')[1] for comment in parse_comments]
    genre = soup.find_all('span', class_='d_book')[0].text.split(':')[1].strip()
    image_link = urljoin(url, soup.find(class_='bookimage').find('img')['src'])
    book = {'Автор': author,
            'Название': book_name,
            'Жанр': genre,
            'Комментарии': comments,
            'Картинка': image_link}

    return book
