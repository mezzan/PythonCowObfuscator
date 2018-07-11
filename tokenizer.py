import tokenize


def tokenize_file(source_file):
    file_obj = open(source_file, 'r')
    tokens = [list(a) for a in tokenize.generate_tokens(file_obj.readline)]
    file_obj.close()
    return tokens


def untokenize_to_file(tokens, destination_file='./out.py'):
    file_obj = open(destination_file)
    file_obj.write(tokenize.untokenize(tokens))
    file_obj.close()