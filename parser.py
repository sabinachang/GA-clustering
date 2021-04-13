import pkg_resources
from os import walk
from os.path import join
from javalang import parse

class Parser:
    def __init__(self, import_start, base, file_end, project_name):
        
        # dict of pacakge to list of nodes
        self.structure = {}

        # dict of node to list of dependent nodes
        self.dependency = {}

        self.base = base

        self.valid_import_start = import_start
        self.valid_file_end = file_end
        self.project_name = project_name

    def main(self):
        pkgs_file = self.project_name + "_pkgs.txt"
        packages = []

        with open(pkgs_file, "r") as pf:
            lines = pf.readlines()
            for l in lines:
                packages.append(l.replace("\n",""))
            
        for package in packages:
            # package name as key
            key = package.replace(self.base,"",1)
            self.structure[key] = []

            # list of nodes in package as value. For nodes in subpackage, 
            # node name includes the subpackage path to avoid duplicate names across subpackages
            # ex: in command, one node name equals /commands/CommandHistory.java
            for root, _, files in walk(package):
                for f in files:
                    if not f.endswith(self.valid_file_end):
                        continue
                    node = join(root,f)
                    d = self.get_dependencies(node)

                    node = node.replace(self.base,"",1)
                    self.dependency[node] = d
                    self.structure[key].append(node)

        
        repr_file = self.project_name + "_repr.txt"
        with open(repr_file, "w") as rf:
            
            for key, values in self.structure.items():
                rf.write(key + "\n")
                rf.write(", ".join(values))
                rf.write("\n\n")

                for v in values:
                    rf.write(v + ": ")
                    rf.write(", ".join(self.dependency[v])+ "\n")
                rf.write("\n\n")
    


    def get_dependencies(self, node):

        source = pkg_resources.resource_string(__name__, node)
        ast = parse.parse(source)

        dependencies = []
        for imp in ast.imports:
            if not imp.path.startswith(self.valid_import_start):
                continue
            dependencies.append(imp.path.replace(".", "/"))

        return dependencies


if __name__ == '__main__':

    # for DesignPatterns
    p = Parser('patterns', 'DesignPatterns-master/src/', '.java','designPattern')
    p.main()