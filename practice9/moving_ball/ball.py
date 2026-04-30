import pygame


class Ball:
    def __init__(self, x, y, radius=20, color=(220, 60, 60),
                 step=20, screen_w=800, screen_h=600):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.step = step
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.trail = []          # list of (x, y) for visual trail

    def move(self, dx, dy):
        """
        Move ball by (dx*step, dy*step).
        Ignores movement that would push the ball off-screen (boundary check).
        """
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        # Boundary conditions: ball must stay fully within screen
        min_x = self.radius
        max_x = self.screen_w - self.radius
        min_y = self.radius
        max_y = self.screen_h - self.radius

        # Only move if new position is valid (ignore off-screen input)
        if min_x <= new_x <= max_x:
            self.x = new_x
        if min_y <= new_y <= max_y:
            self.y = new_y

        # Record trail (keep last 8 positions)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.trail.clear()

    def draw(self, screen):
        # Draw fading trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail)) if self.trail else 0
            r = max(4, self.radius * (i + 1) // (len(self.trail) + 1))
            # Blend toward background
            fade_color = tuple(
                int(c * (i + 1) / len(self.trail))
                for c in self.color
            )
            pygame.draw.circle(screen, fade_color, (tx, ty), r)

        # Shadow
        pygame.draw.circle(screen, (15, 15, 20),
                           (self.x + 4, self.y + 5), self.radius)

        # Main ball with gradient illusion (two circles)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Highlight
        highlight_color = tuple(min(255, c + 80) for c in self.color)
        pygame.draw.circle(screen, highlight_color,
                           (self.x - self.radius // 4, self.y - self.radius // 4),
                           self.radius // 3)

        # Outline
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)
