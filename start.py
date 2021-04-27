import logging
import sys
from population import Population
from individual import Individual
from parse import Parser
from parse_object import ParseObject


def get_dependency(file_path, ignore_path, pkg_name, repr_name, import_start):
    obj = ParseObject()
    obj.set_strct_file_path(file_path)
    obj.set_path_to_ignore(ignore_path)
    obj.set_default_pkg_name(pkg_name)
    obj.set_valid_file_end('.java')
    obj.set_text_repr_name(repr_name)
    obj.set_valid_import_start(import_start)
    Parser(obj).parse()
    return obj.dependency


def main(dependency):
    pop_size = 200  # NEED TODO: file number
    num_nodes = 17  # NEED TODO: file number
    mutation_rate = 0.02    #TODO: tune
    # k, target number of clusters
    k = 4  # TODO: tune
    stop_generations = 1000 # TODO: tune, calculate

    pop = Population(pop_size, num_nodes, mutation_rate, k, stop_generations, dependency)

    while not pop.finished or pop.generations < stop_generations:
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
    ind1.encoding = [1, 1, 2, 1, 2, 3, 3]
    ind2.encoding = [3, 3, 1, 3, 1, 2, 2]
    ind3.encoding = [2, 2, 3, 2, 3, 1, 1]
    ind1.consistent_algorithm()
    ind2.consistent_algorithm()
    ind3.consistent_algorithm()


if __name__ == "__main__":
    # fitness_test()
    # main()
    # test_normalization()
    # dp_dependency = get_dependency('designPattern_strct.txt', 'DesignPatterns-master/src/',
    #                                '', 'designPattern_repr.txt', 'patterns')
    # print(dp_dependency)
    # main(dp_dependency)
    ex_dependency = get_dependency('easyExcel_strct.txt', 'easyexcel-master/src/main/java/',
                                   '/excel', 'easyExcel_repr.txt', 'com.alibaba')
    print(ex_dependency)
