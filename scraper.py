from bs4 import BeautifulSoup
from requests import get

vkupno_knigi = 0


def scrape(search_text):
    base_url = 'http://www.gutenberg.org/ebooks/search/?query='
    url = base_url + search_text.replace(' ', '+')

    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    k = 0
    book_list = []
    # full_dict = {}
    # json_file = open("searched_books_json.txt", "w")

    book_blocks = soup.find_all('li', class_='booklink')
    for book_block in book_blocks:
        k += 1
        # Ako nemama slika da ne prae problem, ako ima ke naprae override
        img = 'NoImage'
        x = 'http://www.gutenberg.org'

        img_elem = book_block.find('img', class_='cover-thumb')
        book_name = book_block.find('span', class_='title')
        author = book_block.find('span', class_='subtitle')
        book_link = x + book_block.find('a', class_='link')['href']

        # if (img_elem, book_name, author, book_link) is not None:
        try:
            img = x + img_elem['src']
            # Tuka go praveme u .text oti ako e NoneType ke naprae error i nema da produze nadole
            # Mos so try i except ke bese poarno nz
            book_name = book_name.text
            author = author.text
        except AttributeError:
            continue
        except TypeError:
            continue

        full_dict = {'book': book_name, 'author': author, 'image': img, 'book_link': book_link}
        book_list.append(full_dict)

        print(book_name)
        if k >= 9:
            # Kolku pati da naprae loop-o, kolku knigi da stae u nizata
            break

    global vkupno_knigi
    vkupno_knigi = len(book_list)
    print(f"Knigi najdeno: {vkupno_knigi}")

    return book_list


if __name__ == "__main__":
    print(scrape("python"))
