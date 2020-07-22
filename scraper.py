from bs4 import BeautifulSoup
from requests import get
from urllib.request import urlopen
from urllib.error import HTTPError

vkupno_knigi = 0


def scrape(search_text):
    base_url = 'http://www.gutenberg.org/ebooks/search/?query='
    url = base_url + search_text.replace(' ', '+')

    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    book_list = []

    book_blocks = soup.find_all('li', class_='booklink')
    for i, book_block in enumerate(book_blocks):
        book_name = book_block.find('span', class_='title')
        author = book_block.find('span', class_='subtitle')
        downloads = book_block.find('span', class_='extra')
        # [href] za da najde linko, a [8:] zatoa so privte 8 char se /ebook/ pa posle e book id
        book_id = book_block.find('a', class_='link')['href'][8:]

        # kaj cover.small.jpg moze da bide cover.medium.jpg small e 50x75 a medium e 200x300
        image_url = f"http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.small.jpg"
        try:
            # image_link - Samo za testing
            urlopen(image_url).read()
            book_name = book_name.text
            author = author.text
            downloads = downloads.text
        except AttributeError:
            continue
        except TypeError:
            continue
        except HTTPError:
            continue

        full_dict = {'book': book_name, 'author': author, 'book_id': book_id, 'downloads': downloads}
        book_list.append(full_dict)

        if i >= 9:
            # Kolku pati da naprae loop-o, kolku knigi da stae u nizata
            break

    global vkupno_knigi
    vkupno_knigi = len(book_list)
    print(f"Knigi najdeno: {vkupno_knigi}")

    return book_list


if __name__ == "__main__":
    print(scrape("tr"))
