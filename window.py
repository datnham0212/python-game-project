import pygame as pg
import player 
import enemy
import random

WIDTH = 960
HEIGHT = 640

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 50)
        self.options = ["Start Game", "Options", "Quit"]
        self.selected = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 60))
            self.screen.blit(text, rect)

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pg.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pg.K_RETURN:
                return self.options[self.selected]
        return None

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 50)
        self.options =["Resume Game", "Return to Start Menu"]
        self.selected = 0
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 60))
            self.screen.blit(text, rect)

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pg.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pg.K_RETURN:
                return self.options[self.selected]
        return None


class Window:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        self.background = pg.image.load("assets/background.jpg")
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_x = 0
        self.background_y = 0
        self.background_y_speed = 1

        self.running = True
        self.in_start_menu = True
        self.start_menu = StartMenu(self.screen)

        self.in_pause_menu = False
        self.pause_menu = PauseMenu(self.screen)

        self.player = player.Player(self.screen)

        self.enemies = []   
        self.previous_spawn_time = 0
        self.enemy_cooldown = 2000

        pg.display.set_caption("Space Shooter")

        self.run()
    
    def run(self):
        clock = pg.time.Clock()

        while self.running:
            if self.in_start_menu:
                self.handle_start_menu()

            elif self.in_pause_menu:
                self.handle_pause_menu()
            
            else:
                self.handle_background()
                self.check_collisions()
                self.handle_events()
                self.constant_update_movements()
                self.initialize_screen()

            clock.tick(60) # Ensure 60fps
        
        pg.quit()
    
    def handle_start_menu(self):
        self.start_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.start_menu.handle_input(event)
            if action == "Start Game":
                self.in_start_menu = False
            elif action == "Options":
                print("Options menu not implemented yet")
            elif action == "Quit":
                self.running = False
        pg.display.update()
    
    def handle_pause_menu(self):
        self.pause_menu.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            action = self.pause_menu.handle_input(event)
            if action == "Resume Game":
                self.in_pause_menu = False
            elif action == "Return to Start Menu":
                self.in_pause_menu = False
                self.in_start_menu = True
        pg.display.update()
    
    
    def handle_background(self):
        self.background_y += self.background_y_speed
        if self.background_y == HEIGHT:
            self.background_y = 0
        
        self.screen.blit(self.background, (self.background_x, self.background_y))
        self.screen.blit(self.background, (0, self.background_y - HEIGHT))
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.in_pause_menu = True

    def constant_update_movements(self):
        keys = pg.key.get_pressed()
        self.player.move(keys)
        self.move_enemies()
        self.handle_shooting(keys)

    def initialize_screen(self):
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        self.player.draw()
        self.player.generate_lives()
        self.generate_enemies()
        pg.display.update()

    def generate_enemies(self):
        current_spawn_time = pg.time.get_ticks()
        if current_spawn_time - self.previous_spawn_time >= 1.5*self.enemy_cooldown:
            if random.random() < 0.5:
                new_enemy = enemy.Enemy(self.screen, random.randrange(50,900))
            else:
                new_enemy = enemy.Meteor(self.screen, random.randrange(50,900))
            self.enemies.append(new_enemy)
            self.previous_spawn_time = current_spawn_time

        self.draw_enemies()
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
    
    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
    
    def handle_shooting(self, keys):
        if keys[pg.K_z]:
            self.player.default_shot()

    def check_collisions(self):
        player_rect = pg.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for enemy in self.enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                print("Player hit!")
                self.player.max_lives -= 1
                
                if self.player.max_lives == 0:
                    self.running = False
                    print("Game Over")
                
                self.enemies.remove(enemy)
                break
                # Handle hit (e.g., decrease health, play sound, etc.)
        
        for laser in self.player.lasers:
            laser_rect = pg.Rect(laser.x, laser.y, laser.width, laser.height)
            for enemy in self.enemies:
                enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if laser_rect.colliderect(enemy_rect):
                    if enemy.take_damage():
                        self.enemies.remove(enemy)
                    self.player.lasers.remove(laser)
                    print("Enemy hit!")
                    # Handle hit (e.g., remove enemy, increase score, etc.)

    