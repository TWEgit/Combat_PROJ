import pygame
import vcs

# Contains most of the game logic.
# Behaviour is based on a reverse-engineering of the original game's code.

# Resolution scale.
SCALE = 2
# Defines the game mode number.
game_mode = 7
score_1 = 0
score_2 = 0

dir_table = (
        (2, 0), (2, -1), (2, -2), (1, -2),
        (0, -2), (-1, -2), (-2, -2), (-2, -1),
        (-2, 0), (-2, 1), (-2, 2), (-1, 2),
        (0, 2), (1, 2), (2, 2), (2, 1),
    )

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
        self.image = vcs.tank_gp[rot % 4]
        self.image = pygame.transform.rotate(vcs.tank_gp[rot % 4], 90*(rot//4))
        self.image = vcs.set_graphic(self.image, clr)
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*SCALE*2), int(self.size[1]*SCALE*2)))
        self.rect = self.image.get_rect()
        self.rect.topleft = posx*SCALE*2, posy*SCALE

        self.clr = clr
        self.p2 = is_p2
        self.lose = False
        self.rush_dir = 0
        self.score_timer = 0
        self.win = False
        self.win_move = False

        self.rotation = rot
        self.rot_counter = 15
        self.rot_right = False

        self.momentum= 0
        self.vel_adjust = 1
        self.mov_counter = 0
        self.velocity = 0
        self.is_mov = False
        self.missl = Missile(self.p2, self.rotation, (self.rect.topleft[0], self.rect.topleft[1]), self)
    
    def update(self, inpt):
        self._in_bounds()
        if self.lose:
            self._lose()
        else:
            self._check_collision()
            if self.win_move and self.win:
                self._move()
            elif not self.win:
                if self.p2:
                    if inpt[pygame.K_LEFT]:
                        self._rotate(False)
                    elif inpt[pygame.K_RIGHT]:
                        self._rotate(True)
                    if inpt[pygame.K_UP]:
                        self._do_move()
                    if inpt[pygame.K_RSHIFT]:
                        self._shoot()
                else:
                    if inpt[pygame.K_a]:
                        self._rotate(False)
                    elif inpt[pygame.K_d]:
                        self._rotate(True)
                    if inpt[pygame.K_w]:
                        self._do_move()
                    if inpt[pygame.K_q]:
                        self._shoot()
                if self.is_mov:
                    self._move()

    def _in_bounds(self):
        coord = self.rect.topleft
        if coord[0] <= -16*SCALE:
            self.rect.topleft = (640 - 16*SCALE, coord[1])
        elif coord[0] >= 640:
            self.rect.topleft = (0, coord[1])
        if coord[1] <= 30:
            self.rect.topleft = (coord[0], 444 - 16*SCALE)
        elif coord[1] >= 414:
            self.rect.topleft = (coord[0], 30)
        
    def _do_move(self):
        self.momentum += self.vel_adjust
        if self.momentum // 16:
            self.is_mov = True
            self.momentum = 0

    def _move(self):
        self.mov_counter += 1
        if self.mov_counter//15:
            self.is_mov = False
            self.mov_counter = 0
        self.velocity += self.vel_adjust
        if self.velocity // 8:
            npos = self.rect.move([x*SCALE for x in dir_table[self.rotation]])
            self.rect = npos
            self.velocity = 0

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
    
    def _check_collision(self):
        if pygame.sprite.collide_mask(self, playfield):
            npos = self.rect.move([x*SCALE*2 for x in dir_table[(self.rotation+8)%16]])
            self.rect = npos
        if pygame.sprite.collide_mask(self, player_1 if self.p2 else player_2):
            npos = self.rect.move([x*SCALE*2 for x in dir_table[(self.rotation+8)%16]])
            self.rect = npos
    
    def _shoot(self):
        if not self.missl.alive():
            self.missl = Missile(self.p2, self.rotation, (self.rect.topleft[0], self.rect.topleft[1]), self)
            objects.add(self.missl)
    
    def _get_shot(self):
        global score_1, score_2
        if self.p2:
            score_1 += 1
            player_1.win = True
            player_1.win_move = player_1.is_mov
        else:
            score_2 += 1
            player_2.win = True
            player_2.win_move = player_2.is_mov
        self.lose = True
        self.rush_dir = self.rotation
        self.score_timer = 127
    
    def _lose(self):
        self.rotation = (self.rotation+2)%16
        img = vcs.tank_gp[self.rotation % 4]
        img = pygame.transform.rotate(vcs.tank_gp[self.rotation % 4], 90*(self.rotation//4))
        img = vcs.set_graphic(img, self.clr)
        self.image = pygame.transform.scale(img, (int(self.size[0]*SCALE*2), int(self.size[1]*SCALE*2)))

        self.score_timer -= 1
        if not self.score_timer:
            self.lose = False
            if self.p2:
                player_1.win = False
                player_1.win_move = False
            else:
                player_2.win = False
                player_2.win_move = False
        elif self.score_timer >= 124: 
            npos = self.rect.move([-x*4*SCALE for x in dir_table[self.rush_dir]])
            self.rect = npos


class Missile(pygame.sprite.Sprite):

    def __init__(self, player: bool, rot: int, pos: tuple, ply: Player):
        pygame.sprite.Sprite.__init__(self)
        self.image = vcs.set_graphic(vcs.m_pixel.copy(), 1 if player else 0)
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.size[0]*2*SCALE, self.size[1]*2*SCALE))
        self.player = ply

        self.rotation = rot
        self.rect.topleft = pos
        self.timer = 63
    
    def update(self, inpt):
        self.timer -= 1
        if not self.timer:
            self.kill()
        self._check_collision()
        self.rotation = self.player.rotation
        self._move()

    def _move(self):
        npos = self.rect.move([x*2*SCALE for x in dir_table[self.rotation]])
        self.rect = npos
    
    def _check_collision(self):
        if pygame.sprite.collide_mask(self, playfield):
            self.kill()
        if pygame.sprite.collide_mask(self, player_1) and self.player == player_2:
            player_1._get_shot()
            player_1.missl.kill()
            self.kill()
        elif pygame.sprite.collide_mask(self, player_2) and self.player == player_1:
            player_2._get_shot()
            player_2.missl.kill()
            self.kill()

playfield = Playfield()
player_1 = Player(8, 102, 0, 0, False)
player_2 = Player(142, 102, 1, 8, True)
renderlist = [playfield, player_2, player_1]
objects = pygame.sprite.RenderPlain(renderlist)
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