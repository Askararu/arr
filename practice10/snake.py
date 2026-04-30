import pygame
import random
import sys

CELL = 20          
COLS = 30          
ROWS = 24          
WIDTH  = CELL * COLS   
HEIGHT = CELL * ROWS   
HUD_HEIGHT = 40        


BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = ( 50, 200,  50)
DARK_GREEN = ( 20, 130,  20)
RED        = (220,  50,  50)
GRAY       = ( 40,  40,  40)
GOLD       = (255, 215,   0)
BG_COLOR   = ( 15,  15,  15)


BASE_FPS       = 8
FPS_PER_LEVEL  = 2


FOODS_PER_LEVEL = 4


def cell_rect(col, row):
    """Return a pygame.Rect for a grid cell, offset by the HUD height."""
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)


def random_food(snake_body):
    
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake_body:
            return (col, row)


def draw_grid(surface):
    """Draw a subtle grid so the play area is visible."""
    for c in range(COLS):
        for r in range(ROWS):
            rect = cell_rect(c, r)
            pygame.draw.rect(surface, GRAY, rect, 1)

def draw_walls(surface):
    """Fill the border cells with a different colour to represent walls."""
    for c in range(COLS):
        for r in range(ROWS):
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(surface, (80, 80, 80), cell_rect(c, r))

def draw_snake(surface, snake_body):
    """Draw each segment of the snake; head is lighter."""
    for i, (c, r) in enumerate(snake_body):
        color = GREEN if i == 0 else DARK_GREEN
        rect = cell_rect(c, r)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)   # thin outline

def draw_food(surface, food_pos):
    """Draw the food as a small circle centred in the cell."""
    c, r = food_pos
    rect = cell_rect(c, r)
    centre = rect.center
    pygame.draw.circle(surface, RED, centre, CELL // 2 - 2)

def draw_hud(surface, font, score, level):
    """Draw the score and level at the top of the window."""
    pygame.draw.rect(surface, (30, 30, 30), (0, 0, WIDTH, HUD_HEIGHT))
    score_surf = font.render(f"Score: {score}", True, WHITE)
    level_surf = font.render(f"Level: {level}", True, GOLD)
    surface.blit(score_surf, (10, 8))
    surface.blit(level_surf, (WIDTH - level_surf.get_width() - 10, 8))

def draw_message(surface, font_big, font_small, line1, line2):
    """Draw a centred two-line message (game-over / start screen)."""
    overlay = pygame.Surface((WIDTH, HEIGHT + HUD_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    t1 = font_big.render(line1, True, WHITE)
    t2 = font_small.render(line2, True, GOLD)
    cx = WIDTH // 2
    cy = (HEIGHT + HUD_HEIGHT) // 2
    surface.blit(t1, t1.get_rect(center=(cx, cy - 30)))
    surface.blit(t2, t2.get_rect(center=(cx, cy + 20)))

# ── Main game function ─────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + HUD_HEIGHT))
    pygame.display.set_caption("Snake – Practice 10")

    font       = pygame.font.SysFont("consolas", 22, bold=True)
    font_big   = pygame.font.SysFont("consolas", 48, bold=True)
    font_small = pygame.font.SysFont("consolas", 24)

    clock = pygame.time.Clock()

    # ── Game-state variables ───────────────────────────────────────────────────
    # Snake stored as a list of (col, row) tuples; index 0 = head
    start_col, start_row = COLS // 2, ROWS // 2
    snake   = [(start_col, start_row), (start_col - 1, start_row), (start_col - 2, start_row)]
    direction  = (1, 0)   # moving right
    next_dir   = direction

    food       = random_food(set(snake))
    score      = 0
    level      = 1
    foods_eaten = 0          # foods eaten in the current level

    game_over  = False
    started    = False       # waiting for first keypress

    while True:
        # ── Event handling ─────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not started:
                    started = True   # begin the game on first keypress

                # Arrow keys / WASD – prevent reversing direction
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_dir = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_dir = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_dir = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_dir = (1, 0)

                # Restart after game over
                if game_over and event.key == pygame.K_r:
                    main()   # restart by calling main() again
                    return

        # ── Update logic (only when game is running) ───────────────────────────
        if started and not game_over:
            direction = next_dir
            head_col, head_row = snake[0]
            new_head = (head_col + direction[0], head_row + direction[1])

            # 1. Wall/border collision
            nc, nr = new_head
            if nc <= 0 or nc >= COLS - 1 or nr <= 0 or nr >= ROWS - 1:
                game_over = True

            # 2. Self collision
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)   # move head forward

                # 3. Food eaten
                if new_head == food:
                    score      += 10 * level    # more points at higher levels
                    foods_eaten += 1
                    food = random_food(set(snake))   # 2. food not on snake/wall

                    # 3 & 4. Level up
                    if foods_eaten >= FOODS_PER_LEVEL:
                        level      += 1
                        foods_eaten = 0
                else:
                    snake.pop()   # remove tail only when no food eaten

        # ── Render ────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_walls(screen)
        draw_food(screen, food)
        draw_snake(screen, snake)
        draw_hud(screen, font, score, level)   # 5. score & level display

        if not started:
            draw_message(screen, font_big, font_small,
                         "SNAKE", "Press any arrow key to start")
        elif game_over:
            draw_message(screen, font_big, font_small,
                         "GAME OVER", f"Score: {score}   Level: {level}  |  R to restart")

        pygame.display.flip()

        # 4. Speed increases with level
        fps = BASE_FPS + (level - 1) * FPS_PER_LEVEL
        clock.tick(fps)


if __name__ == "__main__":
    main()
