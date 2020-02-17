import pygame


pygame.init()
size = 350, 100
screen = pygame.display.set_mode(size)

font = pygame.font.Font(None, 80)
text = font.render("Bruuuuuuh", 1, (100, 255, 100))
screen.blit(text, (20, 20))
pygame.display.flip()

while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()