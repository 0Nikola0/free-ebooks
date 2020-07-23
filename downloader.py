# 04.07.2020
# Mos ovoa celoto ke moze u CLass da go staam??
# samo da ne zbrka rabotite oti koa scrapero rabote u array gi stava drugite rabote
# 05. -||-
# Namesto link poarno ke e samo book ID da prate u funkc, i onam u GUI spored book id da se
import requests


# Samo za proba bese ovoa
def download_image_only(book_id):
    image_link = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.medium.jpg"
    img = requests.get(image_link)
    with open("temp.jpg", "wb") as file:
        file.write(img.content)


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
