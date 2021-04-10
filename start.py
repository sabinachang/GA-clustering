from population import Population


def main():
    pop_size = None # TODO: file number
    mutation_rate = 0.01
    k = 10; # TODO: tune

    pop = Population(pop_size, mutation_rate, k)

    while not pop.finished:
        pop.natural_selection()
        pop.generate_new_population()
        pop.evaluate()
        pop.print_population_status()


if __name__ == "__main__":
    main()
