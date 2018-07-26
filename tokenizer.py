import tokenize
import io


__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"


def tokenize_line(line):
    return [list(a) for a in tokenize.generate_tokens(io.StringIO(line).readline)]


def untokenize_line(tokens):
    return tokenize.untokenize(tokens)


def tokenize_file(source_file):
    with open(source_file, 'r') as file_obj:
        return file_obj.readlines()
