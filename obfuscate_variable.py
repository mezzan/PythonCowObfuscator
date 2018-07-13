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

pattern_replace = {
'use_pat': '\s*\(\s*\w*\s*[\)\,]',
'for_pat': '\s*for\s*\w+\s*in\s*',
'as_pat' : '\s*as\s*\w*\s*:',
'ass_pat': '\s*\w*\=\s*',
'ass_pat2':'\s*\=\s*\w*',
'met_pat': '\s*\w*\.\w*'
}

pattern_replacement = [
['\s*\(\s*', '', '\s*[\)\,]'],
['\s*for\s*', '' , '\s*in\s*'],
['\s*as\s*', '', '\s*:'],
['\s*', '', '\=\s*'],
['\s*\=\s*', '' , '\s*'],
['\s*', '', '\.']
]
'use_pat': '\s*\(\s*\w*\s*[\)\,]',
'for_pat': '\s*for\s*\w+\s*in\s*',
'as_pat' : '\s*as\s*\w*\s*:',
'ass_pat': '\s*\w*\=\s*\w*',
'met_pat': '\s*\w*\.\w*'

}

replacement = {}
source = "/Users/valentina/Downloads/PythonCowObfuscator/tokenizer.py"

# add source_file
def search():
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        for p in pattern_search.keys():
            match = re.search(pattern_search.get(p), line)
            if match:
                lines[ind] = tokenize_ofbusate(line)
    #print(lines)

# come modificare la stringa per ottenere le modifiche
def tokenize_ofbusate(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        # caso 1: ( var ) or ( var ,
        if token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]
            replace = generate()
            if old not in replacement.keys() and replace not in replacement.items():
                replacement[old] = replace
        # caso 2: assignment
        elif token_line[ind][0] == token.NAME and token_line[ind+1][1] == '=':
            old = token_line[ind][1]
            replace = generate()
            if old not in replacement.keys() and replace not in replacement.items():
                replacement[old] = replace
        # caso 3: as var :
        elif token_line[ind][1] == 'as' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ':':
            old = token_line[ind+1][1]
            replace = generate()
            if old not in replacement.keys() and replace not in replacement.items():
                replacement[old] = replace
        # caso 4: import and import as
        elif token_line[ind][1] == 'import':
            print(token_line[ind][1])
            if not token_line[ind+2][1]:
                old = token_line[ind+1][1]
                replace = generate()
                if old not in replacement.keys() and replace not in replacement.items():
                    replacement[old] = replace
            else:
                old = tokenizer.tokenize_line[ind+3][1]
                replace = generate()
                if old not in replacement.keys() and replace not in replacement.items():
                    replacement[old] = replace
    #if replacement.keys():
    for word, replace in replacement.items():
        for p in pattern_replace.keys():
            line = re.sub(pattern_replace.get(p), replace, line)
            #ok = line.replace(str(word), str(replace))
    #print(line)
    return line

search()
