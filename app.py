
import pygame
import os
import io   # Za pravenje na temp file na slika od knigata
from urllib.request import urlopen
import scraper
import downloader

# x, y coords deka da se ukluce window screen od pygame
# Title bar e 30 (y), da se pojave na sred screen (x) treba da e 413, za testing podobro mi e 800, 45
windowPosition = (800, 43)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % windowPosition

pygame.init()
WHITE = (250, 250, 250)
GRAY = (30, 30, 30)
screenWidth, screenHeight = 525, 682
screen = pygame.display.set_mode((screenWidth, screenHeight))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT1 = pygame.font.SysFont(None, 32, bold=True)
FONT2 = pygame.font.SysFont('Mono', 16)
FONT3 = pygame.font.SysFont('Arial', 28)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT1.render(text, True, self.color)
        self.active = False

        self.rText = ''
        self.enter = False

    def handle_event(self, evnt):
        self.enter = False
        if evnt.type == pygame.MOUSEBUTTONDOWN:
            # Ako kliknes na input box
            # noinspection PyArgumentList
            if self.rect.collidepoint(evnt.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Menja bojata dali e aktivno ili ne (kliknano ili ne)
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if evnt.type == pygame.KEYDOWN:
            if self.active:
                if evnt.key == pygame.K_RETURN:
                    self.enter = True
                    self.rText = self.text
                    self.active = False
                    self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
                elif evnt.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += evnt.unicode
                # Pisuva go teksto pa
                self.txt_surface = FONT1.render(self.text, True, self.color)

    def update(self):
        # Zgolemuva input box ako teksto e pogolem
        width = max(350, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, scren):
        # Crta teksto
        scren.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Crta kockata
        pygame.draw.rect(scren, self.color, self.rect, 2)


class BooksGUI:
    def __init__(self, gui_id, book_id, author, titl, downlads, img_pos, title_pos):
        # Ovoa e za da znam na koja kniga e kliknal
        self.gui_id = gui_id
        self.book_title = titl
        self.book_author = author
        self.downloads = downlads
        self.book_id = book_id
        self.is_clicked = False
        self.img_url = f"http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.small.jpg"
        self.image_link = urlopen(self.img_url).read()
        # Zima ja slikata od linko i ja prae u temp file
        self.image_file = io.BytesIO(self.image_link)
        # Prae ja slikata u slika od bytes file
        self.image = pygame.image.load(self.image_file)
        # Menjame dimenzii (50x75 e obicnata)
        self.image = pygame.transform.scale(self.image, (75, 105))
        # Mesteme coords deka da se nacrta slikata
        self.image_pos = self.image.get_rect()
        self.image_pos.topleft = img_pos
        self.title = titl
        self.title_pos = title_pos

    def draw_image(self, **kwargs):
        if 'pos' in kwargs:
            screen.blit(self.image, kwargs.get('pos'))
        else:
            screen.blit(self.image, self.image_pos)

    def blit_text(self, font, color=pygame.Color('white')):
        word_height = 0
        words = [word.split(' ') for word in self.title.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        # self.title_pos[0] zatoa so e tuple (x, y) na men mi treba samo x
        max_width = self.title_pos[0] + 125
        max_height = self.title_pos[1] + 75
        x, y = self.title_pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = self.title_pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                if y > max_height:
                    # Ako e pregolem teksto da ne produzuva kaj narednata kniga prestane da go pisuva
                    break
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.title_pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def hande_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Ako kliknes na slikata na knigata
            # Tuka mora da e image_pos oti toa e rect, a slikata e surface i surface nema collide point argument
            if self.image_pos.collidepoint(ev.pos):
                self.is_clicked = True


class SelectedBook:
    def __init__(self, title, author, downlads, book_id):
        self.title = title
        self.author = f"by   {author}"
        self.downloads = downlads
        self.book_id = book_id
        self.img_url = f"http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.medium.jpg"
        # Otvara linko za slikata
        self.image_link = urlopen(self.img_url).read()
        # Zima ja slikata od linko i ja prae u temp file
        self.image_file = io.BytesIO(self.image_link)
        # Prae ja slikata u slika od bytes file
        self.image = pygame.image.load(self.image_file)
        # Menjame dimenzii (200x300 e obicnata medium)
        self.image = pygame.transform.scale(self.image, (200, 300))

    def draw_image(self, img_pos):
        screen.blit(self.image, img_pos)

    @staticmethod
    def blit_text(font, text, title_pos, max_wh, color=pygame.Color('white')):
        word_height = 0
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        # title_pos[0] zatoa so e tuple (x, y) na men mi treba samo x
        max_width = max_wh[0]
        max_height = max_wh[1]
        x, y = title_pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = title_pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                if y > max_height:
                    # Ako e pregolem teksto da ne produzuva kaj narednata kniga prestane da go pisuva
                    break
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = title_pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        return y


class DownloadButton:
    def __init__(self, font, text, pos):
        self.font = font
        self.text = font.render(text, True, COLOR_ACTIVE)
        self.text_pos = self.text.get_rect()
        self.text_pos.topleft = pos
        self.is_clicked = False

    def handle_events(self, evnt):
        if evnt.type == pygame.MOUSEBUTTONDOWN:
            # noinspection PyArgumentList
            if self.text_pos.collidepoint(evnt.pos):
                self.is_clicked = True

    def blit_text(self):
        screen.blit(self.text, self.text_pos)


def search_scene():
    global search, running, show_books
    while search:
        # Ovoa e search scene, tuka e input box i unasa ime na knigata
        screen.fill(GRAY)
        search_box.update()
        search_box.draw(screen)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                # Tuka treba som izleze od search scene da izgase celoto ama nekje taka nesto
                running = False
                search = False
            # Od klasata, proveruva dali si kliknal na s_box, enter, backspace i so tekst upisuvas
            search_box.handle_event(ev)
            if search_box.enter:
                search_book = search_box.rText
                show_books = True
                search = False
                for book_dict in scraper.scrape(search_book):
                    # Od scrapero stava rezultatite u 2 arrays
                    titles.append(book_dict["book"])
                    authors.append(book_dict["author"])
                    book_ids.append(book_dict["book_id"])
                    downloads.append(book_dict["downloads"])
    return images, titles


def create_books(img_x, img_y, title_x, title_y):
    books_arr = []
    i = 0
    base_img_pos_x = img_x
    base_title_pos_x = title_x
    while i < len(book_ids):
        try:
            # Tuka mora try zatoa so moze da se sluce da ima pomalku od 3 knigi
            for _ in range(3):
                books_arr.append(BooksGUI(i, book_ids[i], authors[i], titles[i], downloads[i], (img_x, img_y), (title_x, title_y)))
                i += 1
                # Zgolemuva x za da odat na desno
                img_x += 170
                title_x += 170
        except IndexError:
            break
        # Zgolemuvame y za da odat nadole i x go vrakjame na base za da pocne od prvoto mesto
        img_y += 205  # bese 180
        title_y += 205
        img_x = base_img_pos_x
        title_x = base_title_pos_x
    return books_arr


def draw_searched_text(text, pos):
    text = f"{str(scraper.vkupno_knigi)} Results for: {text}"
    searcher_text = FONT1.render(text, True, COLOR_ACTIVE)
    screen.blit(searcher_text, pos)


def show_boks(boks):
    global search, show_books, running
    search = False
    clicked_on_book = False
    selected_bok = 0
    while show_books:
        # Show books scene, pokazuva gi knigite na ekrano
        screen.fill(GRAY)
        for ev in pygame.event.get():
            for book in boks:   # Tuka proveruvame dali e kliknal na knigata
                book.hande_event(ev)
                if book.is_clicked:
                    selected_bok = book.gui_id
                    clicked_on_book = True
                    show_books = False
                if ev.type == pygame.QUIT:
                    # Serch na True a main_run na false za koa klikne "X" da se vrne na search scene
                    # serch = True
                    running = False
                    show_books = False
        for book in boks:
            book.draw_image()
            book.blit_text(FONT2)
        # Da pokaze kolku results najde
        draw_searched_text(search_box.rText, (30, 25))
        pygame.display.flip()
    return clicked_on_book, selected_bok


def clicked_book_scene(gui_id):
    global running
    c_b_info = [books[gui_id].book_title, books[gui_id].book_author, books[gui_id].downloads, books[gui_id].book_id]
    clicked_book = SelectedBook(c_b_info[0], c_b_info[1], c_b_info[2], c_b_info[3])

    plain_text = DownloadButton(FONT3, "Plain text", (50, 420))
    epub_imgs = DownloadButton(FONT3, "Epub with images", (50, 460))
    epub_noimgs = DownloadButton(FONT3, "Epub without images", (50, 500))
    kindle_imgs = DownloadButton(FONT3, "Kindle with images", (50, 540))
    kindle_noimgs = DownloadButton(FONT3, "Kindle without images", (50, 580))

    posl_scene = True
    while posl_scene:
        screen.fill(GRAY)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                posl_scene = False
            # Proveruva dali si kliknal na download button
            plain_text.handle_events(ev)
            epub_imgs.handle_events(ev)
            epub_noimgs.handle_events(ev)
            kindle_imgs.handle_events(ev)
            kindle_noimgs.handle_events(ev)

            if plain_text.is_clicked:

                downloader.download_txt(clicked_book.book_id, clicked_book.title)
                plain_text.is_clicked = False
            if epub_imgs.is_clicked:
                downloader.download_epub(clicked_book.book_id, clicked_book.title, True)
                epub_imgs.is_clicked = False
            if epub_noimgs.is_clicked:
                downloader.download_epub(clicked_book.book_id, clicked_book.title, False)
                epub_noimgs.is_clicked = False
            if kindle_imgs.is_clicked:
                downloader.download_kindle(clicked_book.book_id, clicked_book.title, True)
                kindle_imgs.is_clicked = False
            if kindle_noimgs.is_clicked:
                downloader.download_kindle(clicked_book.book_id, clicked_book.title, False)
                kindle_noimgs.is_clicked = False

        clicked_book.draw_image((40, 40))
        # Naslovo na knigata
        book_y = clicked_book.blit_text(FONT3, clicked_book.title, (250, 50), (515, 600))
        # Imeto na avtoro
        clicked_book.blit_text(FONT3, clicked_book.author, (250, book_y + 15), (515, 320))
        # Downloads
        clicked_book.blit_text(FONT3, clicked_book.downloads, (50, 345), (240, 350))
        # download buttons
        plain_text.blit_text()
        epub_imgs.blit_text()
        epub_noimgs.blit_text()
        kindle_imgs.blit_text()
        kindle_noimgs.blit_text()

        pygame.display.flip()


search_box = InputBox(100, 70, 700, 32)    # 700 e za dzabe zatoa so odma se smene width oti nema tekst upisano

running = True
enter = False
images = []
titles = []
authors = []
book_ids = []
downloads = []
search = True
show_books = False
img_pos_x = 55
img_pos_y = 75
title_pos_x = img_pos_x - 15
title_pos_y = img_pos_y + 115

while running:
    books = []

    # Ovoa e search_scene
    images, titles = search_scene()


    if show_books:
        # Koa klikne enter na input box, tuka praeme init na knigite od klasata so ke gi pokazuva
        books = create_books(img_pos_x, img_pos_y, title_pos_x, title_pos_y)

        # Da ne proveruva u funkc dali show_books e true ili false, ako e vekje false
        book_clicked, selected_book = show_boks(books)

        if book_clicked:
            clicked_book_scene(selected_book)

    # input("Kraj na loop")

pygame.quit()
