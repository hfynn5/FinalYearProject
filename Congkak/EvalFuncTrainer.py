import math
import random
import statistics
from dataclasses import dataclass, field


@dataclass
class Individual:
    weight_chromosome: list[float]
    score: int


def gaussian_mutator(x, std_dev):
    return max(min(random.gauss(x, std_dev), 1), 0)


class EvalFuncTrainer:

    def __init__(self, max_generation_count, pop_size, size_of_chromosome, initial_std_dev):

        self.max_generation_count = max_generation_count
        self.generation_count = 0

        self.population = []

        self.pop_size = pop_size
        self.size_of_chromosome = size_of_chromosome

        self.gaus_std_dev = initial_std_dev

        self.individual_a_index = 0
        self.individual_b_index = -1

        self.initialize_population(self.pop_size)

        # print("length: " + str(len(self.population)))
        # for individual in self.population:
        #     print(individual)`

    def generate_next_population(self):

        self.generation_count += 1

        print("generating.... generation: " + str(self.generation_count))

        def get_score(individual_x):
            return individual_x.score

        self.population.sort(key=get_score, reverse=True)

        self.population = self.population[:math.floor(self.pop_size/2)]

        random.shuffle(self.population)

        first_half = self.population[:math.floor(self.pop_size/4)]
        second_half = self.population[math.floor(self.pop_size/4):]

        for index, individual_a in enumerate(first_half):

            individual_b = second_half[index]

            new_individual_a, new_individual_b = self.crossover_individuals(individual_a, individual_b)

            self.population.append(new_individual_a)
            self.population.append(new_individual_b)

        for index, individual in enumerate(self.population):
            individual = self.mutate_chromosome(individual, self.gaus_std_dev)

            individual.score = 0

        self.individual_a_index = 0
        self.individual_b_index = -1

        pass

    def get_next_two_agents(self):

        self.individual_b_index += 1

        if self.individual_b_index >= len(self.population):
            self.individual_b_index = 0
            self.individual_a_index += 1

            if self.individual_a_index >= len(self.population):
                return None

        return self.population[self.individual_a_index], self.population[self.individual_b_index]

    def get_best_individual(self):

        def get_score(individual_x):
            return individual_x.score

        self.population.sort(key=get_score, reverse=True)

        return self.population[1]

    def update_score(self, individual_a_score, individual_b_score):
        self.population[self.individual_a_index].score += individual_a_score
        self.population[self.individual_b_index].score += individual_b_score

    def check_if_converge(self, tolerance=0.05):

        value_ranges = []

        for i in range(self.size_of_chromosome):
            values = []
            for individual in self.population:
                values.append(individual.weight_chromosome[i])

            # value_range = max(values) - min(values)
            #
            # value_ranges.append(value_range)

            std_dev = statistics.stdev(values)

            if std_dev > tolerance:
                print("no converge")
                return False

        print("converge")
        return True

    def crossover_individuals(self, individual_a, individual_b):

        crossover_point = random.randint(0, self.size_of_chromosome)

        new_chromosome_a = individual_a.weight_chromosome[:crossover_point] + \
                           individual_b.weight_chromosome[crossover_point:]
        new_chromosome_b = individual_b.weight_chromosome[:crossover_point] + \
                           individual_a.weight_chromosome[crossover_point:]

        individual_a.weight_chromosome = new_chromosome_a
        individual_b.weight_chromosome = new_chromosome_b

        return individual_a, individual_b

    def mutate_chromosome(self, individual, std_dev):

        for point in range(self.size_of_chromosome):
            individual.weight_chromosome[point] = round(gaussian_mutator(individual.weight_chromosome[point],
                                                                         std_dev), 5)

        return individual

    def initialize_population(self, pop_size):

        self.population = []

        for x in range(pop_size):
            random_weight = []
            for c in range(self.size_of_chromosome):
                random_weight.append(round(random.random(), 5))

            self.population.append(Individual(random_weight, 0))
