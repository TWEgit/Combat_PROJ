import pygame

SCALE = 2

colump = [pygame.Color(255, 255, 255) for _ in range(4)]

def set_palette(pal):
    for i,c in enumerate(pal):
        if type(c) == type(pygame.Color()):
            colump[i] = c


def update(screen):
    screen.fill(colump[3])
    pygame.display.flip()