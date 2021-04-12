import logging
import sys
from population import Population
from individual import Individual


def main():
    pop_size = None  # TODO: file number
    mutation_rate = 0.01
    k = 10  # TODO: tune

    pop = Population(pop_size, mutation_rate, k)

    while not pop.finished:
        pop.natural_selection()
        pop.generate_new_population()
        pop.evaluate()
        pop.print_population_status()


def fitness_test():
    # output setting for debug mode
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ind = Individual(17, 5)
    ind.test()

def test_normalization():
    ind1, ind2, ind3 = Individual(7, 3), Individual(7, 3), Individual(7,3)
    ind1.cluster = [1, 1, 2, 1, 2, 3, 3]
    ind2.cluster = [3, 3, 1, 3, 1, 2, 2]
    ind3.cluster = [2, 2, 3, 2, 3, 1, 1]
    ind1.consistent_algorithm()
    ind2.consistent_algorithm()
    ind3.consistent_algorithm()

if __name__ == "__main__":
    # fitness_test()
    # main()
    test_normalization()
