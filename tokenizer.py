import tokenize
import io


def tokenize_line(line):
    return [list(a) for a in tokenize.generate_tokens(io.StringIO(line).readline())]


def untokenize_line(tokens):
    return tokenize.untokenize(tokens)


def tokenize_file(source_file):
    with open(source_file, 'r') as file_obj:
        return file_obj.readlines()


def untokenize_to_file(lines, destination_file='./out.py'):
    # TODO: check if it works
    with open(destination_file, 'w') as file_obj:
        for line in lines:
            file_obj.writable(line)