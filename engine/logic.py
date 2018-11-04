import yaml
from console import Console

# IMPORTANTE: no lugar de definir as palavras no xml, definir palavras padrão e só definir o que cada uma fará em todos os 

# concatenar comandos expecificos com os de configuração como 'sair'

# ter que sacrificar a leitura e mudar para xml para poder adicionar atributos que facilitarão a vida ao invés de eu ter que encadear mais parametros ou ficar cortando um nó em duas partes

#arranjar um jeito de separar descrições com delay do feedback que não deve telo

# customizar futuro vocabulario de erro deixando ele como uma var static ou talvez deixarndo clusula no storyboard?	
class Parser:
	def __init__(self, yaml_path):
		self.prev_sec = 'main'
		self.yaml_obj = yaml.load(open(yaml_path, 'r', encoding = 'utf-8'))
	
	def start(self):
		""" Init the engine """
		self._load_section('main')
		
	def _raise_if_notfound(self, key):
		""" Raise if the key is not found """
		if not self.yaml_obj.get(key, None):
			raise Exception("'%s' section not found" % key)
		
	def _load_section(self, section, playMonologue = True):
		if (playMonologue):
			section_monologue = section + '-monologue'
			self._raise_if_notfound(section_monologue)
			Console.writedln(self.yaml_obj[section_monologue].rstrip())
		self._load_actions(section)
		self.prev_sec = section
	
	def _load_actions(self, section):
		section_action = section + '-action'
		self._raise_if_notfound(section_action)
		
		# não esquecer do especial goback que deve ser procurado antes do scan ocorrer
		# como seria feito isso? eu retornaria uma flag para o metodo anterior?
		# outra coisa é que não é possivel fazer condinionais no yaml?
		# pois se eu entro aqui para "pegar uma arma" por exemplo
		# então a prox vez que entro aqui não deve-se fazer nada
		
		keys = self.yaml_obj[section_action].keys()
		
		if ('goback' in keys):
			self._load_section(self.prev_sec, False)
		
		Console.scan()
		match = False
		while True:
			for key in keys:
				subkeys = key.split(',')
				for subkey in subkeys:
					subkey = subkey.strip()
					if (subkey == Console.input):
						match = True
						sec = self.yaml_obj[section_action][key]
						self._load_section(sec)
						break;
			if (not match):
				Console.writeln("'%s' não é um comando inválido." % Console.input)
				Console.scan()
