import requests


def download_txt(book_id, book_name):
    # Tuka za da najdeme ID na knigata
    page_link = f"http://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    page = requests.get(page_link).content
    book_name = book_name.strip()
    with open(f"{book_name}.txt", "wb") as file:
        file.write(page)


def download_epub(book_id, book_name, imgs):
    download_link = f"http://www.gutenberg.org/ebooks/{book_id}.epub."
    download_link += "images" if imgs else "noimages"
    raw_file = requests.get(download_link, allow_redirects=True)
    # Kaj The Oddysey na krajo ima \r i prae problemi zatoa strip
    book_name = book_name.strip()
    # Tuka treba "wb" za da e write binary inace samo string moze da upisuva
    with open(f"{book_name}.epub", "wb") as file:
        file.write(raw_file.content)
    print("Zavrsi wb")


def download_kindle(book_id, book_name, imgs):
    download_link = f"http://www.gutenberg.org/ebooks/{book_id}.kindle."
    download_link += "images" if imgs else "noimages"
    book_name = book_name.strip()
    raw_file = requests.get(download_link, allow_redirects=True)
    # Tuka treba "wb" za da e write binary inace samo string moze da upisuva
    with open(f"{book_name}.mobi", "wb") as file:
        file.write(raw_file.content)


if __name__ == "__main__":
    download_txt("1952", "1952")
