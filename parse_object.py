class ParseObject:
    def __init__(self,import_start, ignore_path, file_end, project_name, default_pkg):
        # dict of pacakge to list of nodes  
        self.structure = {}

        # dict of node to list of dependent nodes
        self.dependency = {}

        self.ignore_path = ignore_path

        self.valid_import_start = import_start
        self.valid_file_end = file_end
        self.project_name = project_name
        self.default_pkg = default_pkg
        self.strct_file_suffix = "_strct.txt"
        self.repr_file_suffix = "_repr.txt"