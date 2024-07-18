import random
import asyncio

class AgentSelector:
    def __init__(self, agents, decrease_factor=0.85, increase_factor=1.15):
        self.agents = agents
        self.values = [agent[0] for agent in agents]
        self.weights = [agent[1] for agent in agents]
        self.initial_weights = self.weights[:]
        self.choice_counts = {agent: 0 for agent in self.values}
        self.decrease_factor = 0.85
        self.increase_factor = 1.15

    async def choose_agent(self):
        if not self.values:
            raise IndexError('Невозможно выбрать из пустой последовательности')
        chosen_agent = self.pseudo_random_choice()
        self.choice_counts[chosen_agent] += 1
        self.reset_weights_if_close_to_initial()
        return chosen_agent

    def pseudo_random_choice(self):
        chosen_agent = None
        adjusted_weights = [w * self.decrease_factor if agent == chosen_agent else w * self.increase_factor
                            for agent, w in zip(self.values, self.weights)]
        total_weight = sum(adjusted_weights)
        normalized_weights = [w / total_weight for w in adjusted_weights]
        chosen_agent = random.choices(self.values, weights=normalized_weights, k=1)[0]
        for i, agent in enumerate(self.values):
            if agent == chosen_agent:
                self.weights[i] *= self.decrease_factor
            else:
                self.weights[i] *= self.increase_factor
        total_weight_after_update = sum(self.weights)
        self.weights = [w / total_weight_after_update for w in self.weights]
        return chosen_agent

    def reset_weights_if_close_to_initial(self):
        for i, initial_weight in enumerate(self.initial_weights):
            for j, weight in enumerate(self.weights):
                if abs(weight - self.initial_weights[j]) > 2:
                    self.weights = self.initial_weights[:]
                    return


agents_list = lambda config: [("agent1", 5), ("agent2", 1), ("agent3", 2)]
Config = lambda section: None
selector = AgentSelector(agents_list(Config("agent")))

async def main():
    for _ in range(100):
        await selector.choose_agent()
    print(selector.choice_counts)

asyncio.run(main())