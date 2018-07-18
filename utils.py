import random


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"


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
