import dead_code
import generate_equivalent_instructions_sequence as gen
import tokenizer
import obfuscate_variable as obf

def main():

    # 1) dead code
    source = 'esempio.py'
    dead_code.start(source)

    # 2) gen sequence
    source = 'output.py'
    with open('result.py', 'w') as res:
        for line in gen.replace_instructions(tokenizer.tokenize_file(source)):
            res.write(line)

    # 3) replace variables
    source = 'result.py'
    with open('obfuscated.py', 'w') as res:
        for line in obf.obfuscate(source):
            res.write(line)

if __name__ == '__main__':
    main()
