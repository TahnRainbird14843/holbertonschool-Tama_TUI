def add_tuple(tuple1, tuple2):
    return ((tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]))

def scale_tuple(scalar, tuple1):
    return ((scalar * tuple1[0], scalar * tuple1[1]))

def tuple_in_list(tuple1, list_of_tuples):
    for tup in list_of_tuples:
        if (len(tup) == 2 and tup[0] == tuple1[0] and tup[1] == tuple1[1]):
            return True
    return False