import copy
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
        self.generation_count = 1

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

        print(self.population)

        self.generation_count += 1

        print("generating.... generation: " + str(self.generation_count))

        def get_score(individual_x):
            return individual_x.score

        self.population.sort(key=get_score, reverse=True)

        self.population = self.population[:math.floor(self.pop_size/2)]

        random.shuffle(self.population)

        first_half = self.population[:math.floor(self.pop_size/4)]
        first_half = copy.deepcopy(first_half)
        second_half = self.population[math.floor(self.pop_size/4):]
        second_half = copy.deepcopy(second_half)

        new_population = []

        for index, individual_a in enumerate(first_half):

            individual_b = second_half[index]

            new_individual_a, new_individual_b = self.crossover_individuals(individual_a, individual_b)

            print(new_individual_a)
            print(new_individual_b)

            new_population.append(new_individual_a)
            new_population.append(new_individual_b)

        self.population += new_population

        print(self.population)

        for index, individual in enumerate(self.population):
            individual = self.mutate_chromosome(individual, self.gaus_std_dev)

            individual.score = 0

        print(self.population)

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

        return self.population[0]

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
        #
        # print("ind a: ", individual_a)
        # print("ind b: ", individual_b)

        crossover_point = random.randint(1, self.size_of_chromosome-2)

        new_chromosome_a = individual_a.weight_chromosome[:crossover_point] + \
                           individual_b.weight_chromosome[crossover_point:]
        new_chromosome_b = individual_b.weight_chromosome[:crossover_point] + \
                           individual_a.weight_chromosome[crossover_point:]

        individual_a.weight_chromosome = new_chromosome_a
        individual_b.weight_chromosome = new_chromosome_b

        # print("ind a", individual_a.weight_chromosome)
        #
        # print("chr a: ", new_chromosome_a)
        # print("chr b: ", new_chromosome_b)
        #
        # print("ind a", individual_a)

        return individual_a, individual_b

    def mutate_chromosome(self, individual, std_dev):

        for point in range(self.size_of_chromosome):
            individual.weight_chromosome[point] = round(gaussian_mutator(individual.weight_chromosome[point],
                                                                         std_dev), 5)

        return individual

    def initialize_population(self, pop_size):

        self.population = []

        weight = [1, 0, 0, 0, 0, 0]
        self.population.append(Individual(weight, 0))

        weight = [0, 1, 0, 0, 0, 0]
        self.population.append(Individual(weight, 0))

        weight = [0, 0, 1, 0, 0, 0]
        self.population.append(Individual(weight, 0))

        weight = [0, 0, 0, 1, 0, 0]
        self.population.append(Individual(weight, 0))

        weight = [0, 0, 0, 0, 1, 0]
        self.population.append(Individual(weight, 0))

        weight = [0, 0, 0, 0, 0, 1]
        self.population.append(Individual(weight, 0))

        # weight = [0.14, 0.3, 0.82, 0.16, 0.76, 0.78]
        # self.population.append(Individual(weight, 0))
        #
        # weight = [0.521, 0.435, 0.924, 0.407, 0.262, 0.713]
        # self.population.append(Individual(weight, 0))

        for x in range(pop_size-6):

            # minimax
            # random_weight = [0.54, 0.5, 0.54, 0.76, 0.08, 0.58]

            # max
            random_weight = [0.14, 0.3, 0.82, 0.16, 0.76, 0.78]

            individual = Individual(random_weight, 0)

            for point in range(self.size_of_chromosome):
                individual.weight_chromosome[point] = round(gaussian_mutator(individual.weight_chromosome[point],
                                                                             0.1), 5)

            self.population.append(individual)

        print(self.population)
