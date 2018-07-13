import tokenizer
import utils

vars=set()


def replace_constants(lines):
    write_to_end = set()
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        constant = get_constant(line_tokenized)
        if constant is not None:
            if constant <= 100000000:
                # inject factorization
                random_function_name = utils.get_random_var(vars)
                lines[index] = replace(line_tokenized, random_function_name, constant)
                write_to_end.add(generate_factorization_function(random_function_name))

    return (lines, write_to_end)


def get_constant(tokens):
    for token in tokens:
        try:
            i = int(token[1])
            return i
        except:
            continue
    return None


def replace(tokens, function_name, num):
    line = ''
    for token in tokens:
        line += token[1]
        if token[1] == '=':
            break

    line += ' ' + function_name + '(' + str(num) + ')'

    return line


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
















