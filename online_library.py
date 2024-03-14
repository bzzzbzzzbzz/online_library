import time

import requests
import os
from pathvalidate import sanitize_filename
from parsing import parse_book_page
from urllib.parse import urlsplit
import argparse


def check_for_redirect(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError('Redirect detected')


def download_txt(book_num, filename, folder='books/'):
    os.makedirs('books', exist_ok=True)
    url = 'https://tululu.org/txt.php'
    payload = {'id': book_num}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    valid_filename = f'{sanitize_filename(filename)}.txt'
    valid_path = os.path.join(folder, valid_filename)
    with open(valid_path, 'wb') as file:
        file.write(response.content)
    return valid_path


def download_image(url, folder='images/'):
    os.makedirs('images', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    url_path = urlsplit(url).path
    filename = url_path.split('/')[2]
    valid_path = os.path.join(folder, filename)

    with open(valid_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose diapason of books. For example if you chose start_id 10, '
                                                 'and end_id 20 '
                                                 '```python3 online_library.py --start_id 10 --end_id 20``` '
                                                 'it will download books from number 10 to 20 and their '
                                                 'images')
    parser.add_argument('--start_id', help='enter first book: ', default=1)
    parser.add_argument('--end_id', help='enter last book ', default=10)
    args = parser.parse_args()
    fail_connection = 0
    for book_number in range(int(args.start_id), int(args.end_id)+1):
        book_url = f'https://tululu.org/b{book_number}/'
        try:
            check_for_redirect(book_url)
            book_parser = parse_book_page(book_url)
            filename = book_parser['Название']
            download_txt(book_number, filename)
            image_link = book_parser['Картинка']
            download_image(image_link)
            print(book_parser)
        except requests.HTTPError:
            print(f'HTTP Error. Probably, {book_url} is not book.')
            continue
        except requests.ConnectionError:
            print('No connection')
            fail_connection += 1
            if fail_connection > 1:
                time.sleep(60)
            print('Trying to connect...')
            continue

