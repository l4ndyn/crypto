import random

def shuffle_sequence(start, end, size):
    """
    Generate an array of tuples of integers that provides the indices to swap, so that a segment (starting at `start` (inclusive) and ending at `end` (exclusive)) of an array of size `size` becomes shuffled.
    """

    #the last element doesnt need to be swapped assuming all the ones before it have gotten swapped with an element after them
    if end == size:
        end -= 1
    
    return [(i, random.randint(i + 1, size - 1)) for i in range(start, end)]