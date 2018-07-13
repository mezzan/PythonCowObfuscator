import random
import tokenize
import string

list=['while', 'for', 'def', 'if']


def control(source_string):
	for x in list:
		if x in source_string:
			return True
		
	return False

def start(source_path):
	# apro il file da offuscare
	source = open(source_path, "r")
	output = open('output.py', 'w')

	lines = source.readlines()

	#variable_is_inizialized = False

	dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')

	for line in dead_code_variables:
		output.write(line)

	output.write('\n\n')

	for line in lines:

		if not '#' in line:
			if (not line[0] == ' ') and (not line[0] == '\t') and control(line):
				output.write('\n')
				insert_dead_code(output)
				output.write('\n\n' + line)
			else:
				output.write(line)
		
		'''
		# verifico che line non sia una riga di commento
		if line[0] != '#':

			# se line è vuota e le variabili del codice morto non sono ancora state inizializzate le inizializzo
			if line == '\n' and not variable_is_inizialized:
				dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')

				output.write('\n')

				for line in dead_code_variables:
					output.write(line)
					variable_is_inizialized = True

				output.write('\n')

			elif line == '\n':

				insert_dead_code(output)
				output.write('\n\n')

			else:
				output.write(line)
		'''

	output.write('\n')
	insert_dead_code(output)
	output.write('\n')

	output.close()
	source.close()

def insert_dead_code(output):
	ran = random.randint(1,15)
	dead_code = open('./dead_code/dead_code_' + str(ran) +'.py', 'r')

	output.write('\n')

	for line in dead_code.readlines():
		output.write(line)

	dead_code.close()






