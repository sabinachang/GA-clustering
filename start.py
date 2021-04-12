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


if __name__ == "__main__":
    fitness_test()
    # main()
