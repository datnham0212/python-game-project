import pygame as pg
import laser
import window
import random

class Enemy:
    def __init__(self, screen, x):
        self.screen = screen
        self.image = pg.image.load("assets/ship1.png")
        self.x = x
        self.y = 0 # <= 200
        self.velocity = 3
        self.width = 70
        self.height = 70
        self.damage = 0
        self.lasers = []
        self.last_time = 0
        self.cooldown = random.randint(500, 2000)
        self.spawn_time = pg.time.get_ticks()
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        for laser in self.lasers:
            laser.draw(screen)

    def move(self):
        self.y += self.velocity

        for laser in self.lasers:
            laser.enemy_laser_move()

        self.lasers = [laser for laser in self.lasers if laser.y < window.HEIGHT]
    
    def enemy_shoot(self):
        #Return the current time since running the program
        current_time = pg.time.get_ticks()
        
        delay = random.randint(200, 3000)
        if current_time - self.spawn_time < delay:
            return

        #If the time since the last laser is greater than the cooldown, shoot a new laser
        if current_time - self.last_time >= self.cooldown:
            new_laser = laser.Laser(self.x + self.width / 2 - 2, self.y + self.height)  # Adjust x position for laser center
            self.lasers.append(new_laser)
            self.last_time = current_time
            self.cooldown = random.randint(500, 2000)

    def take_damage(self):
        self.damage += 1
        if self.damage >= 3:
            return True 
        return False

class Meteor:
    def __init__(self, screen, x):
        self.screen = screen
        self.image = pg.image.load("assets/meteor1.png")
        self.x = x
        self.y = 0 # <= 200
        self.velocity = 2
        self.width = 160
        self.height = 160
        self.damage = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.velocity

    def take_damage(self):
        self.damage += 1
        if self.damage >= 5:
            return True 
        return False

class ManageEnemies:
    def __init__(self, screen):
        self.screen = screen
        self.enemies = []
        self.meteors = []
        self.previous_spawn_time = 0
        self.enemy_cooldown = 2000

    def generate_enemies(self):
        current_spawn_time = pg.time.get_ticks()
        if current_spawn_time - self.previous_spawn_time >= 1.5 * self.enemy_cooldown:
            if random.random() < 0.5:
                new_enemy = Enemy(self.screen, random.randrange(50, 900))
                self.enemies.append(new_enemy)
            else:
                new_meteor = Meteor(self.screen, random.randrange(50, 900))
                self.meteors.append(new_meteor)
            self.previous_spawn_time = current_spawn_time

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()
        for meteor in self.meteors:
            meteor.move()

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for meteor in self.meteors:
            meteor.draw(self.screen)

            
