import pygame
import random
import json
import os
import db 


WIDTH, HEIGHT = 800, 600
SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4: Snake Advanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        
        
        self.load_settings()
        
        self.state = "MENU"
        self.username = ""
        self.reset_game()

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = {"snake_color": GREEN, "grid": True, "sound": True}

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def reset_game(self):
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.speed = 10
        self.obstacles = []
        self.food = self.spawn_item("FOOD")
        self.powerup = None
        self.shield = False
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.personal_best = db.get_personal_best(self.username) if self.username else 0

    def spawn_item(self, type):
        while True:
            pos = [random.randrange(1, WIDTH//SIZE)*SIZE, random.randrange(1, HEIGHT//SIZE)*SIZE]
            if pos not in self.snake and pos not in self.obstacles:
                if type == "FOOD":
                    # Шанс на разную еду
                    kind = random.choices(["normal", "heavy", "poison"], weights=[70, 20, 10])[0]
                    return {"pos": pos, "kind": kind, "time": pygame.time.get_ticks()}
                return {"pos": pos, "kind": random.choice(["speed", "slow", "shield"]), "time": pygame.time.get_ticks()}

    def draw_text(self, text, x, y, color=WHITE):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def run(self):
        while True:
            if self.state == "MENU": self.menu_screen()
            elif self.state == "GAME": self.game_screen()
            elif self.state == "GAMEOVER": self.game_over_screen()
            elif self.state == "LEADERBOARD": self.leaderboard_screen()
            elif self.state == "SETTINGS": self.settings_screen()

    def menu_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("SNAKE GAME - TSIS 4", 280, 150, GREEN)
        self.draw_text(f"Enter Name: {self.username}", 280, 250)
        self.draw_text("Press ENTER to Play", 280, 350)
        self.draw_text("L - Leaderboard | S - Settings", 260, 400)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username: self.state = "GAME"; self.reset_game()
                elif event.key == pygame.K_l: self.state = "LEADERBOARD"
                elif event.key == pygame.K_s: self.state = "SETTINGS"
                elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                else: 
                    if len(self.username) < 10: self.username += event.unicode

    def game_screen(self):
        self.screen.fill(BLACK)
        now = pygame.time.get_ticks()

        # Обработка клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != "DOWN": self.direction = "UP"
                if event.key == pygame.K_DOWN and self.direction != "UP": self.direction = "DOWN"
                if event.key == pygame.K_LEFT and self.direction != "RIGHT": self.direction = "LEFT"
                if event.key == pygame.K_RIGHT and self.direction != "LEFT": self.direction = "RIGHT"

        
        head = list(self.snake[0])
        if self.direction == "UP": head[1] -= SIZE
        if self.direction == "DOWN": head[1] += SIZE
        if self.direction == "LEFT": head[0] -= SIZE
        if self.direction == "RIGHT": head[0] += SIZE
        self.snake.insert(0, head)

        
        if head == self.food["pos"]:
            if self.food["kind"] == "poison":
                self.snake.pop(); self.snake.pop()
                if len(self.snake) <= 1: self.end_game()
            else:
                self.score += 10 if self.food["kind"] == "heavy" else 5
                if self.score // 50 > self.level - 1:
                    self.level += 1; self.speed += 2
                    if self.level >= 3: 
                        self.obstacles.append([random.randrange(1, WIDTH//SIZE)*SIZE, random.randrange(1, HEIGHT//SIZE)*SIZE])
            self.food = self.spawn_item("FOOD")
        else:
            self.snake.pop()

        # Бонусики
        if not self.powerup and now - self.last_powerup_spawn > 10000:
            self.powerup = self.spawn_item("POWERUP")
        
        if self.powerup:
            if now - self.powerup["time"] > 8000: self.powerup = None; self.last_powerup_spawn = now
            elif head == self.powerup["pos"]:
                if self.powerup["kind"] == "speed": self.speed += 5
                elif self.powerup["kind"] == "slow": self.speed = max(5, self.speed - 3)
                elif self.powerup["kind"] == "shield": self.shield = True
                self.powerup = None; self.last_powerup_spawn = now

        # Столкновения
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or 
            head in self.snake[1:] or head in self.obstacles):
            
            if self.shield: 
                self.shield = False  
                self.snake.pop(0)    
                print("Shield used!")
            else: 
                self.end_game()

        
        for p in self.snake: pygame.draw.rect(self.screen, self.settings["snake_color"], (*p, SIZE-2, SIZE-2))
        for obs in self.obstacles: pygame.draw.rect(self.screen, WHITE, (*obs, SIZE, SIZE))
        
        # Еда
        f_color = RED if self.food["kind"] == "heavy" else (DARK_RED if self.food["kind"] == "poison" else GREEN)
        pygame.draw.circle(self.screen, f_color, (self.food["pos"][0]+SIZE//2, self.food["pos"][1]+SIZE//2), SIZE//2)

        if self.powerup:
            pygame.draw.rect(self.screen, BLUE, (*self.powerup["pos"], SIZE, SIZE))

        self.draw_text(f"Score: {self.score} | Level: {self.level} | Best: {self.personal_best}", 10, 10)
        if self.shield: self.draw_text("SHIELD ACTIVE", 600, 10, YELLOW)
        
        pygame.display.update()
        self.clock.tick(self.speed)

    def end_game(self):
        db.save_game_result(self.username, self.score, self.level)
        self.state = "GAMEOVER"

    def game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 330, 200, RED)
        self.draw_text(f"Final Score: {self.score}", 320, 250)
        self.draw_text("Press SPACE to Menu", 290, 350)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: self.state = "MENU"
            if event.type == pygame.QUIT: pygame.quit(); exit()

    def leaderboard_screen(self):
        self.screen.fill(BLACK)
        scores = db.get_top_scores()
        self.draw_text("TOP 10 PLAYERS", 300, 50, YELLOW)
        for i, (name, sc, lv) in enumerate(scores):
            self.draw_text(f"{i+1}. {name} - {sc} pts (Lvl {lv})", 250, 100 + i*30)
        self.draw_text("Press M for Menu", 300, 500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m: self.state = "MENU"

    def settings_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("SETTINGS", 350, 100, BLUE)
        self.draw_text(f"1. Snake Color (Current: {self.settings['snake_color']})", 200, 200)
        self.draw_text("Press M for Menu", 320, 400)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    self.settings["snake_color"] = random.choice([GREEN, YELLOW, BLUE])
                    self.save_settings()
                if event.key == pygame.K_m: self.state = "MENU"

if __name__ == "__main__":
    Game().run()