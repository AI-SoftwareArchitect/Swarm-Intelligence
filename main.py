import pygame
import sys
import random
import math
from agent import Agent
from enemy import Enemy
from entity_manager.entity_manager import EntityManager
from groups.group_manager import GroupManager
from settings import *

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Swarm Intelligence with Enemies")
        self.clock = pygame.time.Clock()

        self.entity_manager = EntityManager()
        self.group_manager = GroupManager(self.entity_manager.agents)

        self.enemy_spawn_counter = 0
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 24)
    
    def spawn_enemy(self):
        self.enemy_spawn_counter += 1
        if self.enemy_spawn_counter >= ENEMY_SPAWN_RATE:
            self.entity_manager.enemies.append(Enemy())
            self.enemy_spawn_counter = 0

    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.agents = [Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
                                 for _ in range(AGENT_COUNT)]
                    self.enemies = []
                    self.score = 0
        return True
    
    def update(self):
        agents = self.entity_manager.agents
        enemies = self.entity_manager.enemies

        # Agent güncelleme
        for agent in agents:
            agent.update(agents)
        
        # Düşman güncelleme
        self.spawn_enemy()
        for enemy in enemies[:]:
            if enemy.update():
                enemies.remove(enemy)
        
        # Çarpışma kontrolü
        for enemy in enemies[:]:
            for agent in agents[:]:
                distance = math.dist((agent.x, agent.y), (enemy.x, enemy.y))
                if distance < enemy.size + AGENT_SIZE:
                    agents.remove(agent)
                    enemy.health -= 20
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        self.score += 10
                    break

        self.entity_manager.update_groups()  # KNN ve renk atama
        self.group_manager.update_groups()   # GroupManager güncel grupları alıyor

    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        agents = self.entity_manager.agents
        enemies = self.entity_manager.enemies

        # Agentları çiz
        for agent in agents:
            agent.draw(self.screen)
        
        # Düşmanları çiz
        for enemy in enemies:
            enemy.draw(self.screen)
        
        # HUD
        score_text = self.font.render(
            f"Score: {self.score} | Agents: {len(agents)} | Enemies: {len(enemies)}", 
            True, (255, 255, 255)
        )
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()