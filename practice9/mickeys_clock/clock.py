import pygame
import math
import datetime
import os


class Clock:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.center = (self.width // 2, self.height // 2)

        img_path = os.path.join(os.path.dirname(__file__), "images", "mickey_hand.png")
        if os.path.exists(img_path):
            raw = pygame.image.load(img_path).convert_alpha()
            self.hand_img = pygame.transform.scale(raw, (30, 120))
        else:
            # Draw a simple glove-shaped hand as fallback
            self.hand_img = self._make_hand_surface(30, 120, (255, 255, 255))

        self.minutes = 0
        self.seconds = 0

        # Font for displaying digital time
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        # Clock face radius
        self.radius = 220

    def _make_hand_surface(self, w, h, color):
        """Create a stylized glove-hand surface when no image is available."""
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Arm part
        arm_rect = pygame.Rect(w // 2 - 6, h // 4, 12, h * 3 // 4)
        pygame.draw.rect(surf, color, arm_rect, border_radius=6)
        # Palm
        palm_rect = pygame.Rect(2, h // 8, w - 4, h // 4)
        pygame.draw.ellipse(surf, color, palm_rect)
        # Fingers (3 bumps)
        for i in range(3):
            fx = 4 + i * (w - 8) // 3
            fy = 2
            pygame.draw.ellipse(surf, color, (fx, fy, (w - 8) // 3, h // 8 + 4))
        return surf

    def update(self):
        now = datetime.datetime.now()
        self.minutes = now.minute
        self.seconds = now.second
        self.time_str = now.strftime("%H:%M:%S")

    def _draw_hand(self, angle_deg, length_scale=1.0, color_tint=(255, 255, 255)):
        """Rotate and blit a hand at the given angle (0=up, clockwise)."""
        # Scale the hand
        scaled = pygame.transform.scale(
            self.hand_img,
            (int(self.hand_img.get_width() * length_scale),
             int(self.hand_img.get_height() * length_scale))
        )
        # Tint by creating a colored copy
        tinted = scaled.copy()
        tinted.fill((*color_tint, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Rotate: pygame rotates CCW, so negate; 0° = top = -90° in math
        rotated = pygame.transform.rotate(tinted, -angle_deg)

        # The hand pivot is at the bottom-center of the image.
        # After rotation, we need to offset so the pivot lands on center.
        orig_w = scaled.get_width()
        orig_h = scaled.get_height()

        # Pivot point in original image coordinates (bottom-center)
        pivot_x = orig_w / 2
        pivot_y = orig_h  # bottom

        # Compute where pivot moves after rotation
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Offset from center of original to pivot
        dx = pivot_x - orig_w / 2
        dy = pivot_y - orig_h / 2

        # Rotate offset
        rotated_dx = dx * cos_a - dy * (-sin_a)
        rotated_dy = dx * sin_a + dy * cos_a

        # Center of rotated image
        rot_cx = rotated.get_width() / 2
        rot_cy = rotated.get_height() / 2

        # Final blit position so pivot aligns with screen center
        blit_x = self.center[0] - (rot_cx + rotated_dx)
        blit_y = self.center[1] - (rot_cy + rotated_dy)

        self.screen.blit(rotated, (int(blit_x), int(blit_y)))

    def draw(self):
        cx, cy = self.center

        # --- Draw clock face ---
        pygame.draw.circle(self.screen, (50, 50, 50), self.center, self.radius)
        pygame.draw.circle(self.screen, (200, 200, 200), self.center, self.radius, 4)

        # Tick marks
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                r_inner, r_outer = self.radius - 20, self.radius - 4
                color = (255, 255, 255)
                width = 3
            else:
                r_inner, r_outer = self.radius - 10, self.radius - 4
                color = (150, 150, 150)
                width = 1
            x1 = cx + int(r_inner * math.cos(angle))
            y1 = cy + int(r_inner * math.sin(angle))
            x2 = cx + int(r_outer * math.cos(angle))
            y2 = cy + int(r_outer * math.sin(angle))
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

        # Hour labels (12, 3, 6, 9)
        for hour, label in [(12, "12"), (3, "3"), (6, "6"), (9, "9")]:
            angle = math.radians(hour * 30 - 90)
            lx = cx + int((self.radius - 42) * math.cos(angle))
            ly = cy + int((self.radius - 42) * math.sin(angle))
            txt = self.small_font.render(label, True, (220, 220, 220))
            self.screen.blit(txt, (lx - txt.get_width() // 2, ly - txt.get_height() // 2))

        # --- Calculate angles ---
        # Minutes: right hand — 360° per 60 min
        minute_angle = self.minutes * 6  # degrees from 12 o'clock
        # Seconds: left hand — 360° per 60 sec
        second_angle = self.seconds * 6

        # --- Draw hands ---
        # Right hand = minutes (yellow-ish)
        self._draw_hand(minute_angle, length_scale=1.0, color_tint=(255, 230, 100))
        # Left hand = seconds (cyan-ish)
        self._draw_hand(second_angle, length_scale=0.85, color_tint=(100, 220, 255))

        # Center dot
        pygame.draw.circle(self.screen, (255, 80, 80), self.center, 10)
        pygame.draw.circle(self.screen, (200, 200, 200), self.center, 10, 2)

        # --- Digital time display ---
        time_surf = self.font.render(self.time_str, True, (255, 255, 255))
        self.screen.blit(time_surf, (cx - time_surf.get_width() // 2, cy + self.radius // 2 + 10))

        # Legend
        min_label = self.small_font.render("Yellow = Minutes  |  Cyan = Seconds", True, (180, 180, 180))
        self.screen.blit(min_label, (cx - min_label.get_width() // 2, cy + self.radius // 2 + 54))
