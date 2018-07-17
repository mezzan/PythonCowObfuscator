import tokenizer
from generate_replacement import generate
import token
import re

replacement_dic = {}

def obfuscate(source):
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        pattern_search = '\s*def\s*\w+\s*\(\w*'
            match = re.search(pattern_search, line)
            if match:
                search_function_to_replace(line)
        if not line == '\n':
            lines[ind] = replace(line)
    return lines

def search_function_to_replace(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        old = ''

        if token_line[ind][1] == 'def' and token_line[ind+1][0] == token.NAME:
            old = token_line[ind+1][1]

        replace = generate()
        if old not in replacement_dic.keys() and not old == '' and replace not in replacement_dic.items():
            replacement_dic[old] = replace

def replace(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, token in enumerate(token_line):
        if token_line[ind][1] in replacement_dic:
            token_line[ind][1] = replacement_dic.get(token_line[ind][1])

    return tokenizer.untokenize_line(token_line)
