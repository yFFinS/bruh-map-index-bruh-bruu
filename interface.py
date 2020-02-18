import pygame as pg
from pygame.locals import *


class SimpleInterfaceObject(pg.sprite.Sprite):

    def __init__(self, pos=(0, 0), size=(0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255), borders_width=1, **kwargs):
        super().__init__()
        self.bg_color = bg_color
        self.borders_color = borders_color
        self.borders_width = borders_width

        self.image = pg.Surface(size, 32)

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.render_image()

    def move(self, pos, is_center=False):
        if is_center:
            self.rect.center = pos
        else:
            self.rect.topleft = pos

    def render_image(self):
        size = self.rect.size
        coords = [(self.borders_width, self.borders_width),
                  (size[0] - self.borders_width, self.borders_width),
                  (size[0] - self.borders_width, size[1] - self.borders_width),
                  (self.borders_width, size[1] - self.borders_width)]
        for i in range(len(coords)):
            pg.draw.line(self.image, self.borders_color, coords[i - 1], coords[i], self.borders_width)

    def resize(self, size):
        self.rect.size = size
        self.render_image()


class DynamicInterfaceObject(SimpleInterfaceObject):
    def __init__(self, pos=(0, 0), size=(0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, args=(), **kwargs):
        super().__init__(pos, size, bg_color, borders_color, borders_width, **kwargs)
        self.action = action
        self.args = args

        self.hovered = False
        self.pressed = False

    def update(self, event):
        if event.type is MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type is MOUSEBUTTONDOWN:
            if event.button is BUTTON_LEFT:
                self.pressed = self.hovered
        if event.type is MOUSEBUTTONUP:
            if self.pressed:
                self.on_click_action()

    def on_click_action(self):
        if self.action is not None:
            self.action(*self.args)


class Label(SimpleInterfaceObject):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, **kwargs):
        super().__init__(pos, size, bg_color, borders_color, borders_width, **kwargs)
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 20) if font is None else font
        self.rendered_text = None
        self.render_text()

    def render_text(self):
        size = self.rect.size
        line = self.font.render(self.text, True, self.text_color)
        rect = line.get_rect(center=(size[0] // 2, size[1] // 2))
        self.render_image()
        self.image.blit(line, rect)

    def set_text(self, text):
        self.text = text
        self.render_text()


class Button(Label, DynamicInterfaceObject):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, args=(), **kwargs):
        super().__init__(pos, size, text=text, font=font, text_color=text_color,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                         action=action, args=args)

