def remove_none_values(dictionary):
    return {a: b for (a, b) in dictionary.items() if b is not None}
