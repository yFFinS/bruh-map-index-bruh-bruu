import os

import pygame as pg
import requests

from interface import Label, Button, TextField


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


def start_screen(screen):
    global running

    add_label((70, 200), text="Введите начальные координаты/адрес", font_size=60, text_color=(100, 255, 100),
              borders_color=(100, 100, 100), borders_width=10)
    add_textfield((70, 300), (860, 50), init_text="если текст не влез в рамку я не виновата",
                  borders_color=(100, 255, 100), borders_width=2, font_size=20, action=load_map)
    running = True

    pg.display.flip()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                pass
            interface.update(event)

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
    return str(arg).replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')\
        .replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')


def make_map(point, spn, size, filename):
    print('Point ll: ', point)
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


def load_map(request):
    try:
        point = make_point(request)

        make_map(point, spn, map_size, filename)
    except IndexError:
        print('Wrong point')
        exit(-1)

    terminate()


def terminate():
    global running
    running = False


def main():
    global interface, spn, map_size, filename, map_api_server, geocoder_api_server, apikey

    pg.init()

    map_size = (600, 450)
    spn = (0.01, 0.01)
    filename = "map.png"
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"

    interface = pg.sprite.Group()
    size = 1000, 800
    screen = pg.display.set_mode(size)
    start_screen(screen)

    pg.quit()
    exit_dialog()


def exit_dialog():
    if input('Write S to save map file: ') not in {'s', 'S'}:
        os.remove(filename)
        print('File deleted')
    else:
        print('File saved')


if __name__ == '__main__':
    main()
