import tokenizer
import random
import re
import utils

""" A set with variables name. """
vars = set()


def replace_instructions(lines):
    """
    For each line, if it is neccessary, it replaces an instruction with a sequence of instructions.

    :param lines: Result from tokenizer.tokenize_file(...).
    :return: A list of lines.
    """
    for index, line in enumerate(lines):
        print("-) "+ line)
        line_tokenized = tokenizer.tokenize_line(line)
        line_to_replace = line

        # short to long
        pattern = '\w+[\+\-\*\/]=\w+'
        if re.search(pattern, line) is not None:
            line_to_replace = short_to_long(line_tokenized)
            line_tokenized = tokenizer.tokenize_line(line_to_replace)

        # match the correct pattern
        pattern = match_pattern(line_to_replace)
        if pattern == 0:
            # var = var + var
            # match the correct operation
            operators = get_operators(line_tokenized)
            if operators['op'] == '+' or operators['op'] == '-':
                lines[index] = generate_sum_sub_var_var_var(operators)
            elif operators['op'] == '*':
                lines[index] = generate_mult_var_var_var(operators)
            elif operators['op'] == '/':
                lines[index] = generate_div_var_var_var(operators)
        elif pattern == 1:
            # var = var + num
            # match the correct operation
            operators = get_operators(line_tokenized)
            if operators['op'] == '+' or operators['op'] == '-':
                lines[index] = generate_sum_sub_var_var_num(operators)
            elif operators['op'] == '*':
                lines[index] = generate_mult_var_var_num(operators)
            elif operators['op'] == '/':
                lines[index] = generate_div_var_var_num(operators)
        elif pattern == 2:
            # var = num + var
            # match the correct operation
            operators = get_operators(line_tokenized)
            if operators['op'] == '+' or operators['op'] == '-':
                lines[index] = generate_sum_sub_var_num_var(operators)
            elif operators['op'] == '*':
                lines[index] = generate_mult_var_num_var(operators)
            elif operators['op'] == '/':
                lines[index] = generate_div_var_num_var(operators)
    return lines


def match_pattern(line):
    """
    Return the corresponding pattern of instruction.
    
    :param line: The code line to categorize.
    :return: The category code.
    """
    pattern_var_var_var = '\w+\s*\=\s*\w+\s*[\+\-\*\/]\s*\w+'
    pattern_var_var_num = '\w+\s*\=\s*\w+\s*[\+\-\*\/]\s*\d+'
    pattern_var_num_var = '\w+\s*\=\s*\d+\s*[\+\-\*\/]\s*\w+'
    if (re.search(pattern_var_num_var, line)) is not None:
        return 2
    elif (re.search(pattern_var_var_num, line)) is not None:
        return 1
    elif (re.search(pattern_var_var_var, line)) is not None:
        return 0


def get_operators(tokens):
    """
    Return a dictionary with instruction operators.

    :param tokens: Tokens given from tokenizer
    :return: A dictionary
    """
    operators = {}
    for i in range(0, len(tokens)):
        if tokens[i][1] == '=':
            operators['first'] = tokens[i-1][1]
            operators['second'] = tokens[i+1][1]
            operators['third'] = tokens[i+3][1]
            operators['op'] = tokens[i+2][1]
            # TODO: indentation -1   ???
            operators['indentation'] = tokens[i-1][2][1]
            return operators
    return operators


def generate_sum_sub_var_var_var(operators):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = variable [+,-] variable.
    
    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """
    # var = var {+,-} var

    # get indentation
    indentation = operators['indentation']

    # get variable name
    var_name = operators['first']

    # get term
    term = operators['third']

    if random.randint(0, 1) == 0:
        # generate for

        if operators['first'] == operators['second']:
            # v1 = v1 + v2
            block = ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '-1):\n'

            block += ' ' * (indentation + utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 {+,-} v3
            block = ' ' * indentation
            block += var_name
            block += '='
            block += operators['second']
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'

    else:
        # generate while
        if operators['first'] == operators['second']:
            # v1 = v1 {+,-} v2
            block = ' ' * indentation
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '-1):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 {+,-} v3
            block = ' ' * indentation
            block += var_name
            block += '='
            block += operators['second']
            block += '\n'
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_sum_sub_var_var_num(operators):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = variable [+,-] integer.
    
    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """
    # var = var {+,-} num

    # get indentation
    indentation = operators['indentation']

    # get variable name
    var_name = operators['first']

    # get term
    term = int(operators['third'])

    if random.randint(0, 1) == 0:
        # generate for

        if operators['first'] == operators['second']:
            # v1 = v1 {+,-} num
            block = ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += str(term-1)
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 {+,-} num
            block = ' ' * indentation
            block += var_name
            block += '='
            block += operators['second']
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += str(term)
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'

    else:
        # generate while
        if operators['first'] == operators['second']:
            # v1 = v1 {+,-} num
            block = ' ' * indentation
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term-1)
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 {+,-} num
            block = ' ' * indentation
            block += var_name
            block += '='
            block += operators['second']
            block += '\n'
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term)
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_sum_sub_var_num_var(operators):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = integer [+,-] variable.
    
    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num {+,-} var
    temp = operators['second']
    operators['second'] = operators['third']
    operators['third'] = temp
    return generate_sum_sub_var_var_num(operators)


def generate_mult_var_var_var(operators):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = variable * variable.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """
    # var = var * var

    # get indentation
    indentation = operators['indentation']

    # get variable name
    var_name = operators['first']

    # get term
    term = operators['third']

    if random.randint(0, 1) == 0:
        # generate for

        if operators['first'] == operators['second']:
            # v1 = v1 * v2
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '-1):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
        else:
            # v1 = v2 * v3
            block = ' ' * indentation
            block += var_name
            block += '=0\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += operators['second']
            block += '\n'

    else:
        # generate while
        if operators['first'] == operators['second']:
            # v1 = v1 * v2
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '-1):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 * v3
            block = ' ' * indentation
            block += var_name
            block += '=0\n'
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += operators['second']
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_mult_var_var_num(operators):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = variable * integer.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """
    # var = var * num

    # get indentation
    indentation = operators['indentation']

    # get variable name
    var_name = operators['first']

    # get term
    term = int(operators['third'])

    if random.randint(0, 1) == 0:
        # generate for

        if operators['first'] == operators['second']:
            # v1 = v1 * num
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += str(term-1)
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
        else:
            # v1 = v2 * num
            block = ' ' * indentation
            block += var_name
            block += '=0\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = utils.get_random_var(vars)
            vars.add(var_name_for)
            block += var_name_for

            block += ' in range(0, '
            block += str(term)
            block += '):\n'

            block += ' ' * (indentation +  utils.SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += operators['second']
            block += '\n'

    else:
        # generate while
        if operators['first'] == operators['second']:
            # v1 = v1 * num
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term-1)
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'
        else:
            # v1 = v2 * num
            block = ' ' * indentation
            block += var_name
            block += '=0\n'
            var_name_while = utils.get_random_var(vars)
            vars.add(var_name_while)
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term)
            block += '):\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += operators['second']
            block += '\n'
            block += ' ' * (indentation +  utils.SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_mult_var_num_var(operators):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = integer * variable.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num * var
    temp = operators['second']
    operators['second'] = operators['third']
    operators['third'] = temp
    return generate_mult_var_var_num(operators)


def generate_div_var_var_var(operators):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = variable / variable.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """
    # var1 = var2 / var3

    # get indentation
    indentation = operators['indentation']

    # get var name of quotient, dividend and divisor
    quotient = operators['first']
    dividend = operators['second']
    divisor = operators['third']

    rand_factor = random.randint(1,1000)

    block = ' ' * indentation
    block += quotient
    block += ' = '
    block += dividend
    block += ' * '
    block += str(rand_factor)
    block += ' / '
    block += divisor
    block += ' * '
    block += str(rand_factor)
    block += '\n'

    return block


def generate_div_var_var_num(operators):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = variable / integer.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions.
    """

    # get indentation
    indentation = operators['indentation']

    # get var name of quotient, dividend and divisor
    quotient = operators['first']
    dividend = operators['second']
    divisor = int(operators['third'])

    rand_factor = random.randint(1,1000)

    divisor *= rand_factor

    block = ' ' * indentation
    block += str(quotient)
    block += ' = '
    block += dividend
    block += ' * '
    block += str(rand_factor)
    block += ' / '
    block += str(divisor)
    block += '\n'

    return block


def generate_div_var_num_var(operators):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = integer / variable.

    :param operators: A dictionary with operators.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num + var
    temp = operators['second']
    operators['second'] = operators['third']
    operators['third'] = temp
    return generate_div_var_var_num(operators)


def short_to_long(tokens):
    """
    Transform an algebraic instruction from short to long version, for example from 'v+=1' to 'v=v+1'.
    :return: A string as the new format instruction.
    """
    # from: var1 += var2
    # to: var1 = var1 + var

    var1 = tokens[0][1]
    var2 = tokens[2][1]
    op = tokens[1][1][:1]

    print(tokens)
    indentation = int(tokens[0][2][0]) - 1
    block = ' ' * indentation

    block += var1
    block += ' = '
    block += var1
    block += op
    block += var2
    block += '\n'

    return block
