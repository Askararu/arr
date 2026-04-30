import pygame
import sys
from clock import Clock

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mickey's Clock")
    clock_obj = Clock(screen)
    fps = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        clock_obj.update()
        clock_obj.draw()
        pygame.display.flip()
        fps.tick(60)

if __name__ == "__main__":
    main()
