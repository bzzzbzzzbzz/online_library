import requests
import os
from pathvalidate import sanitize_filename
from parsing import get_text_name, get_image_link, parse_book_page
from urllib.parse import urlsplit
import argparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError('Redirect detected')


def download_txt(url, filename, folder='books/'):
    os.makedirs('books', exist_ok=True)
    response = requests.get(url)
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
    url_path = urlsplit(url).path
    filename = url_path.split('/')[2]
    valid_path = os.path.join(folder, filename)

    with open(valid_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='enter books number')
    parser.add_argument('--start_id', help='enter first book: ', default=1)
    parser.add_argument('--end_id', help='enter last book ', default=11)
    args = parser.parse_args()
    for i in range(int(args.start_id), int(args.end_id)):
        text_url = f"https://tululu.org/txt.php?id={i}"
        book_url = f'https://tululu.org/b{i}/'
        filename = get_text_name(book_url)
        try:
            download_txt(text_url, filename)
            image_link = get_image_link(book_url)
            download_image(image_link)
            print(parse_book_page(book_url))
        except requests.HTTPError:
            continue
