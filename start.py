import logging
import sys
from population import Population
from individual import Individual
from parse import Parser
from parse_object import ParseObject
from converter import dependency_text_to_numerical



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


def run_GA(dependency):
    num_nodes = len(dependency)
    pop_size = num_nodes * 10   # TODO: tune
    stop_generations = num_nodes * 200
    mutation_rate = 0.02    # TODO: tune
    # k, target number of clusters
    k = 4  # TODO: tune

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
    # test_normalization()
    if len(sys.argv) != 2:
        print('ERROR: Please input the source code path in the argument!\n'
              'EX: easyexcel-master or DesignPatterns-master')
    else:
        if sys.argv[1].lower() == 'easyexcel-master':
            obj = get_parsed_object('easyExcel_strct.txt', 'easyexcel-master/src/main/java/',
                                                    '/excel', 'easyExcel_repr.txt', 'com.alibaba')
            num_dep = dependency_text_to_numerical(obj)
            run_GA(num_dep)
            # TODO: show_result

        elif sys.argv[1].lower() == 'designpatterns-master':
            obj = get_parsed_object('designPattern_strct.txt', 'DesignPatterns-master/src/',
                                                    '', 'designPattern_repr.txt', 'patterns')

            num_dep = dependency_text_to_numerical(obj)
            run_GA(num_dep)
            # TODO: show_result()
        else:
            print('ERROR: Please input a valid source code path!\n'
                  'EX: easyexcel-master or DesignPatterns-master')


