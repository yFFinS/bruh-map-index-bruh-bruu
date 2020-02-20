import os
import math

import pygame as pg
import requests

from interface import Label, Button, TextField, Image


def add_label(pos, size=(0, 0), text='', font_size=20, text_color=(255, 255, 255),
              bg_color=(0, 0, 0), borders_color=(0, 0, 0), borders_width=1):
    obj = Label(pos, size, text=text, font_size=font_size, text_color=text_color,
                bg_color=bg_color, borders_color=borders_color, borders_width=borders_width)
    interface.add(obj)
    return obj


def add_button(pos, size=(0, 0), text='', font_size=20, text_color=(255, 255, 255),
               bg_color=(0, 0, 0), borders_color=(0, 0, 0), borders_width=1,
               action=None, args=()):
    obj = Button(pos, size, text=text, font_size=font_size, text_color=text_color,
                 bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                 action=action, args=args)
    interface.add(obj)
    return obj


def add_textfield(pos, size=(0, 0), init_text='', font_size=20, text_color=(255, 255, 255),
                  bg_color=(0, 0, 0), borders_color=(0, 0, 0), borders_width=1,
                  action=None, args=()):
    obj = TextField(pos, size, init_text=init_text, font_size=font_size, text_color=text_color,
                    bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                    action=action, args=args)
    interface.add(obj)
    return obj


def add_image(pos, size=(0, 0), bg_color=(0, 0, 0), borders_color=(0, 0, 0), borders_width=1):
    obj = Image(pos, size=size, bg_color=bg_color, borders_color=borders_color, borders_width=borders_width)
    interface.add(obj)
    return obj


def start_screen(screen):
    global running, map_image

    add_label((70, 10), text="Введите начальные координаты/адрес", font_size=60, text_color=(100, 255, 100),
              borders_color=(100, 255, 100), borders_width=5)
    add_textfield((70, 80), (860, 50), init_text="если текст не влез в рамку я не виновата",
                  borders_color=(100, 255, 100), borders_width=2, font_size=30, action=load_map)

    map_image = add_image((180, 160), (map_size[0] * 3, map_size[1] * 3), borders_width=1, borders_color=(100, 255, 100))
    running = True

    pg.display.flip()

    while running:
        handle_events()
        handle_keys()
        interface.draw(screen)
        pg.display.flip()


def make_point(request_text):
    geocoder_params = {
        "apikey": apikey,
        "geocode": request_text,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Поиск координат,', response)
        exit(-1)
    return response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()


def to_param(arg):
    return str(arg).replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '') \
        .replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')


def make_map(point, spn, size, filename):
    map_params = {
        "ll": to_param(point),
        "l": "map",
        "size": to_param(size),
        "spn": to_param(spn)}
    response = requests.get(map_api_server, params=map_params)

    if not response:
        print('Создание карты,', response)
        exit(-1)

    with open(filename, 'wb') as pic:
        pic.write(response.content)

    map_image.set_image_from_file(filename)


def load_map(request):
    global point
    try:
        point = make_point(request)
        print('Point ll: ', point)
        make_map(point, spn, map_size, filename)
    except IndexError:
        print('Wrong point')
        exit(-1)


def terminate():
    global running
    running = False


def main():
    start_screen(screen)

    pg.quit()
    exit_dialog()


def exit_dialog():
    try:
        os.remove(filename)
        print('File deleted')
    except FileNotFoundError:
        print('File not found')


def handle_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            terminate()
        if event.type == pg.KEYDOWN:
            keys.add(event.key)
        if event.type == pg.KEYUP and event.key in keys:
            keys.remove(event.key)
        interface.update(event)


def handle_keys():
    if pg.K_PAGEUP in keys:
        zoom(0.5)
        keys.remove(pg.K_PAGEUP)
    if pg.K_PAGEDOWN in keys:
        zoom(2)
        keys.remove(pg.K_PAGEDOWN)
    if pg.K_UP in keys:
        translate(0, -1)
        keys.remove(pg.K_UP)
    if pg.K_DOWN in keys:
        translate(0, 1)
        keys.remove(pg.K_DOWN)
    if pg.K_LEFT in keys:
        translate(-1, 0)
        keys.remove(pg.K_LEFT)
    if pg.K_RIGHT in keys:
        translate(1, 0)
        keys.remove(pg.K_RIGHT)


def zoom(zoom_factor):
    global spn
    a = min(10.24, max(0.000625, spn[0] * zoom_factor))
    b = min(10.24, max(0.000625, spn[1] * zoom_factor))
    spn = a, b
    if point is not None:
        make_map(point, spn, map_size, filename)


def translate(dx, dy):
    global point
    point[0] = str(float(point[0]) + 2 * dx * spn[0] * 2)
    point[1] = str(float(point[1]) - 2 * dy * spn[1])
    print(point)
    map_image.translate(dx, dy)
    make_map(point, spn, map_size, filename)


pg.init()
interface = pg.sprite.Group()
size = 1650, 1280
screen = pg.display.set_mode(size)
pg.display.set_caption('app 2 h4ck 1dex ly7')
keys = set()

map_size = (300, 300)
spn = (1, 1)
filename = "map.png"
map_api_server = "https://static-maps.yandex.ru/1.x/"
geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
point = None


if __name__ == '__main__':
    main()
