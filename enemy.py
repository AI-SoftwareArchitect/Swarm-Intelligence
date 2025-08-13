import pygame
import random
import math
from settings import *

class Enemy:
    def __init__(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        
        if side == 'top':
            self.x = random.randint(0, WIDTH)
            self.y = -ENEMY_SIZE
        elif side == 'right':
            self.x = WIDTH + ENEMY_SIZE
            self.y = random.randint(0, HEIGHT)
        elif side == 'bottom':
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + ENEMY_SIZE
        else: # left
            self.x = -ENEMY_SIZE
            self.y = random.randint(0, HEIGHT)
            
        self.angle = math.atan2(HEIGHT/2 - self.y, WIDTH/2 - self.x)
        self.speed = random.uniform(*ENEMY_SPEED_RANGE)
        self.size = ENEMY_SIZE
        self.color = ENEMY_COLOR
        self.health = ENEMY_HEALTH
        
    def update(self):
        # Rastgele yön değişikliği
        self.angle += random.uniform(-0.2, 0.2)
        
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Ekran dışı kontrolü
        if (self.x < -100 or self.x > WIDTH+100 or 
            self.y < -100 or self.y > HEIGHT+100):
            return True
        return False
    
    def draw(self, surface):
        # Boyutlar
        body_width = self.size * 1.5
        body_height = self.size * 2.2
        track_width = self.size * 0.4
        track_height = self.size * 2
        turret_radius = self.size * 0.5
        barrel_length = self.size * 1.5
        barrel_width = self.size * 0.2

        # Sol palet
        left_track = pygame.Rect(
            int(self.x - body_width / 2 - track_width),
            int(self.y - track_height / 2),
            int(track_width),
            int(track_height)
        )
        pygame.draw.rect(surface, (60, 60, 60), left_track)

        # Sağ palet
        right_track = pygame.Rect(
            int(self.x + body_width / 2),
            int(self.y - track_height / 2),
            int(track_width),
            int(track_height)
        )
        pygame.draw.rect(surface, (60, 60, 60), right_track)

        # Gövde
        body_rect = pygame.Rect(
            int(self.x - body_width / 2),
            int(self.y - body_height / 2),
            int(body_width),
            int(body_height)
        )
        pygame.draw.rect(surface, self.color, body_rect)

        # Taret
        pygame.draw.circle(surface, (100, 100, 100), (int(self.x), int(self.y)), int(turret_radius))

        # Namlu (yukarı bakan)
        barrel_rect = pygame.Rect(
            int(self.x - barrel_width / 2),
            int(self.y - turret_radius - barrel_length),
            int(barrel_width),
            int(barrel_length)
        )
        pygame.draw.rect(surface, (80, 80, 80), barrel_rect)
