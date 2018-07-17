import random
import re
candidate_lines = ['while', 'for', 'def', 'if ']


# funzione che veriifica se la riga è una riga candidata
def is_candidate(source_string):
    for line in candidate_lines:
        if line in source_string:
            return True

    return False


def start(source_path):
    # apro il file da offuscare
    source = open(source_path, "r")
    output = open('output.py', 'w')

    # TODO: si può usare tokenizer_tokenize_file(source) ? (nicolò)
    lines = source.readlines()

    # === AGGIUNTO ===
    imports = get_imports(lines)
    for imp in list(imports):
        output.write(imp)
    output.write('\n')
    # === FINE AGGIUNTO ===

    dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')

    # inizializzo le variabili del codice morto
    for line in dead_code_variables:
        output.write(line)

    output.write('\n')

    # variabile che indica se sono in un blocco di commenti
    comment = False

    value = ('\t', ' ', '', '\n')

    for line in lines:

        # Verifico se sto entrando in un blocco di commento
        if '"""' in line:
            # se il blocco non inizia e termina sulla stessa riga, allora imposto comment=True per indicare che sono entrato nel blocco,
            # la variabile comment sarà riportata a False quando verrà trovata la fine del blocco (ovvero la stringa '""""')
            if line.count('"""') != 2:
                comment = not comment
        else:
            # Se non sono in un blocco di commento
            if comment == False:

                # verifico se ci sono commenti sulla riga, e in tal caso prendo solo la parte di stringa che lo precede
                if '#' in line:
                    line = line[:line.find('#')]

                # verifico che line non sia vuota
                if line != '':
                    # verifico che line non inizi con spazi o tabulazioni (ovvero non sia nello scope di un costrutto)
                    if (not line[0] == ' ') and (not line[0] == '\t') and is_candidate(line):

                        # inserisco il codice morto
                        insert_dead_code(output)
                        output.write('\n' + line)

                    # se sono nello scope di un costrutto oppure line non è una riga candidata
                    else:

                        # verifico che line non sia fatta solo da spazi e tabulazioni
                        if any(c not in value for c in line):
                            # scrivo la line in output
                            output.write(line)

    insert_dead_code(output)

    output.close()
    source.close()


# funzione che aggiunge codice morto
def insert_dead_code(output):
    # seglie a random un file tra dead_code_.py1,...,dead_code_21.py
    ran = random.randint(1, 21)
    dead_code = open('./dead_code/dead_code_' + str(ran) + '.py', 'r')

    # inserisce il file dead_code_x.py nel file output.py
    for line in dead_code.readlines():
        output.write(line)

    dead_code.close()


# (AGGIUNTO) Metodo che ritorna gli import da scrivere all'inizio del file
def get_imports(lines):
    pattern = 'import\s+\w+'
    imports = set()
    for index, line in enumerate(lines):
        if re.search(pattern, line) is not None:
            imports.add(line)
            lines[index] = ''
    return imports
