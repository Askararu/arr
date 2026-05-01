import pygame
import random
from config import *

class Food:
    def __init__(self, obstacles):
        self.pos = self.generate_pos(obstacles)
        self.type = random.choice(["normal", "heavy", "poison"])
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 5000 if self.type == "heavy" else 10000

    def generate_pos(self, obstacles):
        while True:
            pos = [random.randrange(1, WIDTH//CELL_SIZE) * CELL_SIZE,
                   random.randrange(1, HEIGHT//CELL_SIZE) * CELL_SIZE]
            if pos not in obstacles: return pos

class PowerUp:
    def __init__(self, obstacles):
        self.pos = self.generate_pos(obstacles)
        self.type = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()

    def generate_pos(self, obstacles):
        while True:
            pos = [random.randrange(1, WIDTH//CELL_SIZE) * CELL_SIZE,
                   random.randrange(1, HEIGHT//CELL_SIZE) * CELL_SIZE]
            if pos not in obstacles: return pos

class Snake:
    def __init__(self, color):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.dir = "RIGHT"
        self.color = color
        self.shield = False

    def move(self):
        head = list(self.body[0])
        if self.dir == "UP": head[1] -= CELL_SIZE
        if self.dir == "DOWN": head[1] += CELL_SIZE
        if self.dir == "LEFT": head[0] -= CELL_SIZE
        if self.dir == "RIGHT": head[0] += CELL_SIZE
        self.body.insert(0, head)

    def draw(self, surface):
        for part in self.body:
            pygame.draw.rect(surface, self.color, (*part, CELL_SIZE, CELL_SIZE))
        if self.shield: 
            pygame.draw.rect(surface, YELLOW, (*self.body[0], CELL_SIZE, CELL_SIZE), 2)