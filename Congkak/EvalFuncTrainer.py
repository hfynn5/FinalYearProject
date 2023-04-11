import random
from dataclasses import dataclass, field


@dataclass
class Individual:
    weight_chromosome: list[float]
    score: int


def gaussian_mutator(x, std_dev):
    return max(min(random.gauss(x, std_dev), 1), 0)


class EvalFuncTrainer:

    def __init__(self, pop_size, size_of_chromosome, initial_std_dev):

        self.population = []

        self.pop_size = pop_size
        self.size_of_chromosome = size_of_chromosome

        self.gaus_std_dev = initial_std_dev

        self.individual_a_index = 0
        self.individual_b_index = -1

        self.initialize_population(self.pop_size)


    def get_next_two_agents(self):

        self.individual_b_index += 1

        if self.individual_b_index >= len(self.population):
            self.individual_b_index = 0
            self.individual_a_index += 1

            if self.individual_a_index >= len(self.population):
                return None

        return self.population[self.individual_a_index], self.population[self.individual_b_index]

    def update_score(self, individual_a_score, individual_b_score):
        self.population[self.individual_a_index].score += individual_a_score
        self.population[self.individual_b_index].score += individual_b_score

    def crossover_individuals(self, individual_a, individual_b):

        crossover_point = random.randint(0, self.size_of_chromosome)

        # chromosome_a_start = individual_a.weight_chromosome[:crossover_point]
        # chromosome_a_end = individual_a.weight_chromosome[crossover_point:]
        # chromosome_b_start = individual_b.weight_chromosome[:crossover_point]
        # chromosome_b_end = individual_b.weight_chromosome[crossover_point:]

        # new_chromosome_a = chromosome_a_start + chromosome_b_end
        # new_chromosome_b = chromosome_b_start + chromosome_a_end

        new_chromosome_a = individual_a.weight_chromosome[:crossover_point] + \
                           individual_b.weight_chromosome[crossover_point:]
        new_chromosome_b = individual_b.weight_chromosome[:crossover_point] + \
                           individual_a.weight_chromosome[crossover_point:]

        individual_a.weight_chromosome = new_chromosome_a
        individual_b.weight_chromosome = new_chromosome_b

        return individual_a, individual_b

    def mutate_chromosome(self, individual, mutation_rate, std_dev):

        for point in range(self.size_of_chromosome):
            individual.weight_chromosome[point] = gaussian_mutator(individual.weight_chromosome[point],
                                                                   std_dev)

        return individual

    def initialize_population(self, pop_size):

        self.population = []

        for x in range(pop_size):
            random_weight = []
            for c in range(self.size_of_chromosome):
                random_weight.append(random.random())

            self.population.append(Individual(random_weight, 0))
