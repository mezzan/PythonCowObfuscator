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
'met_pat': ['\s*', '', '\.(\w*|\w*\_)\('],
'use_pat': ['\s*\(\s*', '', '\s*\)'],
'use_pat2': ['\s*\(\s*', '', '\s*\,'],
'for_pat': ['\s*for\s*', '', '\s*in\s*'],
'for_pat2': ['\s*in\s*', '', '\s*\:\s*'],
'as_pat' : ['\s*as\s*', '', '\s*:'],
'ass_pat': ['\s*', '', '\=\s*'],
'ass_pat2':['\s*\=\s*', '', '']
}

pattern_replacement_dic = {
'met_pat': [' ', '', '.'],
'use_pat': ['(', '', ')'],
'use_pat2': ['(', '', ','],
'for_pat': ['for ', '' , ' in '],
'for_pat2': [' in ', '', ' :'],
'as_pat' : ['as ', '', ' :'],
'ass_pat': [' ', '', '= '],
'ass_pat2': ['= ', '' , ' ']
}

replacement_dic = {}
source = "/Users/valentina/Downloads/PythonCowObfuscator/generate_equivalent_instructions_sequence.py"
#source = "/Users/valentina/Downloads/obfuscate_variable.py"
method = []

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

        elif token_line[ind][1] == '.' and token_line[ind+1][0] == token.NAME:
            method.append(token_line[ind+1][1])

        # case 5: import and import as TODO
        elif token_line[ind][1] == 'import':
            print(token_line[ind][1])
            if not token_line[ind+2][1]:
                old = token_line[ind+1][1]
            else:
<<<<<<< HEAD
                old = tokenize_line[ind+3][1]
=======
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
>>>>>>> 1d7b43646440d6bb28d1cc431f720200333a964c

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
'''
def replace(line):
    #if replacement_dic.keys():
    for word, replace in replacement_dic.items():
        print('word: ' + word + ', replace: ' + replace)
        if word in line:
            for p in pattern_replace.keys():
                #print('pattern: ' + p + '\nline :' + line)
                # modify pattern of replacement
                replacement = pattern_replacement_dic.get(p)
                replacement[1] = replace

                # modify pattern of search
                search_word = pattern_replace.get(p)
                search_word[1] = word

                # case call on a variable
                if p == 'met_pat' and re.search('\s*\w*\.(\w*|\w*\_)\(', line):
                    method = line[line.find('.')+1:line.find('(')]
                    #print('case method: ' + method)
                    replacement[2] = replacement[2] + method + '('
                    line = re.sub(''.join(search_word), ''.join(replacement), line)
                    replacement[2] = '.'
                else:
                    line = re.sub(''.join(search_word), ''.join(replacement), line)
                print('replaced: ' + line)
    return line
'''
obfuscate()
