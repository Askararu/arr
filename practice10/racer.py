
import pygame
import random
import sys

WIDTH, HEIGHT = 600, 700
FPS           = 60


ROAD_LEFT  = 150
ROAD_RIGHT = 450
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3   


BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (100, 100, 100)
DARK_GRAY  = ( 50,  50,  50)
GREEN      = ( 34, 139,  34)
YELLOW     = (255, 220,   0)
RED        = (220,  50,  50)
BLUE       = ( 50, 100, 220)
GOLD       = (255, 200,   0)
SKY        = ( 70, 130, 180)


CAR_W, CAR_H = 40, 70


ENEMY_INTERVAL = 1500   
ENEMY_SPEED    = 5


COIN_INTERVAL = 1000    
COIN_RADIUS   = 12

# Road stripe animation
STRIPE_HEIGHT = 60
STRIPE_GAP    = 40

# ── Lane helpers
def lane_center(lane_index):
    """Return the x-centre of lane 0, 1, or 2."""
    return ROAD_LEFT + LANE_WIDTH * lane_index + LANE_WIDTH // 2


def draw_background(surface):
    """Draw sky and grass on the sides of the road."""
    surface.fill(GREEN)
    pygame.draw.rect(surface, SKY, (0, 0, WIDTH, HEIGHT // 4))

def draw_road(surface, stripe_offset):
    """Draw the asphalt and animated white lane stripes."""
    
    pygame.draw.rect(surface, DARK_GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    # Road edges (white kerb lines)
    pygame.draw.line(surface, WHITE, (ROAD_LEFT,  0), (ROAD_LEFT,  HEIGHT), 4)
    pygame.draw.line(surface, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    
    for lane in range(1, 3):   # two dividers between 3 lanes
        x = ROAD_LEFT + LANE_WIDTH * lane
        y = stripe_offset - STRIPE_HEIGHT
        while y < HEIGHT:
            pygame.draw.rect(surface, YELLOW, (x - 2, y, 4, STRIPE_HEIGHT))
            y += STRIPE_HEIGHT + STRIPE_GAP

def draw_car(surface, rect, color, highlight):
    """Draw a simple rectangular car with a windshield and wheels."""
    pygame.draw.rect(surface, color, rect, border_radius=6)
    # Windshield
    ws = pygame.Rect(rect.x + 6, rect.y + 8, rect.width - 12, 16)
    pygame.draw.rect(surface, highlight, ws, border_radius=3)
    # Wheels (four corners)
    wheel_color = BLACK
    ww, wh = 8, 14
    for cx in (rect.x - 4, rect.right - 4):
        for cy in (rect.y + 6, rect.bottom - 20):
            pygame.draw.rect(surface, wheel_color, (cx, cy, ww, wh), border_radius=3)

def draw_coin(surface, cx, cy):
    """Draw a gold coin as a circle with a $ sign."""
    pygame.draw.circle(surface, GOLD, (cx, cy), COIN_RADIUS)
    pygame.draw.circle(surface, (200, 160, 0), (cx, cy), COIN_RADIUS, 2)

def draw_hud(surface, font, coins, score):
    """Display coin count top-right and score top-left."""
    # Score (top-left)
    score_surf = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))
    # Coin icon + count (top-right)  ← Task 2: coin count in top-right corner
    pygame.draw.circle(surface, GOLD, (WIDTH - 80, 22), 12)
    coin_surf  = font.render(f"x {coins}", True, WHITE)
    surface.blit(coin_surf, (WIDTH - 60, 10))

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer – Practice 10")
    clock  = pygame.time.Clock()

    font     = pygame.font.SysFont("consolas", 22, bold=True)
    font_big = pygame.font.SysFont("consolas", 48, bold=True)
    font_med = pygame.font.SysFont("consolas", 26)

    # ── Player car ────────────────────────────────────────────────────────────
    player_lane = 1   # start in middle lane
    player_rect = pygame.Rect(0, 0, CAR_W, CAR_H)
    player_rect.centerx = lane_center(player_lane)
    player_rect.bottom  = HEIGHT - 30

    # ── Game state ─────────────────────────────────────────────────────────────
    enemy_cars  = []   # list of pygame.Rect
    coins       = []   # list of (cx, cy) tuples  ← Task 1: coins on road
    coin_count  = 0    # number of collected coins  ← Task 2: counter
    score       = 0

    stripe_offset = 0           # for road stripe animation
    enemy_timer   = 0           # ms since last enemy spawn
    coin_timer    = 0           # ms since last coin spawn

    game_over = False
    started   = False

    # ── Game loop ─────────────────────────────────────────────────────────────
    while True:
        dt = clock.tick(FPS)   # delta-time in milliseconds

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if not started:
                    started = True

                if not game_over:
                    # Move player between lanes
                    if event.key in (pygame.K_LEFT, pygame.K_a) and player_lane > 0:
                        player_lane -= 1
                    if event.key in (pygame.K_RIGHT, pygame.K_d) and player_lane < 2:
                        player_lane += 1

                if game_over and event.key == pygame.K_r:
                    main(); return   # restart

        if started and not game_over:
            # ── Move player car horizontally (smooth snap) ────────────────────
            target_x = lane_center(player_lane)
            player_rect.centerx += (target_x - player_rect.centerx) // 4

            # ── Animate road stripes ──────────────────────────────────────────
            stripe_offset = (stripe_offset + ENEMY_SPEED) % (STRIPE_HEIGHT + STRIPE_GAP)

            # ── Spawn enemy cars ──────────────────────────────────────────────
            enemy_timer += dt
            if enemy_timer >= ENEMY_INTERVAL:
                enemy_timer = 0
                lane = random.randint(0, 2)
                rect = pygame.Rect(0, -CAR_H, CAR_W, CAR_H)
                rect.centerx = lane_center(lane)
                enemy_cars.append(rect)

            # ── Spawn coins randomly on road  (Task 1) ────────────────────────
            coin_timer += dt
            if coin_timer >= COIN_INTERVAL:
                coin_timer = 0
                lane = random.randint(0, 2)
                cx   = lane_center(lane)
                cy   = -COIN_RADIUS             # start just above the screen
                coins.append([cx, cy])

            # ── Move enemies & check collision ───────────────────────────────
            for rect in enemy_cars[:]:
                rect.y += ENEMY_SPEED
                if rect.colliderect(player_rect):
                    game_over = True
                if rect.top > HEIGHT:
                    enemy_cars.remove(rect)
                    score += 10   # survived an enemy

            # ── Move coins & check collection (Task 1 + 2) ───────────────────
            for coin in coins[:]:
                coin[1] += ENEMY_SPEED           # scroll down at road speed
                cx, cy   = coin
                dist     = ((cx - player_rect.centerx)**2 + (cy - player_rect.centery)**2)**0.5
                if dist < COIN_RADIUS + CAR_W // 2:
                    coin_count += 1              # collect coin
                    score      += 5
                    coins.remove(coin)
                elif cy - COIN_RADIUS > HEIGHT:
                    coins.remove(coin)           # off-screen

        # ── Render ────────────────────────────────────────────────────────────
        draw_background(screen)
        draw_road(screen, stripe_offset)

        # Draw coins
        for cx, cy in coins:
            draw_coin(screen, int(cx), int(cy))

        # Draw enemy cars
        for rect in enemy_cars:
            draw_car(screen, rect, RED, (255, 120, 120))

        # Draw player car
        draw_car(screen, player_rect, BLUE, (120, 180, 255))

        # HUD: score + coin count (Task 2)
        draw_hud(screen, font, coin_count, score)

        # Overlay messages
        if not started:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            t = font_big.render("RACER", True, WHITE)
            s = font_med.render("Use ← → to change lanes", True, GOLD)
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
            screen.blit(s, s.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            t  = font_big.render("CRASH!", True, RED)
            s1 = font_med.render(f"Score: {score}   Coins: {coin_count}", True, WHITE)
            s2 = font_med.render("Press R to restart", True, GOLD)
            screen.blit(t,  t.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
            screen.blit(s1, s1.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))
            screen.blit(s2, s2.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
