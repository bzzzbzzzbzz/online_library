from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_name = soup.find('table').find('h1').text.split('::')[0].strip()
    author = soup.find('table').find('h1').text.split('::')[1].strip()
    all_comments = soup.find('table').find_all('div', class_='texts')
    comments = [comment.text.split(')')[1] for comment in all_comments]
    genre = soup.find_all('span', class_='d_book')[0].text.split(':')[1].strip()
    image_link = urljoin(response.url, soup.find(class_='bookimage').find('img')['src'])
    book = {'Author': author,
            'Book name': book_name,
            'Genre': genre,
            'Comments': comments,
            'Image': image_link}

    return book
