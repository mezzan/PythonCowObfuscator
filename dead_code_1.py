import random
import tokenize
import string

candidate_lines=['while', 'for', 'def', 'if ']

#funzione che veriifica se la riga è una riga candidata
def is_candidate(source_string):
	for line in candidate_lines:
		if line in source_string:
			return True
		
	return False

def start(source_path):
	# apro il file da offuscare
	source = open(source_path, "r")
	output = open('output.py', 'w')

	lines = source.readlines()

	dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')

	#inizializzo le variabili del codice morto
	for line in dead_code_variables:
		output.write(line)

	output.write('\n')

	#variabile che indica se sono in un blocco di commenti
	comment = False

	value = ('\t', ' ', '', '\n')

	for line in lines:

		#if line != '\n' and line != '    ':
			#Verifico se sto entrando in un blocco di commento
			if '"""' in line:
				#se il blocco non inizia e termina sulla stessa riga, allora imposto comment=True per indicare che sono entrato nel blocco,
				#la variabile comment sarà riportata a False quando verrà trovata la fine del blocco (ovvero la stringa '""""')
				if line.count('"""') != 2:
					comment = not comment
			else:
				#Se non sono in un blocco di commento
				if comment == False:
					
					#Verifico se ci sono altri commenti sulla riga
					if '#' in line:
						line = line[:line.find('#')]
						"""
						#se ho trovato commenti e ilne è una riga candidata, inserisco il codice morto 
						if (not line[0] == ' ') and (not line[0] == '\t') and is_candidate(line):
								insert_dead_code(output)
								output.write('\n' + line[:line.find('#')])
						#se line non è una riga candidata, riscrivo la riga senza commento
						else:
							#se in line[:'#'] ci sono caratteri diversi da ' ' e '\t' allora stampo la substring line[:'#']
							#altrimenti la ignoro
							if any(c not in value for c in line[:line.find('#')]):
								output.write(line[:line.find('#')] + '\n') 
						"""
					#else:
					#se non ho trovato commenti e line è una riga candidata allora inserisco il codice morto
					if line != '':	
						if (not line[0] == ' ') and (not line[0] == '\t') and is_candidate(line):
							insert_dead_code(output)
							output.write('\n' + line)
						#se line non è una riga candidata allora la riscrivo senza aggiungere niente
						else:
							if any(c not in value for c in line):
								output.write(line)

	
	#output.write('\n')
	insert_dead_code(output)

	output.close()
	source.close()

#funzione che aggiunge codice morto
def insert_dead_code(output):

	#seglie a random un file tra dead_code_.py1,...,dead_code_21.py
	ran = random.randint(1,21)
	dead_code = open('./dead_code/dead_code_' + str(ran) +'.py', 'r')

	#output.write('\n')

	#inserisce il file dead_code__x.py nel file output.py
	for line in dead_code.readlines():
		output.write(line)

	dead_code.close()