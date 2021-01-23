import os, sys
import pygame

# Contains the scale of the window.
SCALE = 2

# Real color palette (P1, P2, PF, BK).
colump = [pygame.Color(176, 60, 60), pygame.Color(28, 32, 156), pygame.Color(236, 168, 128), pygame.Color(180, 192, 120)]

# Loads graphics at boot-up (borrowed from Pygame's tutorials)
def load_image(name):
    pathname = os.path.join("res", "gfx", name)
    print("Loaded " + pathname)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


# Playfield graphics modes.
pf_modes = [load_image(name) for name in ("pf_none.png", "pf_comp.png")]
# Score numbers.
sc_nums = [load_image("sc_"+str(name)+".png") for name in range(10)]
# Tank graphics.
tank_gp = [load_image("tank_"+str(name)+".png") for name in range(1,5)]
# The missile pixel.
m_pixel = load_image("a_single_pixel.png")


def set_palette(pal):
    for i,c in enumerate(pal):
        if type(c) == type(pygame.Color()):
            colump[i] = c

def set_graphic(img, clr):
    pal = pygame.Surface(img.get_size())
    pal.fill(colump[clr])
    img.blit(pal, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
    return img

def print_score(screen, num, sc2):
    n1 = sc_nums[num%10]
    n1 = pygame.transform.scale(n1, (n1.get_width()*8*SCALE, n1.get_height()*2*SCALE))
    pal = pygame.Surface(n1.get_size())
    pal.fill(colump[1] if sc2 else colump[0])
    n1.blit(pal, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    sc_render = pygame.Surface((8*8*SCALE, 10*SCALE))
    sc_render.fill(colump[3])
    sc_render.blit(n1,(sc_render.get_width()//2, 0))
    if num//10:
        n2 = sc_nums[(num//10)%10]
        n2 = pygame.transform.scale(n2, (n2.get_width()*8*SCALE, n2.get_height()*2*SCALE))
        n2.blit(pal, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        sc_render.blit(n2,(0,0))
    pos = ((8*4+8*20)*SCALE, 2*SCALE) if sc2 else ((8*4)*SCALE, 2*SCALE)
    screen.blit(sc_render,pos)


def update(screen, objects, sc1, sc2):
    screen.fill(colump[3])
    if sc1 != None:
        print_score(screen, sc1, False)
    if sc2 != None:
        print_score(screen, sc2, True)
    objects.draw(screen)
    pygame.display.flip()