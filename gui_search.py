"""
09.Jul.2020
- Pocetok
############
10 -||-
- Stavav tie 3te funkc, da naprae slika, da ja pokaze i input box u funkc staeno
- Dzabe gi stavav nema logika nisto toa
############
11 -||-
- Trgnav trite funkc od vcera oti bea za nigde
- Staviv u main while loop 2 posebni eden za koa searcha drugio za da pokaze slikite
- Napraviv posebna funkc za search_scene
############
- Staviv show books u posebna funkc
############
14 -||-
- Staviv naslovo na knigata da produze u nareden red ako e pregolem naslovo
############
15 -||-
- Menjav fontovite
- Sega proveruva dali si kliknal na nekoja kniga
############
17 -||-
- Srediv goleminata na window
- Napraviv da pokazuva grid 3x3 knigi
- Presmetuvav rastojanieto megju niv i mestiv na teksto goleminata
- Napraviv posebna funkc za pravenjeto na knigite od klasa
"""

import pygame
import os
import io   # Za pravenje na temp file na slika od knigata
from urllib.request import urlopen
import scraper

# x, y coords deka da se ukluce window screen od pygame
# Title bar e 30 (y), da se pojave na sred screen (x) treba da e 413, za testing podobro mi e 800
windowPosition = (800, 45)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % windowPosition

pygame.init()
WHITE = (250, 250, 250)
GRAY = (30, 30, 30)
screenWidth, screenHeight = 525, 682
screen = pygame.display.set_mode((screenWidth, screenHeight))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont(None, 32, bold=True)
font2 = pygame.font.SysFont('Mono', 16)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
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
                    print(self.text)
                    self.enter = True
                    self.rText = self.text
                    self.active = False
                    self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
                elif evnt.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += evnt.unicode
                # Pisuva go teksto pa
                self.txt_surface = FONT.render(self.text, True, self.color)

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
    def __init__(self, book_id, image_link, titl, img_pos, title_pos):
        self.is_clicked = False
        self.id = book_id
        # Linko deka so e slikata (https://www...)
        self.image_link = urlopen(image_link).read()
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

    def draw_image(self, **kwargs):
        if 'pos' in kwargs:
            screen.blit(self.image, kwargs.get('pos'))
        else:
            screen.blit(self.image, self.image_pos)

    def hande_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Ako kliknes na slikata na knigata
            # Tuka mora da e image_pos oti toa e rect, a slikata e surface i surface nema collide point argument
            if self.image_pos.collidepoint(ev.pos):
                print(f"Klikna na knigata {self.title} so id {self.id}")
                self.is_clicked = True


def search_scene(serch, main_run, draw_books=False):
    while serch:
        # Ovoa e search scene, tuka e input box i unasa ime na knigata
        screen.fill(GRAY)
        search_box.update()
        search_box.draw(screen)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                # Tuka treba som izleze od search scene da izgase celoto ama nekje taka nesto
                main_run = False
                serch = False
            # Od klasata, proveruva dali si kliknal na s_box, enter, backspace i so tekst upisuvas
            search_box.handle_event(ev)
            if search_box.enter:
                search_book = search_box.rText
                draw_books = True
                serch = False
                for book_dict in scraper.scrape(search_book):
                    # Od scrapero stava rezultatite u 2 arrays
                    images.append(book_dict["image"])
                    titles.append(book_dict["book"])
    return main_run, search, draw_books, images, titles


def create_books(img_x, img_y, title_x, title_y):
    books_arr = []
    i = 0
    base_img_pos_x = img_x
    base_title_pos_x = title_x
    while i < len(images):
        try:
            # Tuka mora try zatoa so moze da se sluce da ima pomalku od 3 knigi
            for _ in range(3):
                books_arr.append(BooksGUI(i, images[i], titles[i], (img_x, img_y), (title_x, title_y)))
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
    searcher_text = FONT.render(text, True, COLOR_ACTIVE)
    screen.blit(searcher_text, pos)


def show_boks(show_buks, main_run, boks):
    clicked_on_book = False
    selected_bok = 0
    serch = False
    while show_buks:
        # Show books scene, pokazuva gi knigite na ekrano
        screen.fill(GRAY)
        for ev in pygame.event.get():
            for book in boks:   # Tuka proveruvame dali e kliknal na knigata
                book.hande_event(ev)
                if book.is_clicked:
                    selected_bok = book.id
                    clicked_on_book = True
                    show_buks = False
                if ev.type == pygame.QUIT:
                    # Serch na True a main_run na false za koa klikne "X" da se vrne na search scene
                    # serch = True
                    main_run = False
                    show_buks = False
        for book in boks:
            book.draw_image()
            book.blit_text(font2)
        # Da pokaze kolku results najde
        draw_searched_text(search_box.rText, (30, 25))
        pygame.display.flip()
    return main_run, serch, clicked_on_book, selected_bok


def clicked_book_scene(main_run, book_id):
    show_book = True
    while show_book:
        screen.fill(GRAY)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                main_run = False
                show_book = False
        books[book_id].draw_image(pos=(100, 100))
    return main_run


search_box = InputBox(100, 70, 700, 32)    # 700 e za dzabe zatoa so odma se smene width oti nema tekst upisano

running = True
enter = False
images = []
titles = []
search = True
show_books = False
img_pos_x = 55
img_pos_y = 75
title_pos_x = img_pos_x - 15
title_pos_y = img_pos_y + 115

while running:
    books = []

    # Ovoa e search_scene
    running, search, show_books, images, titles = search_scene(search, running)

    print("Posle search pred da init")

    if show_books:
        # Koa klikne enter na input box, tuka praeme init na knigite od klasata so ke gi pokazuva
        books = create_books(img_pos_x, img_pos_y, title_pos_x, title_pos_y)

        print("posle init")
        # Da ne proveruva u funkc dali show_books e true ili false, ako e vekje false
        running, search, book_clicked, selected_book = show_boks(show_books, running, books)

        if book_clicked:
            clicked_book_scene(running, selected_book)

    input("Kraj na loop")

pygame.quit()
