from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_title = soup.find('table').find('h1').text.split('::')[0].strip()
    book_author = soup.find('table').find('h1').text.split('::')[1].strip()
    all_comments = soup.find('table').find_all('div', class_='texts')
    book_comments = [comment.text.split(')')[1] for comment in all_comments]
    book_genre = soup.find_all('span', class_='d_book')[0].text.split(':')[1].strip()
    book_image_link = urljoin(response.url, soup.find(class_='bookimage').find('img')['src'])
    book_details = {'book_author': book_author,
                    'book_title': book_title,
                    'book_genre': book_genre,
                    'book_comments': book_comments,
                    'book_image_link': book_image_link}

    return book_details
