import yaml
from console import Console, str_to_array

# IMPORTANTE: no lugar de definir as palavras no xml, definir palavras padrão e só definir o que cada uma fará em todos os 

# concatenar comandos expecificos com os de configuração como 'sair'

# customizar futuro vocabulario de erro deixando ele como uma var static ou talvez deixarndo clusula no storyboard?	

WRITE_KEYWORD = 'write'
GOTO_KEYWORD = 'goto'
# DESCRIPTION = 'description'

def load_yaml(file):
	with open(file, 'r', encoding = 'utf-8') as file:
		return file.read().replace("\t", ' ')

class Parser:
	def __init__(self, yaml_path):
		text = load_yaml(yaml_path)
		self.yaml_obj = yaml.load(text)
	
	def start(self):
		""" Init the engine """
		self.prev_sec = 'main'
		self._load_default_actions()
		self._load_section(self.prev_sec)
	
	def _load_default_actions(self):
		self._actions = self.yaml_obj['actions']
		
	def _load_section(self, str_section):
		str_description = self.yaml_obj[str_section]['description']
		# Console.writedln(str_description.rstrip())
		
		self._load_actions(str_section)
		self.prev_sec = str_section

	def _execute_action(self, command, param):
		if command == WRITE_KEYWORD:
			Console.writeln(param)
		elif command == GOTO_KEYWORD:
			print("?")
			bool_ressult = self._load_section(param)
		
	def _parse_action(self, user_args, section, action):
		""" Return the command given and the param """
		# command = texts, to, match: param
		dict_commands = self.yaml_obj[section][action]
		str_param = None
		cmd = None
		found = False
		for str_command in dict_commands:
			sign_index = str_command.index('=')
			cmd = str_command[0:sign_index].strip()
			cmd_variations = str_command[sign_index + 1:].split(',')

			for srt_var in cmd_variations:
				array_var = str_to_array(srt_var)
				if user_args == array_var: # the user input is the same as a action command
					str_param = self.yaml_obj[section][action][str_command]
					found = True
					break

		# print(self._actions.get(key, 'Observar'))
		# print(self._actions.get(key, None))
		if not found :#or self._actions.get(key, None) != None: # default message
			str_param = self._actions[action]

		return (cmd, str_param, found)

	def _load_actions(self, section):	
		# não esquecer do especial goback que deve ser procurado antes do scan ocorrer
		# como seria feito isso? eu retornaria uma flag para o metodo anterior?
		# outra coisa é que não é possivel fazer condinionais no yaml?
		# pois se eu entro aqui para "pegar uma arma" por exemplo
		# então a prox vez que entro aqui não deve-se fazer nada
		
		# keys = self.yaml_obj[section_action].keys()
		
		# if ('goback' in keys):
		# 	self._load_section(self.prev_sec, False)
		
		action_keys = list(self.yaml_obj[section].keys())
		str_inputargs = Console.scan_args()
		while True:
			write_notfound = True

			for action_key in action_keys:
				# isso realmente precisava ficar aqui aumentando o nivel de indent? pela logica eu posso retirar a obrigatoriedade de ter actions predefinididas. < fazer isso.
				if action_key in self._actions: # check if is a valid key
					if str_inputargs[0] == action_key: # the user get the correct verb
						cmd, param, found = self._parse_action(str_inputargs[1:], section, action_key)
						
						if not found: # command will be None if the text after the verb not match
							Console.writeln(param)
							write_notfound = False
						else:
							self._execute_action(cmd, param)
							# continue
						# else:
						#  	return # if i'm use break then pass a arg with a number of block to jump
				# else:
					# print(action_key)
					# print(action_key in self._actions.keys())
					# print(self._actions)
						
			if write_notfound:
				Console.writeln(str_inputargs[0] + ' ' + self._actions['_notfound'])

			str_inputargs = Console.scan_args()

