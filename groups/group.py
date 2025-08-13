class Group:
    def __init__(self):
        self.agent_uuids = []
        self.leader = None
        self.color = None  # grup rengi

    def add_agent(self, agent):
        self.agent_uuids.append(agent.id)
        if not self.leader:
            self.leader = agent
            
    def remove_agent(self, agent):
        if agent.id in self.agent_uuids:
            self.agent_uuids.remove(agent.id)
            if self.leader == agent:
                self.leader = None  # basitçe lideri kaldır, yeni atama update sırasında olur