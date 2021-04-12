import random
import string
import logging
import sys

# dummy dependency for testing
# assume dependency is a global dictionary, so that Individual object do not need to copy it every time.
# to avoid redundant calculation, only consider edge connected to classes with lager index number.
dependency = {
    0: [2, 3, 10],
    1: [9, 10, 11, 13, 16],
    2: [3, 9],
    3: [7],
    4: [12],
    5: [14, 16],
    6: [8],
    7: [14],
    8: [10],
    9: [15],
    10: [13, 16],
    11: [],
    12: [],
    13: [16],
    14: [],
    15: [],
    16: []
}


class Individual:
    """
        Individual in the population
    """

    def __init__(self, size, k):
        self.k = k
        self.fitness = 0
        self.cluster = self.generate_random_cluster(size, k)

    def test(self):
        # test case of 17 classes in 5 different clusters.
        self.cluster = [1, 2, 1, 1, 4, 5, 4, 1, 4, 2, 3, 4, 5, 3, 5, 1, 3]
        self.calc_fitness()
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    # group classes by their cluster number
    def __group_by(self):
        temp = []
        for n in range(1, self.k+1):
            indices = [i for i, x in enumerate(self.cluster) if x == n]
            temp.append(indices)
        return temp

    @staticmethod
    def calc_intra_conn(cluster_):
        u = 0
        for class_ in cluster_:
            for item in dependency[class_]:
                if item in cluster_:
                    u += 1
        return u

    @staticmethod
    def calc_inter_conn(cluster_, cluster__):
        e = 0
        for class_ in cluster_:
            for item in dependency[class_]:
                if item in cluster__:
                    e += 1
        return e

    # TODO: MQ score + 1
    def calc_fitness(self):
        self.fitness = 0
        clusters = self.__group_by()
        sum_intra_conn = sum_inter_conn = 0
        # iterate all k clusters
        for i in range(0, self.k):
            cluster_ = clusters[i]
            # calculate intra-connectivity
            temp = self.calc_intra_conn(cluster_)
            logging.debug("cluster {} intra:\t{}".format(i+1, temp))
            sum_intra_conn += temp / (len(cluster_) * len(cluster_))

            # calculate inter-connectivity
            for j in range(i, self.k):
                # i = j ==> Eij = 0
                if i == j:
                    logging.debug("cluster {} {} inter:\t{}".format(i + 1, j + 1, 0))
                    continue
                # else, do calculation
                cluster__ = clusters[j]
                temp = self.calc_inter_conn(cluster_, cluster__)\
                     + self.calc_inter_conn(cluster__, cluster_)
                logging.debug("cluster {} {} inter:\t{}".format(i + 1, j + 1, temp))
                sum_inter_conn += temp/(2 * len(cluster_) * len(cluster__))
            logging.debug("")
        intra_conn = sum_intra_conn / self.k
        inter_conn = 2 * sum_inter_conn / (self.k * (self.k - 1))
        # compute MQ and normalize it to non-negative value
        self.fitness = intra_conn - inter_conn + 1
        logging.debug(self.fitness)

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

        # TODO: odd number --> return the best child
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
