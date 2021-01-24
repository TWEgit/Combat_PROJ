import pygame
import combat
import vcs

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 444

def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Combat")

    active = True

    while(active):
        active = combat.update(window)
        
    pygame.quit()

if __name__ == "__main__":
    main()