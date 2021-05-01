import random
import string
import logging
import sys
import numpy as np
import pandas as pd

# dummy dependency for testing revs.user_stars_mean * revs.user_review_num
# assume dependency is a global dictionary, so that Individual object do not need to copy it every time.
# to avoid redundant calculation, only consider edge connected to classes with lager index number.
# dependency = {
#     0: [2, 3, 10],
#     1: [9, 10, 11, 13, 16],
#     2: [3, 9],
#     3: [7],
#     4: [12],
#     5: [14, 16],
#     6: [8],
#     7: [14],
#     8: [10],
#     9: [15],
#     10: [13, 16],
#     11: [],
#     12: [],
#     13: [16],
#     14: [],
#     15: [],
#     16: []
# }

test_dependency = {
    0: [1, 2, 3],
    1: [0, 2, 3],
    2: [0, 1, 3],
    3: [0, 1, 2],
    4: [5, 6, 7],
    5: [4, 6, 7],
    6: [4, 5, 7],
    7: [4, 5, 6],
    8: [9, 10, 11],
    9: [8, 10, 11],
    10: [8, 9, 11],
    11: [8, 9, 10],
    12: [13, 14, 15, 16],
    13: [12, 14, 15, 16],
    14: [12, 13, 15, 16],
    15: [12, 13, 14, 16],
    16: [12, 13, 14, 15]
}


class Individual:
    """
        Individual in the population
    """

    def __init__(self, size, k, defaultEncoding=False):
        self.k = k
        self.num_nodes = size
        self.fitness = 0
        if defaultEncoding == True:
            self.encoding = [None] * size
        else:
            self.encoding = self.generate_random_cluster(size, k)
        self.consistent_algorithm()

    # # group classes by their cluster number
    # def __group_by(self):
    #     temp = []
    #     for n in range(1, self.k+1):
    #         indices = [i for i, x in enumerate(self.cluster) if x == n]
    #         temp.append(indices)
    #     return temp

    @staticmethod
    def calc_intra_conn(cluster_, dependency):
        u = 0
        for class_ in cluster_:
            for item in dependency[class_]:
                if item in cluster_:
                    u += 1
        if u == 0:
            return 0
        ni = len(cluster_)
        return u / (ni ** 2)

    @staticmethod
    def calc_inter_conn(cluster_i, cluster_j, dependency):
        e = 0
        for node_i in cluster_i:
            for item in dependency[node_i]:
                if item in cluster_j:
                    e += 1
        if e == 0:
            return 0
        return (e * 0.5) / len(cluster_i) / len(cluster_i)

    @staticmethod
    def calc_intra_conn2(cluster_, dependency):
        u = 0
        x = set(cluster_)
        for class_ in cluster_:
            y = set(dependency[class_])
            intersection = x & y  # or, equivalently
            # common_elements = train_set.intersection(test_set)
            u += len(intersection)
        if u == 0:
            return 0
        ni = len(cluster_)
        return u / (ni ** 2)

    @staticmethod
    def calc_inter_conn2(cluster_i, cluster_j, dependency):
        e = 0
        for node_i in cluster_i:
            x = set(dependency[node_i])
            y = set(cluster_j)
            intersection = x & y  # or, equivalently
            e += len(intersection)
        if e == 0:
            return 0
        return (e * 0.5) / len(cluster_i) / len(cluster_i)

    # NEW TODO: global dependency?
    def calc_fitness(self, dependency):
        self.fitness = 0
        clusters = pd.Series(range(1, self.num_nodes + 1)).groupby(self.encoding).apply(list).tolist()
        # logging.debug("Grouped encoding into {} clusters; target cluster size: {}".format(len(clusters), self.k))
        actual_k = len(clusters)

        total_intra_conn = 0
        total_inter_conn = 0

        for curr_cluster in clusters:
            intra_score = self.calc_intra_conn2(curr_cluster, dependency)
            # logging.debug("cluster intra:\t{}".format(intra_score))
            total_intra_conn += intra_score

        for i in range(actual_k - 1):
            for j in range(i + 1, actual_k):
                inter_score = self.calc_inter_conn2(clusters[i], clusters[j], dependency)
                total_inter_conn += inter_score
                # logging.debug("cluster {} {} inter:\t{}".format(i + 1, j + 1, inter_score))

        if total_intra_conn > 0:
            total_intra_conn /= actual_k
        if total_inter_conn > 0:
            total_inter_conn /= (0.5 * actual_k * (actual_k - 1))

        mq = total_intra_conn - total_inter_conn
        # normalize MQ to non-negative value for wheel selection easiness
        self.fitness = mq + 1
        # logging.debug("fitness score: {}".format(self.fitness))

    def __repr__(self):
        return "fitness: " + str(self.fitness) + " -> " + ''.join([str(i) for i in self.encoding])

    '''
    This randomly generates an individual with the given size(i.e. number of nodes),
    in k clusters.
    '''

    @staticmethod
    def generate_random_cluster(size, k):
        cluster = []
        for i in range(size):
            cluster.append(random.randint(1, k))
        return cluster

    '''
    normalization algorithm 
    '''
    def consistent_algorithm(self):
        S = np.zeros(len(self.encoding))
        label = 1
        for i in range(len(S)):
            if S[i] == 0:
                aux = self.encoding[i]
                for j in range(len(S)):
                    if self.encoding[j] == aux and S[j] == 0:
                        self.encoding[j] = label
                        S[j] = 1
                label += 1

    '''
    This normalize the individual encoding
    '''
    def normalize_encoding(self):
        lowest_unused_code = 1
        encoding_conversion_map = {}
        for assignment in self.encoding:
            if assignment not in encoding_conversion_map.keys():
                encoding_conversion_map[assignment] = lowest_unused_code
                lowest_unused_code += 1
            else:
                continue
        self.encoding = [encoding_conversion_map[old_code] for old_code in self.encoding]

    '''
    The crossover function selects pairs of individuals to be mated, 
    generating a third individual (child)
    '''

    def crossover(self, partner):
        ind_len = len(self.encoding)
        child = Individual(ind_len, self.k)
        child.encoding = []
        # half and half crossover
        child.encoding = self.encoding[:ind_len // 2] + partner.encoding[ind_len // 2:]

        # TODO: odd number --> return the best child
        # NEW TODO: modify? not calculate and compare here, compare in population
        # if ind_len % 2 != 0:
        #     child.calc_fitness()
        #     child2 = Individual(ind_len, self.k)
        #     child2.encoding = []
        #     child2.encoding = self.encoding[:ind_len // 2 + 1] + partner.encoding[ind_len // 2 + 1:]
        #     child2.calc_fitness()
        #     child = child2 if (child.fitness < child2.fitness) else child

        return child

    '''
    Another crossover function
    Randomly pick up the crossover point and generate two children
    '''

    def crossover2(self, partner):
        ind_len = len(self.encoding)
        child1, child2 = Individual(ind_len, self.k, True), Individual(ind_len, self.k, True)
        child1.encoding, child2.encoding = [], []
        crossPoint = random.randint(0, ind_len - 1)
        child1.encoding = self.encoding[:crossPoint] + partner.encoding[crossPoint:]
        child2.encoding = partner.encoding[:crossPoint] + self.encoding[crossPoint:]

        return child1, child2

    '''
    Another crossover function
    Partially retain cluster structure of parents
    '''
    def crossover3(self, partner):
        clusters1 = pd.Series(range(1, self.num_nodes + 1)).groupby(self.encoding).apply(list).tolist()
        clusters2 = pd.Series(range(1, self.num_nodes + 1)).groupby(partner.encoding).apply(list).tolist()

        child = Individual(self.num_nodes, self.k, True)
        new_cluster_count = 1
        while len(clusters1) > 0 or len(clusters2) > 0:
            if len(clusters1) > 0 and len(clusters2) > 0:
                which_parent = random.randint(1, 2)
                swapped = False
                if which_parent == 2:
                    swapped = True
                    tmp = clusters1
                    clusters1 = clusters2
                    clusters2 = tmp
            elif len(clusters2) > 0:
                clusters1 = clusters2

            if len(clusters1) > 1:
                cluster_opt = random.randint(0, len(clusters1) - 1)
            else:
                cluster_opt = 0
            selected_genes = clusters1[cluster_opt]
            # print(selected_genes)
            for gene in selected_genes:
                child.encoding[gene-1] = new_cluster_count
            for j in range(len(clusters2)-1, -1):
                cluster = clusters2[j]
                for i in range(len(cluster) - 1, -1):
                    if cluster[i] in selected_genes:
                        del cluster[i]
                if len(cluster) == 0:
                    del clusters2[j]
                else:
                    clusters2[j] = cluster

            # print("before: {}".format(len(clusters1)))
            del clusters1[cluster_opt]
            # print("after: {}".format(len(clusters1)))
            new_cluster_count += 1
            if new_cluster_count > self.k:
                break
            if swapped == True:
                tmp = clusters1
                clusters1 = clusters2
                clusters2 = tmp

        remaining_genes = []
        # print("{},After selecting: {}".format(new_cluster_count, len(clusters1)))
        for cluster in clusters1:
            if new_cluster_count > self.k:
                for idx in cluster:
                    child.encoding[idx - 1] = self.k
                continue
            else:
                for idx in cluster:
                    child.encoding[idx - 1] = new_cluster_count
                new_cluster_count += 1

        # print("{}, After selecting 2: {}".format(new_cluster_count, len(clusters2)))
        for cluster in clusters2:
            if new_cluster_count > self.k:
                for idx in cluster:
                    child.encoding[idx - 1] = self.k
                continue
            else:
                for idx in cluster:
                    child.encoding[idx - 1] = new_cluster_count
                new_cluster_count += 1

        # print(child)
        return child

    '''
    Mutation: based on a mutation probability, 
    the function picks a new random character and replace a gene with it
    '''
    def mutate(self, mutation_rate):
        # code to mutate the individual here
        p = random.uniform(0, 1)
        if p < mutation_rate:
            random_ind = random.randint(0, self.num_nodes - 1)
            self.encoding[random_ind] = random.randint(1, self.k)
        # for i in range(self.num_nodes):
        #     if random.uniform(0, 1) < mutation_rate:
        #         self.encoding[i] = random.randint(1, self.k)

    '''
    This tests the fitness function 
    '''
    def test(self):
        # test case of 17 classes in 5 different clusters.
        self.encoding = [1, 2, 1, 1, 4, 5, 4, 1, 4, 2, 3, 4, 5, 3, 5, 1, 3]
        self.calc_fitness()
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
