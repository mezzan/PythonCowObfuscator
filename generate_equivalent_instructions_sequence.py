import token


'''
def generete_equivalent_instructions_sequence(list_of_tokens, start):

    # get a list of tokens which represents a single instruction
    tokens = []
    end = start
    for token in list_of_tokens[start:]:
        if ( token[0] == token.NEWLINE ):
            break
        else:
            tokens.append(token)
            end += 1

    for token in tokens:
        if token[0] == token.OP:
            if (token[1] == '+'):
                # sum
                return new_sum(tokens, start, end)
            elif (token[1] == '-'):
                # sub
                return new_sub(tokens, start, end)
            elif (token[1] == '*'):
                # mult
                return new_mult(tokens, start, end)
            elif (token[1] == '/'):
                # div
                return new_div(tokens, start, end)


def new_sum(tokens, start, end):
    new_block = ''

    return ''


def new_sub(tokens, start, end):
    return ''


def new_mult(tokens, start, end):
    return ''


def new_div(tokens, start, end):
    return ''
'''


