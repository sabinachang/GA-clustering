class ParseObject:
    def __init__(self):
        # dict of pacakge to list of nodes  
        self.structure = {}

        # dict of node to list of dependent nodes
        self.dependency = {}

        # mapping each node to a number
        self.node_to_num = {}
        self.num_to_node = {}
        
        self.ignore_path = ""
        self.valid_import_start = ""
        self.valid_file_end = ""
        self.text_repr_name = ""
        self.default_pkg = ""
        self.strct_file_path = ""

        self.output_dir_path = "./output"
    
    def set_strct_file_path(self, path):
        self.strct_file_path = path

    def set_path_to_ignore(self,path):
        self.ignore_path = path
    
    def set_valid_import_start(self, start):
        self.valid_import_start = start
    
    def set_default_pkg_name(self, pkg):
        self.default_pkg = pkg

    def set_valid_file_end(self,suffix):
        self.valid_file_end = suffix
    
    def set_text_repr_name(self,name):
        self.text_repr_name = name