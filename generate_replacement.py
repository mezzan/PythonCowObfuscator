from random import randint


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"


def length():
    return randint(5,20)

def cap_letter():
    if randint(0,1) == 0:
        return 'M'
    else:
        return 'O'

def low_letter():
    if randint(0,1) == 0:
        return 'm'
    else:
        return 'o'

def choice_letter():
    if randint(0,1) == 0:
        return cap_letter()
    else:
        return low_letter()

def generate():
    key = ''
    for i in range(0, length()):
        key+=choice_letter()
    return key
