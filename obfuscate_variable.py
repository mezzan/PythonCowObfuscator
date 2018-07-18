import tokenizer
from generate_replacement import generate
import token
import re


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

""" Dictionary of regex pattern """
pattern_search = { 'if_pat': '\s*if\s*\w+',
                'for_pat': '\s*for\s*\w+\s*in\s*',
                'imp_pat': '\s*import\s*\w*',
                'met_pat': '\s*\w*\(\w*\)\s*',
                'ass_pat': '\s*\w*\s*\=\s*\w*',
                'wh_pat': '\s*while\s*\w*\:',
                'with_pat': '\s*with\s*[^\s.]*\s*',
                'def_pat': '\s*def\s*\w+\s*\(\w*',
                }

""" List of variable name to ignore """
ignore_variable = ['__name__', '__main__', '__doc__', '__getattr__',
                '__setattr__', '__class__', '__bases__', '__subclasses__',
                '__init__', '__dict__', 'and', 'not', '__author__',
                '__copyright__', '__credits__', '__license__', '__version__',
                '__maintainer__', '__email__', '__status__']

""" Dictionary of variable to replace """
replacement_dic = {}

""" List of imported module """
import_list = []

def obfuscate(source):
    """
    Given the source code,it searchs for variables name and replaces them.

    :param source: Source file.
    :return: A list of lines.
    """
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        for pattern in pattern_search.values():
            match = re.search(pattern, line)
            if match:
                search_variable_to_replace(line)
    lines = replace(lines)
    return (lines, replacement_dic)

def search_variable_to_replace(line):
    """
    For each line, it searchs for variables name, creates new variables and saves them in a dictonary.

    :param line: A single line from tokenizer.tokenize_file(...).
    """
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        old = ''
        # case 1: (var) or (var,
        if token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 2: (var ) or (var ,
        elif token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ' ' and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+1][1]

        # case 3: ( var) or ( var,
        elif token_line[ind][1] == '(' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+2][1]

        # case 4: ( var ) or ( var ,
        elif token_line[ind][1] == '(' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and token_line[ind+3][1] == ' ' and (token_line[ind+4][1] == ')' or token_line[ind+4][1] == ','):
            old = token_line[ind+2][1]

        # case 5 ,var) or ,var,
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 6: , var) or , var,
        elif token_line[ind][1] == ',' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+2][1]

        # case 7: ,var ) or ,var ,
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ' ' and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+1][1]

        # case 8: , var ) or , var ,
        elif token_line[ind][1] == ',' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and token_line[ind+3][1] == ' ' and (token_line[ind+4][1] == ')' or token_line[ind+4][1] == ','):
            old = token_line[ind+2][1]

        # case 9: assignment
        elif token_line[ind][0] == token.NAME and (token_line[ind+1][1] == '=' or token_line[ind+2][1] == '='):
            old = token_line[ind][1]

        # case 10: as var :
        elif token_line[ind][1] == 'as' and ((token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ':') or token_line[ind+1][0] == token.NAME):
            old = token_line[ind+1][1]

        # case 11: for var
        elif token_line[ind][1] == 'for' and token_line[ind+1][0] == token.NAME:
            old = token_line[ind+1][1]

        # case 12: if var
        elif token_line[ind][1] == 'if' and token_line[ind+1][0] == token.NAME and not token_line[ind+2][1] == '(':
            old = token_line[ind+1][1]

        # case 13: while var
        #elif token_line[ind][1] == 'while' and token_line[ind+1][0] == token.NAME:
        #    old = token_line[ind+1][1]

        # case 14: save import module
        elif token_line[ind][1] == 'import' and token_line[ind+1][0] == token.NAME:
            import_list.append(token_line[ind+1][1])

        replace = generate()
        if old not in replacement_dic.keys() and not old == '' and replace not in replacement_dic.values():
            replacement_dic[old] = replace

def replace(lines):
    """
    For each line, it replaces the old variables name with the new ones.

    :param lines: A list of lines.
    :return: A list of modified lines.
    """
    for index, line in enumerate(lines):
        if not line == '\n':
            token_line = tokenizer.tokenize_line(line)
            for ind, token in enumerate(token_line):
                #replaced = False
                if token_line[ind][1] in replacement_dic.keys() and token_line[ind][1] not in ignore_variable:
                    if ind > 1 and token_line[ind-2][1] in import_list:
                        continue
                    token_line[ind][1] = replacement_dic.get(token_line[ind][1])
                    #replaced = True
                #if not replaced and token_line[ind][1] in replacement_dic.keys() and token_line[ind][1] not in ignore_variable:
                #    token_line[ind][1] = replacement_dic.get(token_line[ind][1])

            lines[index] = tokenizer.untokenize_line(token_line)
    return lines
