def get_number_of_xtiles_at_level(level):
    return 1 << level

def get_number_of_ytiles_at_level(level):
    return 1 << level

def reverse_y_tag(y, level):
    return get_number_of_ytiles_at_level(level) - y - 1