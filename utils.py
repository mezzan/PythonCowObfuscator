import random


""" Indentation length. """
SPACE_NUM = 4


def get_random_var(vars_set):
    """
    :return: Return a fresh and random variable name.
    """
    while True:
        var = 'random_gen_'
        var += str(random.randint(0,100000))
        if var not in vars_set:
            return var
