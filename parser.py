import pkg_resources
from os import walk
from os.path import join
from javalang import parse
from parse_object import ParseObject

class Parser:
    def __init__(self, parse_object):
        self.po = parse_object

    def parse(self):
        packages = self.__read_pkgs_file()
            
        for package in packages:
            # package name as key
            key = package.replace(self.po.ignore_path,"",1)
            self.po.structure[key] = []

            # list of nodes in package as value. For nodes in subpackage, 
            # node name includes the subpackage path to avoid duplicate names across subpackages
            # ex: in command, one node name equals /commands/CommandHistory.java
            for root, _, files in walk(package):
                for f in files:
                    if not f.endswith(self.po.valid_file_end):
                        continue
                    node = join(root,f)
                    d = self.__get_dependencies(node)

                    node = node.replace(self.po.ignore_path,"",1)
                    self.po.dependency[node] = d
                    self.po.structure[key].append(node)

        self.__create_text_representation()
    
    def __read_pkgs_file(self):
        pkgs_file = self.po.project_name + self.po.pkgs_file_suffix
        packages = []

        with open(pkgs_file, "r") as pf:
            lines = pf.readlines()
            for l in lines:
                packages.append(l.replace("\n",""))

        return packages

    def __create_text_representation(self):
        repr_file = self.po.project_name + self.po.repr_file_suffix
        with open(repr_file, "w") as rf:
            
            for key, values in self.po.structure.items():
                rf.write(key + "\n")
                rf.write(", ".join(values))
                rf.write("\n\n")

                for v in values:
                    rf.write(v + ": ")
                    rf.write(", ".join(self.po.dependency[v])+ "\n")
                rf.write("\n\n")

    def __get_dependencies(self, node):

        source = pkg_resources.resource_string(__name__, node)
        ast = parse.parse(source)

        dependencies = []
        for imp in ast.imports:
            if not imp.path.startswith(self.po.valid_import_start):
                continue
            dependencies.append(imp.path.replace(".", "/"))

        return dependencies


if __name__ == '__main__':
    # for DesignPatterns
    obj = ParseObject('patterns', 'DesignPatterns-master/src/', '.java','designPattern', "")
    Parser(obj).parse()
