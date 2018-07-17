import tokenizer
import utils
import re


vars=set()
write_to_end = set()


def replace_constant_var_num(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        constant = get_constant(line_tokenized)
        if constant is not None:
            if constant <= 100000000000:
                # inject factorization
                random_function_name = utils.get_random_var(vars)
                lines[index] = replace(line_tokenized, random_function_name, constant)
                write_to_end.add(generate_factorization_function(random_function_name))

    return (lines, write_to_end)


def replace_constant_while(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_while(line):
            constant = get_constant(line_tokenized)
            if constant <= 100000000000:
                # inject factorization
                random_function_name = utils.get_random_var(vars)
                lines[index] = replace_while(line_tokenized, random_function_name, constant)
                write_to_end.add(generate_factorization_function(random_function_name))

    return (lines, write_to_end)


def is_while(line):
    pattern = '\s*while\s*\(\s*\w+[\<\>\!=]\w+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


def get_constant(tokens):
    for token in tokens:
        try:
            i = int(token[1])
            return i
        except:
            continue
    return None


def replace_constant_for(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_for(line):
            spec = get_for_spec(line_tokenized)
            for k in spec.keys():
                print(spec[k])
            if is_a_integer(spec['end']):
                print('ok1')
                if int(spec['end']) <= 100000000000:
                    # inject factorization
                    print('ok2')
                    random_function_name = utils.get_random_var(vars)
                    lines[index] = replace_for(line_tokenized, spec, random_function_name)
                    write_to_end.add(generate_factorization_function(random_function_name))

    return (lines, write_to_end)


def is_for(line):
    pattern = '\s*for\s*\w+\s*in\s*range\(\d+,\d+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


# for var in range(num,num):
def get_for_spec(tokens):
    spec = {}
    for i in range(0, len(tokens)):
        if tokens[i][1] == 'for':
            spec['var'] = tokens[i+1][1]
            spec['start'] = tokens[i + 5][1]
            spec['end'] = tokens[i + 7][1]
    return spec


def replace_for(tokens, spec, function_name):
    line = ' ' * get_indentation(tokens, 'for')
    line += 'for ' + spec['var'] + ' in range(' + spec['start'] + ','
    line += function_name + '(' + str(spec['end']) + ')):\n'

    return line


def replace(tokens, function_name, num):
    line = ''
    for token in tokens:
        line += token[1]
        if token[1] == '=':
            break

    line += ' ' + function_name + '(' + str(num) + ')'

    return line


def replace_while(tokens, function_name, num):
    line = ' ' * get_indentation(tokens, 'while')
    line += 'while('
    var_name, op = get_while_spec(tokens)
    line += var_name
    line += op
    line += function_name + '(' + str(num) + ')):\n'

    return line


def get_indentation(tokens, construct):
    if construct == 'while':
        for token in tokens:
            if token[1] == 'while':
                return token[2][1]
    if construct == 'for':
        for token in tokens:
            if token[1] == 'for':
                return token[2][1]
    return 0


def get_while_spec(tokens):
    for i in range(0, len(tokens)):
        if tokens[i][1] == '(':
            return (tokens[i+1][1], tokens[i+2][1])
    return None


def generate_factorization_function(function_name):
    random_var_while = utils.get_random_var(vars)
    vars.add(random_var_while)

    block = 'def ' + function_name + '(n):\n'

    block += ' ' * utils.SPACE_NUM
    block += random_var_while
    block += '=2\n'

    res = utils.get_random_var(vars)
    vars.add(res)
    block += ' ' * utils.SPACE_NUM
    block += res
    block += '=1\n'

    block += ' ' * utils.SPACE_NUM
    block += 'while ' + random_var_while + '*' + random_var_while + '<=n:\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += 'while n%' + random_var_while + '==0:\n'

    block += ' ' * (utils.SPACE_NUM * 3)
    block += res + '*=' + random_var_while + '\n'

    block += ' ' * (utils.SPACE_NUM * 3)
    block += 'n' + '//=' + random_var_while + '\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += random_var_while + '+=1\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += 'if n>1:\n'

    block += ' ' * (utils.SPACE_NUM * 3)
    block += res + '*=n\n'

    block += ' ' * (utils.SPACE_NUM * 1)
    block += 'return ' + res + '\n'

    return block


def is_a_integer(str):
    try:
        num = int(str)
        return True
    except:
        return False












