import pygame as pg
from pygame.locals import *


class InterfaceObject(pg.sprite.Sprite):

    def __init__(self, pos, size, group,
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, *args):

        super().__init__(group)
        self.size = size
        self.bg_color = bg_color
        self.borders_color = borders_color
        self.borders_width = borders_width

        self.image = pg.Surface(size, 32)
        self.init_image()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.action = action
        self.args = args

        self.hovered = False
        self.pressed = False

    def init_image(self):
        coords = [(self.borders_width, self.borders_width),
                  (self.size[0] - self.borders_width, self.borders_width),
                  (self.size[0] - self.borders_width, self.size[1] - self.borders_width),
                  (self.borders_width, self.size[1] - self.borders_width)]
        for i in range(len(coords)):
            pg.draw.line(self.image, self.borders_color, coords[i - 1], coords[i], self.borders_width)

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


class Label(InterfaceObject):
    def __init__(self, pos, size, group, text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1):
        super().__init__(pos, size, group, bg_color, borders_color, borders_width)
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 20) if font is None else font
        self.rendered_text = None
        self.render_text()

    def render_text(self):
        line = self.font.render(self.text, True, self.text_color)
        rect = line.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.init_image()
        self.image.blit(line, rect)

    def update(self, event):
        pass
