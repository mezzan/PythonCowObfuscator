import tokenizer
import utils
import re
import random


__author__ = "Ceoletta Valentina, Zanotti Mattiva, Zenari Nicolo"
__version__ = '"1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

""" A set with varaibles random generates. """
vars = set()
""" A list with the new function definition. """
new_def = []


def replace_constants(source):
    """
    For each line, if it is neccessary, it replaces a costant with a call to a new random function.

    :param source: File path
    :return: A list of lines
    """
    lines = tokenizer.tokenize_file(source)
    lines = replace_constant_var_num(lines)
    lines = replace_constant_while(lines)
    lines = replace_constant_for(lines)

    pattern = 'import\s+\w+\s*'
    for index, line in enumerate(lines):
        if re.search(pattern, line) is None:
            break

    for block in new_def:
        lines.insert(index, block)
        index += 1

    return lines


def replace_constant_var_num(lines):
    """
    For each line, if it is neccessary, it replaces a constant assignment to a variable with a call to a new function.

    :param lines: A list of lines returned from tokenizer.tokenize_file(...)
    :return: A list of lines.
    """
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_var_num(line):
            constant = get_constant(line_tokenized)
            if constant is not None:
                if constant <= 100000000000:
                    if random.randint(0,1) == 0:
                        if is_not_prime(constant):
                            # inject factorization
                            random_function_name = utils.get_random_var(vars)
                            vars.add(random_function_name)
                            lines[index] = replace_var_constant(line_tokenized, random_function_name, constant)
                            new_def.append(generate_factorization_function(random_function_name))
                        else:
                            random_function_name = utils.get_random_var(vars)
                            vars.add(random_function_name)
                            lines[index] = replace_var_constant(line_tokenized, random_function_name, constant)
                            new_def.append(generate_ascii_function(random_function_name))
                    else:
                        random_function_name = utils.get_random_var(vars)
                        vars.add(random_function_name)
                        lines[index] = replace_var_constant(line_tokenized, random_function_name, constant)
                        new_def.append(generate_ascii_function(random_function_name))

    return lines


def is_var_num(line):
    """
    Check if the operation is var = integer.

    :param line: A single code line.
    :return: True if a line match the regex.
    """
    pattern = '\s*\w+\s*=\s*\d+'
    if re.search(pattern, line) is not None:
        return True
    return False


def get_constant(tokens):
    """
    If a single token contains a constant, return it; otherwise return None
    :param tokens: A tokenized line.
    :return: A constant or None
    """
    for token in tokens:
        if token[1].isnumeric():
            return int(token[1])
    return None


def replace_var_constant(tokens, function_name, num):
    """
    Replace the assignment operation.

    :param tokens: A tokenized line.
    :param function_name: The generated function name.
    :param num: Constant integer number.
    :return: The new line.
    """
    line = ''
    for token in tokens:
        line += token[1]
        if token[1] == '=':
            break

    line += ' ' + function_name + '(' + str(num) + ')\n'
    return line

def replace_constant_while(lines):
    """
    Replace a constant into a while statement.

    :param lines: A list of lines returned from tokenizer.tokenize_file(...)
    :return: A list of lines.
    """
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_while(line):
            constant = get_constant(line_tokenized)
            if constant is not None and constant <= 100000000000:
                # inject factorization
                random_function_name = utils.get_random_var(vars)
                vars.add(random_function_name)
                lines[index] = replace_while(line_tokenized, random_function_name)
                new_def.append(generate_factorization_function(random_function_name))

    return lines


def is_while(line):
    """
    Check if the line contain a while.

    :param line: A single code line.
    :return: True if a line match the regex.
    """
    pattern = '\s*while\s*\(\s*\w+[\<\>\!=]\w+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


def replace_constant_for(lines):
    """
    Replace a constant into a for statement.

    :param lines: A list of lines returned from tokenizer.tokenize_file(...)
    :return: A list of lines.
    """
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_for(line):
            spec = get_for_spec(line_tokenized)
            if is_a_integer(spec['end']):
                if int(spec['end']) <= 100000000000:
                    # inject factorization
                    random_function_name = utils.get_random_var(vars)
                    vars.add(random_function_name)
                    lines[index] = replace_for(line_tokenized, spec, random_function_name)
                    new_def.append(generate_factorization_function(random_function_name))

    return lines


def is_for(line):
    """
    Check if the line contain a for.

    :param line: A single code line.
    :return: True if a line match the regex.
    """
    pattern = '\s*for\s*\w+\s*in\s*range\(\d+,\d+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


# for var in range(num,num):
def get_for_spec(tokens):
    """
    Recover the for specifications.

    :param tokens: A tokenized line.
    :return: A dictionary with the specs.
    """
    spec = {}
    for i in range(0, len(tokens)):
        if tokens[i][1] == 'for':
            spec['var'] = tokens[i+1][1]
            spec['start'] = tokens[i + 5][1]
            spec['end'] = tokens[i + 7][1]
    return spec


def replace_for(tokens, spec, function_name):
    """
    Replace the for statement.

    :param tokens: A tokenized line.
    :param spec: The dictionary with the specs.
    :param function_name: The generated function name.
    :return: The new line.
    """
    line = ' ' * get_indentation(tokens, 'for')
    line += 'for ' + spec['var'] + ' in range(' + spec['start'] + ','
    line += function_name + '(' + str(spec['end']) + ')):\n'

    return line


def replace_while(tokens, function_name):
    """
    Replace the while operation.

    :param tokens: A tokenized line.
    :param function_name: The generated function name.
    :param num: Constant integer number.
    :return: The new line.
    """
    line = ' ' * get_indentation(tokens, 'while')
    line += 'while('
    spec = get_while_spec(tokens)
    line += spec['var']
    line += spec['op']
    line += function_name + '(' + str(spec['constant']) + ')):\n'

    return line


def get_while_spec_old(tokens):
    """
    Recover the while specifications.

    :param tokens: A tokenized line.
    :return: variable name and operator.
    """
    for i in range(0, len(tokens)):
        if tokens[i][1] == '(':
            return (tokens[i+1][1], tokens[i+2][1])
    return None


def get_while_spec(tokens):
    """
    Recover the while specifications.

    :param tokens: A tokenized line.
    :return: A dictionary with the specs.
    """
    spec = {}
    for i in range(0, len(tokens)):
        if tokens[i][1] == 'while':
            spec['var'] = tokens[i+1][1]
            spec['op'] = tokens[i + 2][1]
            spec['constant'] = tokens[i + 3][1]
    return spec


def get_indentation(tokens, construct):
    """
    Calculate the correct indentation.

    :param tokens: A tokenized line.
    :param construct: While o For constructor
    :return: The number of spaces.
    """
    if construct == 'while':
        for token in tokens:
            if token[1] == 'while':
                return token[2][1]
    if construct == 'for':
        for token in tokens:
            if token[1] == 'for':
                return token[2][1]
    return 0


def generate_factorization_function(function_name):
    """
    Generate a factorization function with random variable.

    :param function_name: The random function name
    :return: A code block with the function.
    """
    random_var_while = utils.get_random_var(vars)
    vars.add(random_var_while)

    random_var_par = utils.get_random_var(vars)
    vars.add(random_var_par)
    random_var_for = utils.get_random_var(vars)
    vars.add(random_var_for)

    block = 'def ' + function_name + '(' + random_var_par + '):\n'

    res = utils.get_random_var(vars)
    vars.add(res)
    block += ' ' * utils.SPACE_NUM
    block += res
    block += '=1\n'

    block += ' ' * utils.SPACE_NUM
    block += 'while ' + random_var_par + '>1:\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += 'for ' + random_var_for + ' in range(2,' + random_var_par + '+1):\n'

    block += ' ' * (utils.SPACE_NUM * 3)
    block += 'if ' + random_var_par + '%' + random_var_for + '==0:\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += random_var_par + '//=' + random_var_for + '\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += res + '*=' + random_var_for + '\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += 'break\n'

    block += ' ' * (utils.SPACE_NUM * 1)
    block += 'return ' + res + '\n'

    return block


def generate_ascii_function(function_name):
    """
    Generate a function with random variable to play with a constant.

    :param function_name: The random function name
    :return: A code block with the function.
    """
    random_var_par = utils.get_random_var(vars)
    vars.add(random_var_par)

    random_var_list = utils.get_random_var(vars)
    vars.add(random_var_list)

    block = 'def ' + function_name + '(' + random_var_par + '):\n'

    block += ' ' * utils.SPACE_NUM
    block += random_var_list + '=[]\n'

    random_var_for = utils.get_random_var(vars)
    vars.add(random_var_for)
    block += ' ' * utils.SPACE_NUM
    block += 'for ' + random_var_for + ' in str(' + random_var_par + '):\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += random_var_list + '.append(str(ord(' + random_var_for + ')))\n'

    random_var_count = utils.get_random_var(vars)
    vars.add(random_var_count)
    block += ' ' * utils.SPACE_NUM
    block += random_var_count + '=len(' + random_var_list + ')-1\n'

    random_var_res = utils.get_random_var(vars)
    vars.add(random_var_res)
    block += ' ' * utils.SPACE_NUM
    block += random_var_res + '=0\n'

    random_var_for_2 = utils.get_random_var(vars)
    vars.add(random_var_for_2)
    block += ' ' * utils.SPACE_NUM
    block += 'for ' + random_var_for_2 + ' in ' + random_var_list + ':\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += random_var_res + '+=(10**' + random_var_count + ')*int(chr(int(' + random_var_for_2 + ')))\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += random_var_count + '-=1\n'

    block += ' ' * utils.SPACE_NUM
    block += 'return ' + random_var_res + '\n'

    return block


def is_a_integer(str):
    """
    Check if str contains an integer.

    :param str: The string in which check.
    :return: True if str can be converted to int, False otherwise.
    """
    try:
        num = int(str)
        return True
    except:
        return False


def is_not_prime(n):
    """
    Check if integer n is not a prime number.

    :param n: Number to check.
    :return: True if n is not a prime, False otherwise.
    """

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2:
        return True

    # all other even numbers are not primes
    if not n & 1:
        return False

    # range starts with 3 and only needs to go up
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True
