import random
from dataclasses import dataclass, field


@dataclass
class Individual:
    weight_chromosome: list[float]
    score: int


class EvalFuncTrainer:

    def __init__(self, pop_size, size_of_chromosome):

        self.population = []

        self.pop_size = pop_size
        self.size_of_chromosome = size_of_chromosome

        self.initialize_population(self.pop_size)

        pass

    def initialize_population(self, pop_size):

        self.population = []

        for x in range(pop_size):
            random_weight = []
            for c in range(self.size_of_chromosome):
                random_weight.append(random.random())

            self.population.append(Individual(random_weight, 0))