import pkg_resources
from os import walk, makedirs
from os.path import join, isfile, split, exists
from javalang import parse
#from parse_object import ParseObject

class Parser:
    def __init__(self, parse_object):
        self.po = parse_object

    def parse(self):
        paths = self.__read_strct_file()
            
        for path in paths:
            if isfile(path):
                head_tail = split(path)
                if not head_tail[1].endswith(self.po.valid_file_end):
                    continue
                
                st = head_tail[0]+self.po.default_pkg
                #default package name as key
                key = st.replace(self.po.ignore_path,"",1)

                if not key in self.po.structure:
                    self.po.structure[key] = []
                
                self.__add_dependencies(path)
                self.__add_structure(key, path)

            else:
                # package name as key
                key = path.replace(self.po.ignore_path,"",1)
                self.po.structure[key] = []

                # list of nodes in package as value. For nodes in subpackage, 
                # node name includes the subpackage path to avoid duplicate names across subpackages
                # ex: in command, one node name equals /commands/CommandHistory.java
                for root, _, files in walk(path):
                    for f in files:
                        if not f.endswith(self.po.valid_file_end):
                            continue
                        node = join(root,f)
                        self.__add_dependencies(node) 
                        self.__add_structure(key, node)


        self.__create_text_repr_file()
    
    def __read_strct_file(self):
        pkgs_file = self.po.strct_file_path
        packages = []

        with open(pkgs_file, "r") as pf:
            lines = pf.readlines()
            for l in lines:
                packages.append(l.replace("\n",""))

        return packages

    def __create_text_repr_file(self):
        if not exists(self.po.output_dir_path):
            makedirs(self.po.output_dir_path)
        
        repr_file = join(self.po.output_dir_path,self.po.text_repr_name)
        with open(repr_file, "w") as rf:
            
            for key, values in self.po.structure.items():
                rf.write(key + "\n")
                rf.write(", ".join(values))
                rf.write("\n\n")

                for v in values:
                    rf.write(v + ": ")
                    rf.write(", ".join(self.po.dependency[v])+ "\n")
                rf.write("\n\n")

    def __add_dependencies(self, node):
        source = pkg_resources.resource_string(__name__, node)
        ast = parse.parse(source)

        dependencies = []
        for imp in ast.imports:
            if not imp.path.startswith(self.po.valid_import_start):
                continue
            dependencies.append(imp.path.replace(".", "/"))

        node = node.replace(self.po.ignore_path,"",1)
        self.po.dependency[node] = dependencies

    def __add_structure(self, key, node):
        node = node.replace(self.po.ignore_path,"",1)
        self.po.structure[key].append(node)

#if __name__ == '__main__':
    # for DesignPatterns
    # obj = ParseObject()
    # obj.set_strct_file_path('designPattern_strct.txt')
    # obj.set_path_to_ignore('DesignPatterns-master/src/')
    # obj.set_default_pkg_name('')
    # obj.set_valid_file_end('.java')
    # obj.set_text_repr_name('designPattern_repr.txt')
    # obj.set_valid_import_start('patterns')
    # Parser(obj).parse()

    # for easyExcel
    # obj = ParseObject()
    # obj.set_strct_file_path('easyExcel_strct.txt')
    # obj.set_path_to_ignore('easyexcel-master/src/main/java/')
    # obj.set_default_pkg_name('/excel')
    # obj.set_valid_file_end('.java')
    # obj.set_text_repr_name('easyExcel_repr.txt')
    # obj.set_valid_import_start('com.alibaba')
    # Parser(obj).parse()