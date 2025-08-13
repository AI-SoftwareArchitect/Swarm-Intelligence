from groups.group import Group

class GroupManager:
    def __init__(self, agents):
        self.agents = agents
        self.groups = []

    def update_groups(self):
        """EntityManager zaten grupları oluşturuyor, sadece referans alıyoruz"""
        self.groups = list({agent.group_id for agent in self.agents if agent.group_id is not None})

    def get_groups(self):
        return self.groups
