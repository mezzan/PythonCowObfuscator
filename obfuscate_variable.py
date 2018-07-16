import tokenizer
from generate_replacement import generate
import token
import re

pattern_search = {
'if_pat': '\s*if\s*\w+',
'for_pat': '\s*for\s*\w+\s*in\s*',
'def_pat': '\s*def\s*\w+\s*\(\w*',
'imp_pat': '\s*import\s*\w*\s*as\s*',
'met_pat': '\s*\w*\(\w*\)\s*',
'ass_pat': '\s*\w*\=\s*\w*',
'wh_pat': '\s*while\s*\w*\:',
'with_pat': '\s*with\s*[^\s.]*\s*'
}

replacement_dic = {}
source = "/Users/valentina/Downloads/PythonCowObfuscator/obfuscate_va.py"


def obfuscate():
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        for p in pattern_search.keys():
            match = re.search(pattern_search.get(p), line)
            if match:
                search_variable_to_replace(line)
        if not line == '\n':
            lines[ind] = replace(line)
    print(lines)

def search_variable_to_replace(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        old = ''
        # case 1: ( var ) or ( var ,
        if token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 2
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 3: assignment
        elif token_line[ind][0] == token.NAME and token_line[ind+1][1] == '=':
            old = token_line[ind][1]

        # case 4: as var :
        elif token_line[ind][1] == 'as' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ':':
            old = token_line[ind+1][1]

        # case 5: import and import as TODO
        elif token_line[ind][1] == 'import':
            print(token_line[ind][1])
            if not token_line[ind+2][1]:
                old = token_line[ind+1][1]
            else:
                old = tokenize_line[ind+3][1]

        print(old)
        replace = generate()
        if old not in replacement_dic.keys() and not old == '' and replace not in replacement_dic.items():
            replacement_dic[old] = replace

def replace(line):
    token_line = tokenizer.tokenize_line(line)
    for token in token_line:
        if token[1] in replacement_dic:
            token[1] = replacement_dic.get(token[1])

    return tokenizer.untokenize_line(token_line)

obfuscate()
