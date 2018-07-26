from random import randint


__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"


def length():
    """
    Returns a random integer used as length for the key name.
    """
    return randint(5,20)


def cap_letter():
    """
    Random generator for uppercase letter (M,O).
    """
    if randint(0,1) == 0:
        return 'M'
    else:
        return 'O'


def low_letter():
    """
    Random generator for lowercase letter (m,o).
    """
    if randint(0,1) == 0:
        return 'm'
    else:
        return 'o'


def choice_letter():
    """
    Random generator for choosing the next letter.
    """
    if randint(0,1) == 0:
        return cap_letter()
    else:
        return low_letter()


def generate():
    """
    Generates a new variable/function name.
    """
    key = ''
    for i in range(0, length()):
        key+=choice_letter()
    return key
