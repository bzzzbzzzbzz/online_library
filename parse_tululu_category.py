import json
import requests

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from online_library import download_image, download_txt
from parsing import parse_book_page


def parse_books_links(pages_number):
    all_book_links = []
    for page_number in range(pages_number + 1):
        url = f'https://tululu.org/l55/{page_number}'

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        book_tables = soup.find_all('table', class_='d_book')

        for table in book_tables:
            a_tag = table.find('a', href=True)
            href = a_tag['href']
            if href.startswith('/b') and href[2].isdigit():
                full_url = urljoin(url, href)
                all_book_links.append(full_url)
    return all_book_links


if __name__ == '__main__':
    book_links = parse_books_links(10)
    for link in book_links:
        response = requests.get(link)
        response.raise_for_status()
        book_details = parse_book_page(response)
        filename = book_details['book_title']
        image_link = book_details['book_image_link']
        book_number = link.split('/')[3][1:]
        book_json = json.dumps(book_details, ensure_ascii=False)
        try:
            download_txt(book_number, filename)
            print(f'Downloaded book {filename}')
            download_image(image_link)
            print(f'Downloaded image{filename}')
            with open("books.json", "w", encoding='utf8') as my_file:
                my_file.write(book_json)
            print(book_json)
        except requests.HTTPError:
            print(f'HTTP Error. Probably, {link} is not book.')
            continue

