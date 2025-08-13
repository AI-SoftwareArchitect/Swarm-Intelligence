import pygame
import math
import random
from pygame import gfxdraw
from settings import *
import uuid

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.history = []
        self.id = uuid.uuid4()
        self.color = AGENT_COLOR
        self.group_id = None  # hangi gruba ait olduğunu saklar
        self.color_timer = 0  # saniye cinsinden
        
    def update(self, agents):
        cohesion, alignment, separation, total_neighbors = self.calculate_behaviors(agents)
        steering = self.combine_behaviors(cohesion, alignment, separation, total_neighbors)
        self.apply_steering(steering)
        self.move()
        self.handle_borders()
        self.update_history()

    def set_color(self, rgb):
        import time
        now = time.time()
        if now - self.color_timer > 2:  # en az 2 saniye bekle
            self.color = rgb
            self.color_timer = now
    
    def calculate_behaviors(self, agents):
        cohesion = pygame.Vector2(0, 0)
        alignment = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        total_neighbors = 0
        
        for other in agents:
            distance = math.dist((self.x, self.y), (other.x, other.y))
            
            if distance < PERCEPTION_RADIUS:
                cohesion += pygame.Vector2(other.x, other.y)
                alignment += pygame.Vector2(math.cos(other.angle), math.sin(other.angle))
                
                if distance < SEPARATION_RADIUS:
                    diff = pygame.Vector2(self.x - other.x, self.y - other.y)
                    if distance > 0:
                        diff /= distance
                    separation += diff
                
                total_neighbors += 1
        
        return cohesion, alignment, separation, total_neighbors
    
    def combine_behaviors(self, cohesion, alignment, separation, total_neighbors):
        if total_neighbors > 0:
            cohesion /= total_neighbors
            cohesion = pygame.Vector2(cohesion - pygame.Vector2(self.x, self.y))
            cohesion = cohesion.normalize() * COHESION_WEIGHT if cohesion.length() > 0 else cohesion
            
            alignment /= total_neighbors
            alignment = alignment.normalize() * ALIGNMENT_WEIGHT if alignment.length() > 0 else alignment
            
            separation = separation.normalize() * SEPARATION_WEIGHT if separation.length() > 0 else separation
        
        return cohesion + alignment + separation
    
    def apply_steering(self, steering):
        if steering.length() > 0:
            desired_angle = math.atan2(steering.y, steering.x)
            angle_diff = (desired_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += angle_diff * TURN_FACTOR
    
    def move(self):
        self.x += math.cos(self.angle) * AGENT_SPEED
        self.y += math.sin(self.angle) * AGENT_SPEED
    
    def handle_borders(self):
        if self.x < 0:
            self.angle = random.uniform(-math.pi/2, math.pi/2)
            self.x = 0
        elif self.x > WIDTH:
            self.angle = random.uniform(math.pi/2, 3*math.pi/2)
            self.x = WIDTH
            
        if self.y < 0:
            self.angle = random.uniform(0, math.pi)
            self.y = 0
        elif self.y > HEIGHT:
            self.angle = random.uniform(math.pi, 2*math.pi)
            self.y = HEIGHT
    
    def update_history(self):
        self.history.append((self.x, self.y))
        if len(self.history) > HISTORY_LENGTH:
            self.history.pop(0)
    
    def draw(self, surface):
        # Drone gövdesi
        body_length = AGENT_SIZE * 2.5
        body_width = AGENT_SIZE
        
        center = pygame.Vector2(self.x, self.y)
        angle_rad = self.angle
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Drone şekli
        points = [
            pygame.Vector2(-body_length/2, -body_width/2),
            pygame.Vector2(body_length/2, -body_width/2),
            pygame.Vector2(body_length/2, body_width/2),
            pygame.Vector2(-body_length/2, body_width/2)
        ]
        
        rotated_points = []
        for point in points:
            rotated_x = point.x * cos_a - point.y * sin_a + center.x
            rotated_y = point.x * sin_a + point.y * cos_a + center.y
            rotated_points.append((rotated_x, rotated_y))
        
        pygame.draw.polygon(surface, self.color, rotated_points)
        
        # Yön çizgisi
        front_x = (body_length/2 + 5) * cos_a + center.x
        front_y = (body_length/2 + 5) * sin_a + center.y
        pygame.draw.line(surface, (255, 255, 255), center, (front_x, front_y), 2)