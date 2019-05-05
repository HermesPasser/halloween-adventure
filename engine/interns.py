class Interns:
    # TODO: change to lower case
    SAVE = 'save'  # _save in the yaml
    LOAD = 'load'  # _load in the yaml
    EXIT = 'exit'  # _exit in the yaml
    HELP = 'help'  # _help in the yaml and _helptext for the text to be displayed

# uses too much processing, maybe put a chained if instead?
"""	@staticmethod
	def is_intern(cmd):
		#Loops through the class attributes and compares the cmd with the class static variables
		for i in dir(Interns):
			if i.startswith('_') or callable(i) or isinstance(i, staticmethod): # get rid of private attributes and methods
				continue

			value = Interns.__dict__[i]
			if value == cmd:
				return True

		return False
"""
