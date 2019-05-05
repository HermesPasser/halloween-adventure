import yaml
from interns import Interns
from console import Console, str_to_array

# TODO: remove from here
WRITE_KEYWORD = 'write'
WRITEDESC_KEYWORD = 'writedesc'
GOTO_KEYWORD = 'goto'
END_KEYWORD = 'end'

def load_yaml(file):
    from os.path import exists, isfile
    if not exists(file) or not isfile(file):
        return None
    with open(file, 'r', encoding='utf-8') as file:
        return file.read().replace("\t", ' ')


def save(section):
    with open('save.yaml', 'w', encoding='utf-8') as file:
        file.write('section: ' + section)


def load():
    text = load_yaml('save.yaml')
    if not text:
        return None

    yamobj = yaml.load(text)
    return yamobj.get('section', None)


class Parser:
    def __init__(self, yaml_path):
        text = load_yaml(yaml_path)
        self.yaml_obj = yaml.load(text)
        self.curr_sec = ''
        self._running = False

    def start(self):
        """ Init the engine & main loop """
        self.return_load_section = False  # Tells that is need to go back there to load a new action (avoiding push a load_section above another in the stack)
        self.curr_sec = 'main'
        self._load_default_actions()
        self._running = True
        while self._running:
            self.return_load_section = False
            self._load_description(self.curr_sec)
            self._load_actions(self.curr_sec)

    def load(self):
        self._exec_intern(Interns.LOAD)

    def _load_default_actions(self):
        self._actions = self.yaml_obj['actions']

        # load the intern actions
        Interns.LOAD = self._actions.get('_load', None) or Interns.LOAD
        Interns.SAVE = self._actions.get('_save', None) or Interns.SAVE
        Interns.HELP = self._actions.get('_help', None) or Interns.HELP
        Interns.EXIT = self._actions.get('_exit', None) or Interns.EXIT

    def _load_description(self, str_section):
        str_description = self.yaml_obj[str_section].get('description', "...")  # show '...' if no description is found
        Console.writedln(str_description.strip())

    def _execute_action(self, command, param):
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
                if user_args == array_var:  # the user input is the same as a action command
                    str_param = self.yaml_obj[section][action][str_command]
                    found = True
                    break

        if not found:  # if the user msg is not on defined ones on the storyboard then set to default msg
            str_param = self._actions[action]

        return (cmd, str_param, found)

    def _exec_intern(self, command):
        """ Returns true if a command was found and executed """

        if command == Interns.EXIT:
            self.return_load_section = True
            self._running = False
            return True
        elif command == Interns.HELP:
            Console.writedln(self._actions.get('_helptext', ''))
            return True
        elif command == Interns.SAVE:
            save(self.curr_sec)
            Console.writeln('Salvo')  # TODO: Add to actions
            return True
        elif command == Interns.LOAD:
            self.return_load_section = True
            sec = load()
            if sec:
                Console.writeln('Carregado!\n')  # TODO: Add to actions
                self.curr_sec = sec
            else:
                Console.writeln('Não pode carregar')  # TODO: Add to actions
            return True
        return False

    def _get_input(self):
        array_input = Console.scan_args()
        if len(array_input) == 0:
            return self._get_input()
        return array_input

    def _load_actions(self, section):
        action_keys = list(self.yaml_obj[section].keys())

        section_has_no_actions = len(action_keys) == 1
        if section_has_no_actions:  # if the section haven't actions (just the description) then finish the script
            self._exec_intern(Interns.EXIT)
            return

        # algo mudou já que removi o get input?

        while True:
            arr_inputargs = self._get_input()
            str_fsinput = arr_inputargs[0]

            if str_fsinput in self._actions and not str_fsinput in action_keys:  # if is a valid action but no one on the section
                #write_notfound = False
                Console.writeln(self._actions[str_fsinput])

            for action_key in action_keys:
                if not write_notfound:  # if conditional was true then skip this for
                    break

                # Maybe make this one optional (check if the key is on the denfineds) (it will need to check if the key exists on the _parse_action)
                if action_key in self._actions:  # check if is a valid key
                    if str_fsinput == action_key:  # the user get the correct verb
                        cmd, param, found = self._parse_action(arr_inputargs[1:], section, action_key)

                        write_notfound = False
                        if found:  # where the action is executed
                            self._execute_action(cmd, param)
                        else:  # command will be None if the text after the verb not match
                            Console.writeln(param)

            if self.return_load_section:  # return to the next iteration of the main loop
                return

            if not self._exec_intern(str_fsinput):
                Console.writeln(str_fsinput + ' ' + self._actions['_notfound'])
