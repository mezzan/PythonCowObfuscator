import tokenize


def tokenize_file(file_source):
    file_obj = open(file_source, 'r')
    tokens = [list(a) for a in tokenize.generate_tokens(file_obj.readline)]
    return tokens
