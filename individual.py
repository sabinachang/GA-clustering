import random
import string


class Individual:
    """
        Individual in the population
    """

    def __init__(self, size, k):
        self.k = k
        self.fitness = 0
        self.cluster = self.generate_random_cluster(size, k)

    # TODO: MQ score + 1
    def calc_fitness(self):
        self.fitness = None


        self.fitness += 1

    def __repr__(self):
        return ''.join(self.genes) + " -> fitness: " + str(self.fitness)

    @staticmethod
    def generate_random_cluster(size, k):
        cluster = []

        for i in range(size):
            cluster.append(random.randint(1, k))

        return cluster

    # The crossover function selects pairs of individuals to be mated, generating a third individual (child)
    def crossover(self, partner):
        ind_len = len(self.cluster)
        child = Individual(ind_len, self.k)
        child.cluster = []
        # half and half crossover
        child.cluster = self.cluster[:ind_len // 2] + partner.cluster[ind_len // 2:]

        # TODO: odd number --> return best child
        if ind_len % 2 != 0:
            child.calc_fitness()
            child2 = Individual(ind_len, self.k)
            child2.cluster = []
            child2.cluster = self.cluster[:ind_len // 2 + 1] + partner.cluster[ind_len // 2 + 1:]
            child2.calc_fitness()
            child = child2 if (child.fitness < child2.fitness) else child

        return child

    # Mutation: based on a mutation probability, the function picks a new random character and replace a gene with it
    def mutate(self, mutation_rate):
        # code to mutate the individual here
        ind_len = len(self.cluster)
        p = random.random()
        if p < mutation_rate:
            random_ind = random.randint(0, ind_len - 1)
            self.cluster[random_ind] = random.randint(1, self.k)
