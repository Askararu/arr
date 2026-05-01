import pygame
import random

SCREEN_WIDTH = 400
LANES = [50, 150, 250, 350]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255)) # Default Blue
        self.rect = self.image.get_rect(center=(LANES[1], 500))
        self.lane_index = 1
        self.shielded = False
        self.nitro_timer = 0

    def update(self):
        self.rect.centerx = LANES[self.lane_index]
        if self.nitro_timer > 0:
            self.nitro_timer -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 600:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type # "Nitro", "Shield", "Repair"
        colors = {"Nitro": (255, 165, 0), "Shield": (0, 255, 255), "Repair": (0, 255, 0)}
        self.image = pygame.Surface((30, 30))
        self.image.fill(colors[type])
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > 600:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self, h_type):
        super().__init__()
        self.h_type = h_type # "Oil", "Barrier"
        self.image = pygame.Surface((50, 30))
        self.image.fill((100, 100, 100) if h_type == "Barrier" else (50, 50, 50))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > 600:
            self.kill()