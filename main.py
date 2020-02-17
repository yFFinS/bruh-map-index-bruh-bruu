import pygame
import requests


def start_screen(screen):
    font = pygame.font.Font(None, 60)
    text = font.render("Введите начальные координаты/адрес", 1, (100, 255, 100))
    screen.blit(text, (70, 200))
    pygame.draw.rect(screen, (100, 255, 100), (70, 300, 860, 50), 1)
    font2 = pygame.font.Font(None, 20)
    text = font2.render("если текст не влез в рамку я не виновата", 1, (100, 255, 100))
    screen.blit(text, (70, 360))
    search_text = ''
    button_text = font.render("Готово", 1, (100, 255, 100))
    screen.blit(button_text, (400, 420))
    pygame.draw.rect(screen, (100, 255, 100), (380, 400, 180, 80), 1)
    running = True
    focused = False
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                    pygame.draw.rect(screen, (0, 0, 0), (71, 301, 858, 48))
                else:
                    search_text += event.unicode
                font3 = pygame.font.Font(None, 30)
                screen.blit(font3.render(search_text, 1, (100, 255, 100)), (75, 315))
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if focused:
                    return search_text
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 380 <= x <= 560 and 400 <= y <= 480:
                    focused = True
                    button_text = font.render("Готово", 1, (255, 255, 255))
                    screen.blit(button_text, (400, 420))
                    pygame.draw.rect(screen, (255, 255, 255), (380, 400, 180, 80), 1)
                else:
                    focused = False
                    button_text = font.render("Готово", 1, (100, 255, 100))
                    screen.blit(button_text, (400, 420))
                    pygame.draw.rect(screen, (100, 255, 100), (380, 400, 180, 80), 1)
                pygame.display.flip()


def make_point(request_text):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": request_text,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Поиск координат,', response)
        exit()

    return ','.join(response.json()["response"]["GeoObjectCollection"][
                        "featureMember"][0]["GeoObject"]["Point"]["pos"].split(' '))


def make_map(point, spn, filename):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": point,
        "l": "map",
        "size": (650, 450),
        "spn": spn}

    response = requests.get(map_api_server, params=map_params)

    if not response:
        print('Создание карты,', response)
        exit()

    with open(filename, 'w') as pic:
        pic.write(response.content)


def main():
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)

    start_search_text = start_screen(screen)

    point = make_point(start_search_text)
    print(point)

    make_map(point, 0.01, 'first_map')


if __name__ == '__main__':
    main()
