import pygame
import vcs

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 444

active = True

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Combat")

while(active):

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            active = False
    vcs.update(window)
pygame.quit()