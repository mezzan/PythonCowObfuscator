import tokenizer
import random
import re

""" Indentation length. """
SPACE_NUM = 4
""" A set with variables name. """
vars = set()


def replace_instructions(lines):
    """
    For each line, if it is neccessary, it replaces an instruction with a sequence of instructions.

    :param lines: Result from tokenizer.tokenize_file(...).
    :return: A list of lines.
    """
    for index, line in enumerate(lines):
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
            if line_tokenized[3][1] == '+' or line_tokenized[3][1] == '-':
                lines[index] = generate_sum_sub_var_var_var(line_tokenized)
            elif line_tokenized[3][1] == '*':
                lines[index] = generate_mult_var_var_var(line_tokenized)
            elif line_tokenized[3][1] == '/':
                lines[index] = generate_div_var_var_var(line_tokenized)
        elif pattern == 1:
            # var = var + num
            # match the correct operation
            if line_tokenized[3][1] == '+' or line_tokenized[3][1] == '-':
                lines[index] = generate_sum_sub_var_var_num(line_tokenized)
            elif line_tokenized[3][1] == '*':
                lines[index] = generate_mult_var_var_num(line_tokenized)
            elif line_tokenized[3][1] == '/':
                lines[index] = generate_div_var_var_num(line_tokenized)
        elif pattern == 2:
            # var = num + var
            # match the correct operation
            if line_tokenized[3][1] == '+' or line_tokenized[3][1] == '-':
                lines[index] = generate_sum_sub_var_num_var(line_tokenized)
            elif line_tokenized[3][1] == '*':
                lines[index] = generate_mult_var_num_var(line_tokenized)
            elif line_tokenized[3][1] == '/':
                lines[index] = generate_div_var_num_var(line_tokenized)
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


def generate_sum_sub_var_var_var(tokens):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = variable [+,-] variable.
    
    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """
    # var = var {+,-} var

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get variable name
    var_name = tokens[0][1]

    # get term
    term = tokens[4][1]

    if random.randint(0, 1) == 0:
        # generate for

        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 + v2
            block = ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '-1):\n'

            block += ' ' * (indentation + SPACE_NUM)

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
            block += tokens[2][1]
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'

    else:
        # generate while
        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 {+,-} v2
            block = ' ' * indentation
            var_name_while = get_random_var()
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '-1):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
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
            block += tokens[2][1]
            block += '\n'
            var_name_while = get_random_var()
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_sum_sub_var_var_num(tokens):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = variable [+,-] integer.
    
    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """
    # var = var {+,-} num

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get variable name
    var_name = tokens[0][1]

    # get term
    term = int(tokens[4][1])

    if random.randint(0, 1) == 0:
        # generate for

        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 {+,-} num
            block = ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += str(term-1)
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

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
            block += tokens[2][1]
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += str(term)
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'

    else:
        # generate while
        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 {+,-} num
            block = ' ' * indentation
            var_name_while = get_random_var()
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term-1)
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
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
            block += tokens[2][1]
            block += '\n'
            var_name_while = get_random_var()
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term)
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + 1'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_sum_sub_var_num_var(tokens):
    """
    Generate a sequence of instructions to replace a simple sum o subtraction instruction.
    Instruction format: variable = integer [+,-] variable.
    
    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num {+,-} var
    token_temp = tokens[2]
    tokens[2] = tokens[4]
    tokens[4] = token_temp
    return generate_sum_sub_var_var_num(tokens)


def generate_mult_var_var_var(tokens):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = variable * variable.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """
    # var = var * var

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get variable name
    var_name = tokens[0][1]

    # get term
    term = tokens[4][1]

    if random.randint(0, 1) == 0:
        # generate for

        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 * v2
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '-1):\n'

            block += ' ' * (indentation + SPACE_NUM)

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

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += term
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += tokens[2][1]
            block += '\n'

    else:
        # generate while
        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 * v2
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            var_name_while = get_random_var()
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '-1):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
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
            var_name_while = get_random_var()
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += term
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += tokens[2][1]
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_mult_var_var_num(tokens):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = variable * integer.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """
    # var = var * num

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get variable name
    var_name = tokens[0][1]

    # get term
    term = int(tokens[4][1])

    if random.randint(0, 1) == 0:
        # generate for

        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 * num
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            block += 'for '

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += str(term-1)
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

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

            var_name_for = get_random_var()
            block += var_name_for

            block += ' in range(0, '
            block += str(term)
            block += '):\n'

            block += ' ' * (indentation + SPACE_NUM)

            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += tokens[2][1]
            block += '\n'

    else:
        # generate while
        if tokens[0][1] == tokens[2][1]:
            # v1 = v1 * num
            block = ' ' * indentation
            block += 'var_base = '
            block += var_name
            block += '\n'
            block += ' ' * indentation
            var_name_while = get_random_var()
            block += var_name_while
            block += '=0\n'
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term-1)
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + var_base'
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
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
            var_name_while = get_random_var()
            block += ' ' * indentation
            block += var_name_while
            block += '=0\n'
            block += ' ' * indentation
            block += 'while ('
            block += var_name_while
            block += '<'
            block += str(term)
            block += '):\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name
            block += ' = '
            block += var_name
            block += ' + '
            block += tokens[2][1]
            block += '\n'
            block += ' ' * (indentation + SPACE_NUM)
            block += var_name_while
            block += ' = '
            block += var_name_while
            block += ' + 1'
            block += '\n'

    return block


def generate_mult_var_num_var(tokens):
    """
    Generate a sequence of instructions to replace a simple multiplication instruction.
    Instruction format: variable = integer * variable.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num * var
    token_temp = tokens[2]
    tokens[2] = tokens[4]
    tokens[4] = token_temp
    return generate_mult_var_var_num(tokens)


def generate_div_var_var_var(tokens):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = variable / variable.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """
    # var1 = var2 / var3

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get var name of quotient, dividend and divisor
    quotient = tokens[0][1]
    dividend = tokens[2][1]
    divisor = tokens[4][1]

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


def generate_div_var_var_num(tokens):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = variable / integer.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions.
    """

    # get indentation
    indentation = int(tokens[0][3][0] - 1)

    # get var name of quotient, dividend and divisor
    quotient = tokens[0][1]
    dividend = tokens[2][1]
    divisor = int(tokens[4][1])

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


def generate_div_var_num_var(tokens):
    """
    Generate a sequence of instructions to replace a simple division instruction.
    Instruction format: variable = integer / variable.

    :param tokens: Iterable tokens.
    :return: A string as the new block of instructions given from a call of generate_sum_sub_var_var_num function.
    """
    # var = num + var
    token_temp = tokens[2]
    tokens[2] = tokens[4]
    tokens[4] = token_temp
    return generate_div_var_var_num(tokens)


def get_random_var():
    """
    :return: Return a fresh and random variable name.
    """
    while True:
        var = 'random_var_'
        var += str(random.randint(0,100000))
        if var not in vars:
            vars.add(var)
            return var


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
