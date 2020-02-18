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
        self.image.fill(self.bg_color)
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
        super().__init__(pos=pos, size=size,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width, **kwargs)
        self.action = action
        self.args = args

        self.hovered = False
        self.focused = False
        self.pressed = False

    def update(self, event):
        if event.type is MOUSEMOTION:
            self.hovered = bool(self.rect.collidepoint(event.pos))
        if event.type is MOUSEBUTTONDOWN:
            if event.button is BUTTON_LEFT:
                self.pressed = self.hovered
                self.focused = self.hovered
        if event.type is MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.pressed:
                self.on_click_action()
            self.pressed = False

    def on_click_action(self):
        if self.action is not None:
            self.action(*self.args)


class Label(SimpleInterfaceObject):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, **kwargs):
        super().__init__(pos, size, bg_color, borders_color, borders_width)
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 20) if font is None else font
        self.prevent_unfitted_text = True
        self.rendered_text = None
        self.render_text()

    def render_text(self, center=False):
        self.render_image()
        size = self.rect.size
        line = self.font.render(self.text, True, self.text_color)
        rect = line.get_rect(center=(size[0] // 2, size[1] // 2))
        if not center:
            rect.x = 2 * self.borders_width + 1
        self.image.blit(line, rect)

    def set_text(self, text, center=False):
        if self.prevent_unfitted_text and self.font.size(text)[0] > self.rect.w - 2 * (2 * self.borders_width + 1):
            return
        self.text = text
        self.render_text(center)


class Button(DynamicInterfaceObject, Label):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, args=(), **kwargs):
        super().__init__(pos, size,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                         action=action, args=args, text=text, font=font, text_color=text_color)


class TextField(DynamicInterfaceObject, Label):

    def __init__(self, pos=(0, 0), size=(0, 0), init_text='', font=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, **kwargs):
        super().__init__(pos, size, text='', font=font, text_color=text_color,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                         action=None, args=())

        self.init_text = init_text

    def update(self, event):
        super().update(event)

        if self.focused and event.type is KEYDOWN:
            if event.key is K_BACKSPACE and self.text:
                self.set_text(self.text[:-1])
            elif event.key is K_RETURN:
                self.focused = False
            elif KMOD_SHIFT & pg.key.get_mods():
                self.set_text(self.text + event.unicode.upper())
            else:
                self.set_text(self.text + event.unicode)
