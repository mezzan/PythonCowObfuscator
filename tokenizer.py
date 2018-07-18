import tokenize
import io


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"



def tokenize_line(line):
    return [list(a) for a in tokenize.generate_tokens(io.StringIO(line).readline)]


def untokenize_line(tokens):
    return tokenize.untokenize(tokens)

# TODO: is it necessary?
def tokens_to_line(tokens):
    line = ''
    for token in tokens:
        line += str(token)
    return line


def tokenize_file(source_file):
    with open(source_file, 'r') as file_obj:
        return file_obj.readlines()


def untokenize_to_file(lines, destination_file='./out.py'):
    # TODO: check if it works
    with open(destination_file, 'w') as file_obj:
        for line in lines:
            file_obj.writable(line)