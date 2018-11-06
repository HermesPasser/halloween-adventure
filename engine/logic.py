import yaml
from console import Console, str_to_array

# IMPORTANTE: no lugar de definir as palavras no xml, definir palavras padrão e só definir o que cada uma fará em todos os 


# customizar futuro vocabulario de erro deixando ele como uma var static ou talvez deixarndo clusula no storyboard?	

# verificar se é possivel metch nulo

WRITE_KEYWORD = 'write'
WRITEDESC_KEYWORD = 'writedesc'
GOTO_KEYWORD = 'goto'
END_KEYWORD = 'end'
EXIT_INTERN = 'exit' # _exit in the yaml
HELP_INTERN = 'help' # _help in the yaml and _helptext for the text to be displayed
# LOADFILE = 'load' # not in use, to load a new storyboard

# acusa '... não é um verbo conhecido' se este verbo não ser usado na cena atual

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
		self.return_load_section = False # Tells that is need to go back there to load a new action (avoiding push a load_section above another in the stack)
		self.curr_sec = 'main'
		self._load_default_actions()
		self._running = True
		while self._running:
			self.return_load_section = False
			self._load_section(self.curr_sec)

	def _load_default_actions(self):
		global HELP_INTERN, EXIT_INTERN
		self._actions = self.yaml_obj['actions']
		# load the intern_actions
		HELP_INTERN = self._actions.get('_help', None) or HELP_INTERN
		EXIT_INTERN = self._actions.get('_exit', None) or EXIT_INTERN

	def _load_section(self, str_section):
		str_description = self.yaml_obj[str_section].get('description', "...") # show '...' if no description is found
		Console.writedln(str_description.strip())
		
		self._load_actions(str_section)

	def _execute_action(self, command, param):
		global HELP_INTERN, EXIT_INTERN
		if command == WRITE_KEYWORD:
			Console.writeln(param)
		elif command == WRITEDESC_KEYWORD:
			Console.writedln(param)
		elif command == GOTO_KEYWORD:
			self.curr_sec = param
			self.return_load_section = True
		elif command == END_KEYWORD:
			self.return_load_section = True
			self._running = False
		
	def _parse_action(self, user_args, section, action):
		""" Return the command given and the param """
		# command = texts, to, match: param
		dict_commands = self.yaml_obj[section][action]
		str_param = None
		found = False
		cmd = None
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

		if not found : # if the user msg is not on defineds on the storyboard then set to default msg
			str_param = self._actions[action]

		return (cmd, str_param, found)

	def _exec_intern(self, command):
		global HELP_INTERN, EXIT_INTERN

		if command == EXIT_INTERN:
			self.return_load_section = True
			self._running = False
			return True
		elif command == HELP_INTERN:
			Console.writedln(".ola ...")#self._actions.get('_helptext', ''))
			return True
		return False

	def _load_actions(self, section):
		action_keys = list(self.yaml_obj[section].keys())
		str_inputargs = Console.scan_args()
		while True:
			write_notfound = True

			for action_key in action_keys:# or action_key:
				# Maybe make this one optional (check if the key is on the denfineds) (it will need to check if the key exists on the _parse_action)
				if action_key in self._actions: # check if is a valid key
					if str_inputargs[0] == action_key: # the user get the correct verb
						cmd, param, found = self._parse_action(str_inputargs[1:], section, action_key)
						
						write_notfound = False
						if not found: # command will be None if the text after the verb not match
							Console.writeln(param + "....")
						else:
							self._execute_action(cmd, param)
			
			if self._exec_intern(str_inputargs[0]): # check and execute if is a intern cmd, return false if not
				write_notfound = False
						
			if self.return_load_section:
				return

			if write_notfound:
				Console.writeln(str_inputargs[0] + ' ' + self._actions['_notfound'])

			str_inputargs = Console.scan_args()

