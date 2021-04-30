from individual import Individual
import random
import numpy as np
import threading
import copy


class Population:
    """
        A class that describes a population of virtual individuals
    """

    def __init__(self, pop_size, num_nodes, mutation_rate, k, stop_generations, dependency):
        self.k = k  # target number of clusters
        self.population = []
        self.generations = 0
        self.stop_generations = stop_generations
        self.mutation_rate = mutation_rate
        self.best_ind = None
        self.overall_best_ind = None
        self.finished = False
        self.perfect_score = 2.0
        self.max_fitness = 0.0
        self.overall_max_fitness = 0.0
        self.average_fitness = 0.0
        self.mating_pool = []
        self.dependency = dependency
        self.new_population = []  # a placeholder for the new generation's population

        # Initialize the population & Calculate the initial fitness
        for i in range(pop_size):
            ind = Individual(num_nodes, self.k)
            ind.calc_fitness(self.dependency)
            if ind.fitness > self.max_fitness:
                self.max_fitness = ind.fitness
            self.average_fitness += ind.fitness
            self.population.append(ind)
        self.average_fitness /= pop_size

    def print_population_status(self):
        print("\nPopulation " + str(self.generations))
        print("Average fitness: " + str(self.average_fitness))
        print("Best individual: " + str(self.best_ind))

    # Natural selection using Roulette Wheel
    def roulette_wheel_selection(self, fitness_list, min_fitness, max_fitness):
        pop_size = len(self.population)
        if max_fitness > min_fitness:  # TODO: if not normalizing can avoid local max?
            # if -1 > min_fitness:
            # normalize by leaving out the least fit individual
            mating_quota_list = [round((f - min_fitness) * pop_size * self.k) for f in fitness_list]
        else:
            # not normalize when they performs equally
            # for not making everyone having a zero probability of being selected
            mating_quota_list = [round(f * pop_size * self.k) for f in fitness_list]
        for i in range(len(self.population)):
            mating_candidates = [i] * mating_quota_list[i]
            self.mating_pool.extend(mating_candidates)

    # Generate a mating pool according to the probability of each individual
    def natural_selection(self):
        self.mating_pool = []
        # TODO: The generation of pool can be improved.
        fitness_list = [ind.fitness for ind in self.population]
        min_fitness = min(fitness_list)
        max_fitness = max(fitness_list)

        self.roulette_wheel_selection(fitness_list,
                                      min_fitness,
                                      max_fitness)

    # Generate the new population based on the natural selection function
    def generate_new_population(self):
        new_population = []

        for i in range(len(self.population)):
            a, b = random.sample(self.mating_pool, 2)
            parentA, parentB = self.population[a], self.population[b]

            # CROSSOVER original version
            # child = parentA.crossover(parentB)
            # child.mutate(self.mutation_rate)
            # child.normalize_encoding()
            # child.calc_fitness(self.dependency)

            # # choose the best one may cause a local max
            # choices = [parentA, parentB, child]
            # max_idx = np.argmax([c.fitness for c in choices])
            # choices[max_idx].consistent_algorithm()
            # new_population.append(choices[max_idx])

            # # CROSSOVER2 two children version
            # child1, child2 = parentA.crossover2(parentB)
            # child1.mutate(self.mutation_rate)
            # child1.calc_fitness(self.dependency)
            # child2.mutate(self.mutation_rate)
            # child2.calc_fitness(self.dependency)
            #
            # # TODO: DECISION choose the best one may cause a local max
            # choices = [parentA, parentB, child1, child2]
            # max_idx = np.argmax([c.fitness for c in choices])
            # choices[max_idx].consistent_algorithm()
            # new_population.append(choices[max_idx])

            # CROSSOVER3
            child = parentA.crossover3(parentB)
            child.mutate(self.mutation_rate)
            child.normalize_encoding()
            child.calc_fitness(self.dependency)
            new_population.append(child)

        self.generations += 1
        self.population = new_population
    '''

    def generate_new_population_threaded(self, iter, start_indice, end_indice, mating_pool, population):
        new_sub_population = []
        for i in range(start_indice, end_indice):
            # a, b = random.sample(self.mating_pool, 2)
            # parentA, parentB = self.population[a], self.population[b]
            a, b = random.sample(mating_pool, 2)
            parentA, parentB = population[a], population[b]

            # CROSSOVER original version
            # child = parentA.crossover(parentB)
            # child.mutate(self.mutation_rate)
            # child.normalize_encoding()
            # child.calc_fitness(self.dependency)

            # # choose the best one may cause a local max
            # choices = [parentA, parentB, child]
            # max_idx = np.argmax([c.fitness for c in choices])
            # choices[max_idx].consistent_algorithm()
            # new_population.append(choices[max_idx])

            # # CROSSOVER2 two children version
            # child1, child2 = parentA.crossover2(parentB)
            # # TODO: Check when to mutate is better?
            # # child1.mutate(self.mutation_rate)
            # child1.calc_fitness(self.dependency)
            # # child2.mutate(self.mutation_rate)
            # child2.calc_fitness(self.dependency)
            #
            # # TODO: DECISION choose the best one may cause a local max
            # choices = [parentA, parentB, child1, child2]
            # max_idx = np.argmax([c.fitness for c in choices])
            # # TODO
            # # choices[max_idx].consistent_algorithm()
            # choices[max_idx].mutate(self.mutation_rate)
            # choices[max_idx].normalize_encoding()
            # child2.calc_fitness(self.dependency)
            # new_sub_population.append(choices[max_idx])

            # CROSSOVER3
            child = parentA.crossover3(parentB)
            child.mutate(self.mutation_rate)
            child.normalize_encoding()
            child.calc_fitness(self.dependency)
            new_sub_population.append(child)

        self.new_population[iter] = new_sub_population

    # Generate the new population based on the natural selection function
    def generate_new_population(self):

        thread_list = []
        num_threads = 4
        length_interval_population = len(self.population) // num_threads
        for iter in range(num_threads):
            self.new_population.append([])
            start = length_interval_population * iter
            end = start + length_interval_population if (iter < num_threads - 1) else len(self.population)
            t = threading.Thread(target=self.generate_new_population_threaded,
                                 args=(
                                     iter, start, end, copy.deepcopy(self.mating_pool), copy.deepcopy(self.population)))
            thread_list.append(t)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        self.generations += 1
        self.population = [ind for bucket in self.new_population for ind in bucket]
        self.new_population = []
    '''

    '''
    Compute/Identify the current "most fit" individual within the population
    '''
    def evaluate(self):
        self.max_fitness = 0
        self.average_fitness = 0

        for individual in self.population:
            if individual.fitness > self.max_fitness:
                self.max_fitness = individual.fitness
                self.best_ind = individual
            self.average_fitness += individual.fitness

        self.average_fitness /= len(self.population)

        if self.generations == self.stop_generations or self.best_ind.fitness == self.perfect_score:
            self.finished = True
        if self.max_fitness > self.overall_max_fitness:
            self.overall_max_fitness = self.max_fitness
            self.overall_best_ind = self.best_ind
