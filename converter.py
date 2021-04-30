
def dependency_text_to_numerical(obj):
    num_dependency = {}

    for key, values in obj.dependency.items():
        key = key.replace(obj.valid_file_end, "")
        num_key = obj.node_to_num[key]
        num_dependency[num_key] = []
        for val in values:
            num_val = obj.node_to_num[val]
            num_dependency[num_key].append(num_val)
    return num_dependency


def encoding_initial_structure(obj):
    # encode initial structure of clusters into numerical representation
    encoding = [None] * len(obj.dependency)
    temp = 1
    for key, values in obj.structure.items():
        for item in values:
            encoding[obj.node_to_num[item.split('.')[0]] - 1] = temp
        temp += 1
    return encoding
