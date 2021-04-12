from individual import Individual
import random
import numpy as np


class Population:
    """
        A class that describes a population of virtual individuals
    """

    def __init__(self, pop_size, num_nodes, mutation_rate, k, stop_generations):
        self.k = k  # target number of clusters
        self.population = []
        self.generations = 0
        self.stop_generations = stop_generations
        self.mutation_rate = mutation_rate
        self.best_ind = None
        self.finished = False
        self.perfect_score = 2.0
        self.max_fitness = 0.0
        self.average_fitness = 0.0
        self.mating_pool = []

        # Initialize the population & Calculate the initial fitness
        for i in range(pop_size):
            ind = Individual(num_nodes, self.k)
            ind.calc_fitness()
            if ind.fitness > self.max_fitness:
                self.max_fitness = ind.fitness
            self.average_fitness += ind.fitness
            self.population.append(ind)
        self.average_fitness /= pop_size

    def print_population_status(self):
        print("\nPopulation " + str(self.generations))
        print("Average fitness: " + str(self.average_fitness))
        print("Best individual: " + str(self.best_ind))

    # Generate a mating pool according to the probability of each individual
    def natural_selection(self):
        self.mating_pool = []
        # TODO: The generation of pool can be improved.
        for i in range(len(self.population)):
            n = int(self.population[i].fitness * len(self.population))
            self.mating_pool.extend([i] * n)

    # Generate the new population based on the natural selection function
    # TODO: modify
    def generate_new_population(self):
        new_population = []

        for i in range(len(self.population)):
            a, b = random.sample(self.mating_pool, 2)
            parentA, parentB = self.population[a], self.population[b]

            child = parentA.crossover(parentB)
            child.mutate(self.mutation_rate)
            child.calc_fitness()
            # TODO: Enhancement
            choices = [parentA, parentB, child]
            max_idx = np.argmax([c.fitness for c in choices])
            choices[max_idx].consistent_algorithm()
            new_population.append(choices[max_idx])

        # TODO: normalize encoding
        self.generations += 1
        self.population = new_population

    '''
    Compute/Identify the current "most fit" individual within the population
    '''
    # TODO: modify fitness function
    def evaluate(self):
        self.max_fitness = 0
        self.average_fitness = 0

        for individual in self.population:
            # individual.calc_fitness()
            if individual.fitness > self.max_fitness:
                self.max_fitness = individual.fitness
                self.best_ind = individual
            self.average_fitness += individual.fitness

        self.average_fitness /= len(self.population)

        if self.generations == self.stop_generations or self.best_ind.fitness == self.perfect_score:
            self.finished = True
