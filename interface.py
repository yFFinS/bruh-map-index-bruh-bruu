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
        pg.draw.rect(self.image, self.borders_color, (0, 0, *size), self.borders_width)

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
        self.pressed = False

    def update(self, event):
        if event.type is MOUSEMOTION:
            self.hovered = bool(self.rect.collidepoint(event.pos))
        if event.type is MOUSEBUTTONDOWN:
            if event.button is BUTTON_LEFT:
                self.pressed = self.hovered
        if event.type is MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.pressed:
                self.on_click_event()
            self.pressed = False

    def on_click_event(self):
        self.start_action()

    def start_action(self):
        if self.action is not None:
            self.action(*self.args)


class Label(SimpleInterfaceObject):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font_size=20, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, **kwargs):
        if size == (0, 0):
            size = pg.font.Font(None, font_size).render(text, False, text_color).get_rect().size
            size = size[0] + 2 * borders_width, size[1] + 2 * borders_width
        super().__init__(pos, size, bg_color, borders_color, borders_width)
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, font_size)
        self.center_text = True
        self.prevent_unfitted_text = True
        self.rendered_text = None
        self.render_text()

    def render_text(self):
        self.render_image()
        size = self.rect.size
        line = self.font.render(self.text, True, self.text_color)
        rect = line.get_rect(center=(size[0] // 2, size[1] // 2))
        if not self.center_text:
            rect.x = 2 * self.borders_width + 1
        self.image.blit(line, rect)

    def set_text(self, text):
        if self.prevent_unfitted_text and self.font.size(text)[0] > self.rect.w - 2 * (2 * self.borders_width + 1):
            return
        self.text = text
        self.render_text()


class Button(DynamicInterfaceObject, Label):

    def __init__(self, pos=(0, 0), size=(0, 0), text='', font_size=20, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, args=(), **kwargs):
        super().__init__(pos, size,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                         action=action, args=args, text=text, font_size=font_size, text_color=text_color)


class TextField(DynamicInterfaceObject, Label):
    init_text_color = (30, 30, 30)

    def __init__(self, pos=(0, 0), size=(0, 0), init_text='', font_size=20, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), borders_color=(255, 255, 255),
                 borders_width=1, action=None, args=(), **kwargs):
        super().__init__(pos, size, text='', font_size=font_size, text_color=text_color,
                         bg_color=bg_color, borders_color=borders_color, borders_width=borders_width,
                         action=action, args=args)

        self.focused = False
        self.init_text = init_text

    def update(self, event):
        super().update(event)

        if self.focused and event.type is KEYDOWN:
            if event.key is K_BACKSPACE and self.text:
                self.set_text(self.text[:-1])
            elif event.key is K_RETURN:
                self.on_text_enter_event()
            elif KMOD_SHIFT & pg.key.get_mods():
                self.set_text(self.text + event.unicode.upper())
            else:
                self.set_text(self.text + event.unicode)
        elif not (self.focused or self.text):
            self.show_init_text()

    def show_init_text(self):
        self.text = self.init_text
        color = self.text_color
        self.text_color = TextField.init_text_color
        self.render_text()
        self.text_color = color
        self.text = ''

    def on_text_enter_event(self):
        self.args = *self.args, self.text
        self.focused = False
        self.start_action()

    def on_click_event(self):
        self.focused = True