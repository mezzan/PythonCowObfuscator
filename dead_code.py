import random
import tokenize

#apro il file da offuscare
source = open('source.py', "r")
output = open('output.py', 'w')

lines = source.readlines()

variable_is_inizialized = False

def insert_dead_code():
	ran = random.randint(1,15)
	dead_code = open('./dead_code/dead_code_' + str(ran) +'.py', 'r')

	output.write('\n')

	for line in dead_code.readlines():
		output.write(line)

	dead_code.close()


for line in lines:

	#verifico che line non sia una riga di commento
	if line[0] != '#':
		
		#se line è vuota e le variabili del codice morto non sono ancora state inizializzate le inizializzo
		if line == '\n' and not variable_is_inizialized:
			dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')

			output.write('\n')

			for line in dead_code_variables:
				output.write(line)
				variable_is_inizialized = True

			output.write('\n')

		elif line == '\n':

			insert_dead_code()
			output.write('\n\n')

		else:
			output.write(line)

output.write('\n')
insert_dead_code()

output.close()
source.close()