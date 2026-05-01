import pygame
import random
from racer import Player, Enemy, PowerUp, Hazard
from ui import Button, draw_text
import persistence

pygame.init()
SCREEN = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Street Racer")
CLOCK = pygame.time.Clock()

class Game:
    def __init__(self):
        # имя
        self.state = "NAME_INPUT"
        self.settings = persistence.get_settings()
        self.username = "" 
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.distance = 0
        self.enemy_speed = 5
        self.active_powerup = None

    def run(self):
        while True:
            if self.state == "NAME_INPUT":
                self.name_input_screen()
            elif self.state == "MENU":
                self.main_menu()
            elif self.state == "GAME":
                self.game_loop()
            elif self.state == "GAMEOVER":
                self.game_over()
            elif self.state == "SETTINGS":
                self.settings_screen()
            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()

    def name_input_screen(self):
        while self.state == "NAME_INPUT":
            SCREEN.fill((20, 20, 40)) 
            draw_text(SCREEN, "ENTER YOUR NAME:", 32, 60, 200)

            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 250, 300, 50), 2)
            
            draw_text(SCREEN, self.username + "_", 32, 60, 260, (255, 255, 0))
            
            draw_text(SCREEN, "Press ENTER to start", 20, 100, 320, (150, 150, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.username.strip() == "":
                            self.username = "Guest" 
                        self.state = "MENU" 
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        
                        if len(self.username) < 12:
                            self.username += event.unicode

            pygame.display.flip()
            CLOCK.tick(30)

    def main_menu(self):
        play_btn = Button("PLAY", 100, 200, 200, 50, (0, 150, 0), (0, 200, 0))
        lb_btn = Button("LEADERBOARD", 100, 270, 200, 50, (0, 0, 150), (0, 0, 200))
        set_btn = Button("SETTINGS", 100, 340, 200, 50, (100, 100, 100), (150, 150, 150))
        quit_btn = Button("QUIT", 100, 410, 200, 50, (150, 0, 0), (200, 0, 0))

        while self.state == "MENU":
            SCREEN.fill((30, 30, 30))
            draw_text(SCREEN, f"HELLO, {self.username.upper()}!", 28, 50, 100, (255, 255, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if play_btn.is_clicked(event): self.state = "GAME"; self.reset_game()
                if lb_btn.is_clicked(event): self.state = "LEADERBOARD"
                if set_btn.is_clicked(event): self.state = "SETTINGS"
                if quit_btn.is_clicked(event): pygame.quit(); exit()

            play_btn.draw(SCREEN); lb_btn.draw(SCREEN)
            set_btn.draw(SCREEN); quit_btn.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(30)

    def game_loop(self):
        spawn_timer = 0
        while self.state == "GAME":
            SCREEN.fill((50, 50, 50))
            dt = CLOCK.tick(60)
            
            # Difficulty Scaling & Distance
            move_speed = 10 if self.player.nitro_timer > 0 else 5
            self.distance += move_speed / 100
            self.enemy_speed = 5 + (self.distance // 10)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.player.lane_index > 0:
                        self.player.lane_index -= 1
                    if event.key == pygame.K_RIGHT and self.player.lane_index < 3:
                        self.player.lane_index += 1

            # Spawning (Safe spawn logic)
            spawn_timer += 1
            if spawn_timer > max(20, 60 - int(self.distance)):
                obj_type = random.random()
                if obj_type < 0.7:
                    new_enemy = Enemy(self.enemy_speed)
                    self.enemies.add(new_enemy); self.all_sprites.add(new_enemy)
                elif obj_type < 0.85:
                    new_h = Hazard(random.choice(["Oil", "Barrier"]))
                    self.hazards.add(new_h); self.all_sprites.add(new_h)
                else:
                    new_p = PowerUp(random.choice(["Nitro", "Shield", "Repair"]))
                    self.powerups.add(new_p); self.all_sprites.add(new_p)
                spawn_timer = 0

            # Collisions
            if pygame.sprite.spritecollide(self.player, self.enemies, True) or \
               pygame.sprite.spritecollide(self.player, self.hazards, True):
                if self.player.shielded:
                    self.player.shielded = False
                    self.active_powerup = None
                else:
                    persistence.save_score(self.username, int(self.score), self.distance)
                    self.state = "GAMEOVER"

            p_col = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for p in p_col:
                self.active_powerup = p.type
                if p.type == "Nitro": self.player.nitro_timer = 180 # 3 seconds
                if p.type == "Shield": self.player.shielded = True
                if p.type == "Repair": self.score += 50 # Bonus for "clearing"

            # Updates
            self.all_sprites.update()
            self.all_sprites.draw(SCREEN)
            
            # UI Overlay
            draw_text(SCREEN, f"Score: {int(self.score)}", 24, 10, 10)
            draw_text(SCREEN, f"Dist: {self.distance:.1f}m", 24, 10, 40)
            if self.active_powerup:
                timer_txt = f": {self.player.nitro_timer//60}s" if self.active_powerup == "Nitro" else ""
                draw_text(SCREEN, f"Power: {self.active_powerup}{timer_txt}", 24, 10, 70, (255, 255, 0))

            pygame.display.flip()

    def game_over(self):
        retry_btn = Button("RETRY", 100, 300, 200, 50, (0, 150, 0), (0, 200, 0))
        menu_btn = Button("MENU", 100, 370, 200, 50, (100, 100, 100), (150, 150, 150))
        
        while self.state == "GAMEOVER":
            SCREEN.fill((50, 0, 0))
            draw_text(SCREEN, "GAME OVER", 48, 80, 100)
            draw_text(SCREEN, f"Final Score: {int(self.score)}", 32, 100, 180)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if retry_btn.is_clicked(event): self.state = "GAME"; self.reset_game()
                if menu_btn.is_clicked(event): self.state = "MENU"

            retry_btn.draw(SCREEN); menu_btn.draw(SCREEN)
            pygame.display.flip()

    def leaderboard_screen(self):
        back_btn = Button("BACK", 100, 500, 200, 50, (100, 100, 100), (150, 150, 150))
        scores = persistence.get_leaderboard()
        while self.state == "LEADERBOARD":
            SCREEN.fill((30, 30, 30))
            draw_text(SCREEN, "TOP 10", 40, 140, 30)
            for i, entry in enumerate(scores):
                draw_text(SCREEN, f"{i+1}. {entry['name']} - {entry['score']}", 24, 50, 100 + (i*35))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if back_btn.is_clicked(event): self.state = "MENU"
            
            back_btn.draw(SCREEN)
            pygame.display.flip()

    def settings_screen(self):
        # Simplified settings toggle logic
        back_btn = Button("BACK", 100, 500, 200, 50, (100, 100, 100), (150, 150, 150))
        while self.state == "SETTINGS":
            SCREEN.fill((30, 30, 30))
            draw_text(SCREEN, "SETTINGS", 40, 120, 50)
            draw_text(SCREEN, f"Sound: {'ON' if self.settings['sound'] else 'OFF'}", 30, 100, 150)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if back_btn.is_clicked(event): 
                    persistence.save_settings(self.settings)
                    self.state = "MENU"

            back_btn.draw(SCREEN)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()