import pygame
import vcs

# Resolution scale.
SCALE = 2
# Defines the game mode number.
game_mode = 7
score_1 = 0
score_2 = 0


class Playfield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = vcs.set_graphic(vcs.pf_modes[1], 2)
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*SCALE*8), int(self.size[1]*SCALE*8)))

        # self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 30
        
    def update(self, inpt):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, posx, posy, clr, rot, is_p2):
        pygame.sprite.Sprite.__init__(self)
        self.image = vcs.set_graphic(vcs.tank_gp[rot].copy(), 0)
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*SCALE*2), int(self.size[1]*SCALE*2)))
        self.rect = self.image.get_rect()
        self.rect.topleft = posx*SCALE*2, posy*SCALE

        self.clr = clr
        self.p2 = is_p2
        self.rotation = rot
        self.rot_counter = 15
        self.rot_right = False
    
    def update(self, inpt):
        if self.p2:
            pass
        else:
            if inpt[pygame.K_a]:
                self._rotate(False)
            elif inpt[pygame.K_d]:
                self._rotate(True)

    def _rotate(self, right):
        # In Combat, rotation is done in roughly 22.5 degree steps.
        # For this effect, a counter that gets dec'd every frame is in place.
        # Every time the direction is changed, the counter resets.
        if right != self.rot_right:
            self.rot_counter = 15
            self.rot_right = right
            return
        self.rot_counter -= 1
        if not(self.rot_counter):
            self.rotation = (self.rotation-1 if right else self.rotation+1)%16
            img = vcs.tank_gp[self.rotation % 4]
            img = pygame.transform.rotate(vcs.tank_gp[self.rotation % 4], 90*(self.rotation//4))
            img = vcs.set_graphic(img, self.clr)
            self.image = pygame.transform.scale(img, (int(self.size[0]*SCALE*2), int(self.size[1]*SCALE*2)))
            self.rot_counter = 15


        

playfield = Playfield()
player_1 = Player(8, 102, 0, 0, False)
objects = pygame.sprite.RenderPlain((player_1, playfield))
clock = pygame.time.Clock()

def update(window):
    global game_mode, score_1, score_2

    clock.tick(60)
    # UP, DOWN, LEFT, RIGHT, FIRE (P1, P2)
    inpt = pygame.key.get_pressed()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
            
    objects.update(inpt)
    vcs.update(window, objects, score_1, score_2)
    return True