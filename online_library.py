import argparse
import os
import time
from urllib.parse import urlsplit

import requests
from pathvalidate import sanitize_filename

from parsing import parse_book_page


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError('Redirect detected')


def download_txt(book_num, filename, folder='books/'):
    os.makedirs('books', exist_ok=True)
    url = 'https://tululu.org/txt.php'
    payload = {'id': book_num}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    valid_filename = f'{sanitize_filename(filename)}.txt'
    valid_path = os.path.join(folder, valid_filename)
    with open(valid_path, 'wb') as file:
        file.write(response.content)
    return valid_path


def download_image(url, folder='images/'):
    os.makedirs('images', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    url_path = urlsplit(url).path
    filename = url_path.split('/')[2]
    valid_path = os.path.join(folder, filename)

    with open(valid_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for downloading books from tululu.org. It provide to '
                                                 'download books and their images in diapason which you will choose. '
                                                 'There are 2 options which help you to use script: `--start_id`'
                                                 'and `--end_id`'
                                                 'For example, if you want to download books from 10 to 20 you can use:'
                                                 '```python3 online_library.py --start_id 10 --end_id 20``` '
                                                 'it will download books from number 10 to 20 and their '
                                                 'images. '
                                                 'Using script without options will download first 10 books from tululu')
    parser.add_argument('--start_id', help='enter first book: ', default=1, type=int)
    parser.add_argument('--end_id', help='enter last book ', default=10, type=int)
    args = parser.parse_args()
    fail_connection = 0
    for book_number in range(int(args.start_id), int(args.end_id)+1):
        book_url = f'https://tululu.org/b{book_number}/'
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response)
            filename = book['Название']
            download_txt(book_number, filename)
            image_link = book['Картинка']
            download_image(image_link)
            print(book)
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

