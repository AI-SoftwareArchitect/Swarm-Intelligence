from agent import Agent
from enemy import Enemy
from settings import *
import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
from groups.group import Group
import time

class EntityManager:
    _instance = None  # Singleton örnek saklama

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EntityManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # __init__ birden fazla çağrılırsa tekrar oluşturmayı önle
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.agents = [Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
                       for _ in range(AGENT_COUNT)]
        self.enemies = []
        self.n_neighbors = 5  # KNN parametresi
        self.groups = []

        self._initialized = True  # init bir kere çalışacak

     def validate_group_colors(self,group_id):
        agents = [agent for agent in self.agents if agent.group_id == group_id]
        group = [group for group in self.groups if group.id == group_id][0]
        for agent in agents:
            if agent.color != group.color:
                agent.set_color(group.color)

    def update_groups(self):
        """Tüm ajanları KNN ile gruplara ayırır ve renk atar"""
        if not self.agents:
            self.groups = []
            return

        positions = np.array([[agent.x, agent.y] for agent in self.agents])
        nbrs = NearestNeighbors(n_neighbors=self.n_neighbors, algorithm='ball_tree').fit(positions)
        distances, indices = nbrs.kneighbors(positions)

        visited = set()
        new_groups = []

        for i, agent in enumerate(self.agents):
            if agent.id in visited:
                continue

            neighbors = indices[i]
            group = Group()
            group.color = np.random.randint(0, 255, size=3).tolist()


            for idx in neighbors:
                neighbor = self.agents[idx]
                if neighbor.id in visited:
                    continue
                group.add_agent(neighbor)
                visited.add(neighbor.id)
                neighbor.group_id = group

                # Renk atama: minimum 2 saniye sabit
                now = time.time()
                if not hasattr(neighbor, 'color_timer'):
                    neighbor.color_timer = 0
                if now - neighbor.color_timer > 2:
                    neighbor.set_color(group.color)
                    neighbor.color_timer = now

            new_groups.append(group)
            validate_group_colors(group.id)

        self.groups = new_groups


