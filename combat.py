import pygame
import vcs

# Resolution scale.
SCALE = 2
# Defines the game mode number.
game_mode = 0
score_1 = 0
score_2 = 0

class Playfield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = vcs.pf_modes[0]
        pal = pygame.Surface(self.image.get_size())
        pal.fill(vcs.colump[2])
        self.image.blit(pal, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*SCALE*8), int(self.size[1]*SCALE*8)))

        # self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 30
        
    def update(self):
        pass


playfield = Playfield()
objects = pygame.sprite.RenderPlain((playfield))
clock = pygame.time.Clock()

def update(window):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
    objects.update()
    vcs.update(window, objects, score_1, score_2)
    return True