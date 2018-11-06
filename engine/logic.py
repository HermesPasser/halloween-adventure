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
		str_description = self.yaml_obj[str_section].get('description', "não encontrado")
		Console.writedln(str_description)
		
		self._load_actions(str_section)
		self.prev_sec = str_section

	def _execute_action(self, command, param):
		if command == WRITE_KEYWORD:
			Console.writeln(param)
		elif command == GOTO_KEYWORD:
			self._load_section(param)
		
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

		if not found :#or self._actions.get(key, None) != None: # default message
			str_param = self._actions[action]

		return (cmd, str_param, found)

	def _load_actions(self, section):
		action_keys = list(self.yaml_obj[section].keys())
		str_inputargs = Console.scan_args()
		while True:
			write_notfound = True

			for action_key in action_keys:
				# isso realmente precisava ficar aqui aumentando o nivel de indent? pela logica eu posso retirar a obrigatoriedade de ter actions predefinididas. < fazer isso.
				if action_key in self._actions: # check if is a valid key
					if str_inputargs[0] == action_key: # the user get the correct verb
						cmd, param, found = self._parse_action(str_inputargs[1:], section, action_key)
						
						write_notfound = False
						if not found: # command will be None if the text after the verb not match
							Console.writeln(param)
						else:
							self._execute_action(cmd, param)
						
			if write_notfound:
				Console.writeln(str_inputargs[0] + ' ' + self._actions['_notfound'])

			str_inputargs = Console.scan_args()

