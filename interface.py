import pygame as pg
from pygame.locals import *


class InterfaceObject(pg.sprite.Sprite):
    def __init__(self, pos, size, image, group, action=None, *args):
        super().__init__(group)
        self.size = size
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
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
