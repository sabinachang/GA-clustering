import logging
import sys
from population import Population
from individual import Individual
from parse import Parser
from parse_object import ParseObject
from converter import dependency_text_to_numerical, encoding_initial_structure
import time


def get_parsed_object(file_path, ignore_path, pkg_name, repr_name, import_start):
    obj = ParseObject()
    obj.set_strct_file_path(file_path)
    obj.set_path_to_ignore(ignore_path)
    obj.set_default_pkg_name(pkg_name)
    obj.set_valid_file_end('.java')
    obj.set_text_repr_name(repr_name)
    obj.set_valid_import_start(import_start)
    Parser(obj).parse()
    return obj


def print_init_structure(obj):
    ind = Individual(len(obj.dependency), 1)
    ind.encoding = encoding_initial_structure(obj)
    ind.k = ind.encoding[-1]
    ind.calc_fitness(num_dep)
    print(">>{}: before->modularization {}".format(sys.argv[1], ind.fitness))
    for key, value in obj.structure.items():
        print(">>{}:".format(key))
        for node in value:
            print(">>\t\t\t{}".format(node))


def print_best_structure(obj, best_ind):
    num_to_node = {v: k for k, v in obj.node_to_num.items()}
    print(">>{}: after->modularization {}".format(sys.argv[1], best_ind.fitness))
    for i in range(1, best_ind.k + 1):
        print(">>cluster {}:".format(i))
        for j in range(0, len(best_ind.encoding)):
            if best_ind.encoding[j] == i:
                print(">>\t\t\t{}".format(num_to_node[j + 1]))


def run_GA(dependency, k=23):
    num_nodes = len(dependency)
    pop_size = num_nodes * 10  # TODO: tune
    stop_generations = 500 # num_nodes * 200
    mutation_rate = 0.01  # TODO: tune
    # k, target number of clusters
    # k = 23  # TODO: tune

    print("GA Settings:")
    print(
        "N: {}, population size: {}, mutation rate: {}, cluster size: {}".format(num_nodes, pop_size, mutation_rate, k))

    pop = Population(pop_size, num_nodes, mutation_rate, k, stop_generations, dependency)
    start = time.time()
    while not pop.finished or pop.generations < stop_generations:
        pop.natural_selection()
        pop.generate_new_population()
        if pop.generations % 10 == 0:
            pop.evaluate()
            pop.print_population_status()
    end = time.time()
    print(end - start)
    return pop.overall_best_ind, pop.overall_max_fitness


def fitness_test():
    # output setting for debug mode
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ind = Individual(17, 5)
    ind.test()


def test_normalization():
    ind1, ind2, ind3 = Individual(7, 3), Individual(7, 3), Individual(7, 3)
    ind1.encoding = [1, 1, 2, 1, 2, 3, 3]
    ind2.encoding = [3, 3, 1, 3, 1, 2, 2]
    ind3.encoding = [2, 2, 3, 2, 3, 1, 1]
    ind1.consistent_algorithm()
    ind2.consistent_algorithm()
    ind3.consistent_algorithm()


if __name__ == "__main__":
    # fitness_test()
    # test_normalization()
    if len(sys.argv) != 2:
        print('ERROR: Please input the source code path in the argument!\n'
              'EX: easyexcel-master or DesignPatterns-master')
    else:
        if sys.argv[1].lower() == 'easyexcel-master':
            obj = get_parsed_object('easyExcel_strct.txt', 'easyexcel-master/src/main/java/',
                                    '/excel', 'easyExcel_repr.txt', 'com.alibaba')
            obj.num_to_node = {v: k for k, v in obj.node_to_num.items()}
            num_dep = dependency_text_to_numerical(obj)

            print_init_structure(obj)

            run_GA(num_dep)

            best_ind, best_fitness = run_GA(num_dep)

            print_best_structure(obj, best_ind)

        elif sys.argv[1].lower() == 'designpatterns-master':
            obj = get_parsed_object('designPattern_strct.txt', 'DesignPatterns-master/src/',
                                    '', 'designPattern_repr.txt', 'patterns')
            num_dep = dependency_text_to_numerical(obj)

            print_init_structure(obj)

            best_fitness = 0.0
            best_ind = None
            for k in range(15, 25):
                ind, fitness  = run_GA(num_dep, k)
                if fitness > best_fitness:
                    best_ind = ind
                    best_fitness = fitness

            print_best_structure(obj, best_ind)

        else:
            print('ERROR: Please input a valid source code path!\n'
                  'EX: easyexcel-master or DesignPatterns-master')
