import tokenizer
from generate_variable import generate
import token
import re

pattern ={
'if_pat': '\s*if\s*\w+',
'for_pat': '\s*for\s*\w+\s*in\s*',
'def_pat': '\s*def\s*\w+\s*\(\w*',
'imp_pat': '\s*import\s*\w*\s*as\s*',
'met_pat': '\s*\w*\(\w*\)\s*',
'ass_pat': '\s*\w*\=\s*\w*',
'wh_pat': '\s*while\s*\w*\:',
'with_pat': '\s*with\s*[^\s.]*\s*'}

construct = ['for', 'in', 'with', 'as', 'while', 'def', 'import', '=', 'if', 'return', ]
replacement = {}

# add source_file
def search():
    tokens = tokenizer.tokenize_file(source)
    for ind, token in enumerate(tokens):
        for p in pattern.keys():
            match = re.search(pattern.get(i), token)
            if match:
                tokens[ind] = tokenize_ofbusate(token)

# come modificare la stringa per ottenere le modifiche
def tokenize_ofbusate(token):
    token_line = tokenize_line(token)
    for ind, tok in token_line:
        if token_line[ind][0] == token.OP and token_line[ind+1][0] == token.NAME and token_line[ind+2][0] == token.OP: # (_) or (_,
            old = token_line[ind+1][1]
            if old not in replacement.keys():
                replace = generate()
                token_line[ind+1][1] = replace
                replacement[old] = replace
        elif token_line[ind][0] == token.NAME and token_line[ind+1][0] == token.NAME: # _ =
            old = token_line[ind][1]
            if old not in replacement.keys():
                replace = generate()
                token_line[ind][1] = replacement
                replacement[old] = replacement
        elif token_line[ind][0] == token.NAME and token_line[ind+1][0] == token.NAME and token_line[ind+2][0] == token.OP: # as _ :
            old = token_line[ind+1][1]
            if old not in replacement.keys():
                replace = generate()
                token_line[ind+1][1] = replacement
                replacement[old] = replacement
        elif token_line[ind][0] == token.NAME and token_line[ind+1][0] == token.NAME and token_line[ind+2][0] == token.NAME and token_line[ind+3][0] == token.NAME and token_line[ind+4][0] == token.OP:
            old = token_line[ind+1][1]
            if old not in replacement.keys():
                replace = generate()
                token_line[ind+1][1] = replacement
                replacement[old] = replacement
            old = token_line[ind+3][1]
            if old not in replacement.keys():
                replace = generate()
                token_line[ind+3][1] = replacement
                replacement[old] = replacement
        return tokenizer.untokenize_line(token_line)
