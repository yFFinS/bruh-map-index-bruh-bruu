import pygame as pg
from interface import *
import requests


def start_screen(screen):
    font = pg.font.Font(None, 60)
    text = font.render("Введите начальные координаты/адрес", 1, (100, 255, 100))
    screen.blit(text, (70, 200))
    pg.draw.rect(screen, (100, 255, 100), (70, 300, 860, 50), 1)
    font2 = pg.font.Font(None, 20)
    text = font2.render("если текст не влез в рамку я не виновата", 1, (100, 255, 100))
    screen.blit(text, (70, 360))
    search_text = ''
    button_text = font.render("Готово", 1, (100, 255, 100))
    screen.blit(button_text, (400, 420))
    pg.draw.rect(screen, (100, 255, 100), (380, 400, 180, 80), 1)
    running = True
    focused = False
    pg.display.flip()

    g = pg.sprite.Group()
    lab = Label((20, 20), (300, 50), g, 'hello', (255, 100, 100), None, borders_color=(200, 200, 100), borders_width=3)

    while running:
        g.draw(screen)
        for event in pg.event.get():
            g.update(event)
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    search_text = search_text[:-1]
                    pg.draw.rect(screen, (0, 0, 0), (71, 301, 858, 48))
                else:
                    search_text += event.unicode
                font3 = pg.font.Font(None, 30)
                screen.blit(font3.render(search_text, 1, (100, 255, 100)), (75, 315))
                pg.display.flip()
            if event.type == pg.MOUSEBUTTONDOWN:
                if focused:
                    return search_text
            if event.type == pg.MOUSEMOTION:
                x, y = event.pos
                if 380 <= x <= 560 and 400 <= y <= 480:
                    focused = True
                    button_text = font.render("Готово", 1, (255, 255, 255))
                    screen.blit(button_text, (400, 420))
                    pg.draw.rect(screen, (255, 255, 255), (380, 400, 180, 80), 1)
                else:
                    focused = False
                    button_text = font.render("Готово", 1, (100, 255, 100))
                    screen.blit(button_text, (400, 420))
                    pg.draw.rect(screen, (100, 255, 100), (380, 400, 180, 80), 1)
                pg.display.flip()


pg.init()
size = 1000, 800
screen = pg.display.set_mode(size)

start_search_text = start_screen(screen)
print(start_search_text)