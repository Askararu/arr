import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")

    ball = Ball(WIDTH // 2, HEIGHT // 2, radius=20,
                color=(220, 60, 60), step=20,
                screen_w=WIDTH, screen_h=HEIGHT)

    font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0)
                elif event.key == pygame.K_r:
                    ball.reset(WIDTH // 2, HEIGHT // 2)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Draw
        screen.fill((30, 30, 40))

        # Grid lines (subtle)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, (40, 40, 55), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, (40, 40, 55), (0, y), (WIDTH, y))

        # Border
        pygame.draw.rect(screen, (100, 100, 130), (0, 0, WIDTH, HEIGHT), 3)

        ball.draw(screen)

        # HUD
        hud = font.render(
            f"Position: ({ball.x}, {ball.y})   [Arrow Keys] Move   [R] Reset   [Q] Quit",
            True, (160, 160, 180)
        )
        screen.blit(hud, (10, HEIGHT - 28))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
