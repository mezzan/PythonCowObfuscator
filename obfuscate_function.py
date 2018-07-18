import tokenizer
from generate_replacement import generate
import token
import re


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

""" Dictionary of function to replace """
replacement_dic = {}

""" Dictionary of variable to replace """
variable_dic = {}

def obfuscate(source,dictonary):
    """
    Given the source code and the variable dictonary,it searchs for function name and replaces them.

    :param source,dictionary: Source file and variable dictionary.
    :return: A list of lines.
    """
    variable_dic = dictonary
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        pattern_search = '\s*def\s*\w+\s*\(\w*'
        match = re.search(pattern_search, line)
        if match:
            search_function_to_replace(line)
    lines = replace(lines)
    return lines

def search_function_to_replace(line):
    """
    For each line, it searchs for function name, creates new variables and saves them in a dictonary.

    :param line: A single line from tokenizer.tokenize_file(...).
    """
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        old = ''

        if token_line[ind][1] == 'def' and token_line[ind+1][0] == token.NAME:
            old = token_line[ind+1][1]

        if old not in replacement_dic.keys() and not old == '':
            replace = generate()
            while replace not in variable_dic.values() or replace in replacement_dic.values():
                replace = generate()
            replacement_dic[old] = replace

def replace(lines):
    """
    For each line, it replaces the old functions name with the new ones.

    :param lines: A list of lines.
    :return: A list of modified lines.
    """
    for index, line in enumerate(lines):
        if not line == '\n':
            token_line = tokenizer.tokenize_line(line)
            for ind, token in enumerate(token_line):
                if token_line[ind][1] in replacement_dic.keys():
                    token_line[ind][1] = replacement_dic.get(token_line[ind][1])

            lines[index] = tokenizer.untokenize_line(token_line)
    return lines
