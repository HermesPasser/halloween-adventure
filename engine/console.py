import sys, time
from shutil import get_terminal_size


def is_debug():
    return 'pydevd' in sys.modules


def str_to_array(str, separator=' '):
    raw_args = str.split(separator)
    final_args = []
    for arg in raw_args:
        if arg == '':
            continue
        arg = arg.strip()
        final_args.append(arg)
    return final_args


class Console:
    """ Note: this is a static class, the delay routines cannot work with multithread """

    # Output
    _text = ''
    _pos = 0
    _default_delay = 0.06
    _delay = _default_delay

    # Input
    input = ''

    @classmethod
    def _clear_output(self):
        self._text = ''
        self._pos = 0
        self._delay = self._default_delay

    @classmethod
    def write(self, text):
        """ Write on console
            text: string 
		"""
        print(text, end='', flush=True)

    @classmethod
    def writeln(self, text):
        """ Write on console with a new line at the end
        text: string 
		"""
        print(text)

    @classmethod
    def _write_chars(self):
        while (self._pos < len(self._text)):
            self.write(self._text[self._pos])
            self._pos += 1

            if not is_debug():  # nobody wants to wait while debugging
                time.sleep(self._delay)

    @classmethod
    def writedl(self, text, delay=None):
        """ Write on console with a delay
            text: string 
            delay: delay in seconds
		"""
        self._clear_output()
        self._text = text
        self._delay = delay or self._delay
        self._write_chars()

    @classmethod
    def writedln(self, text, delay=None):
        """ Write on console with a delay and a new line at the end
            text: string 
            delay: delay in seconds
		"""
        self.writedl(text + "\n", delay)

    @classmethod
    def scroll_down(self):
        """ Scroll down all lines """
        lines = 0
        try:
            lines = get_terminal_size().lines
        except:
            lines = 10

        for x in range(0, lines):
            self.writedln('')

    @classmethod
    def _clear_input(self):
        self.input = ''
        self.args = []

    @classmethod
    def scan(self):
        """ Write the prompt '>' and get the user input in lower case"""
        self.write('\n> ')
        self.input = input().strip().lower()
        return self.input

    @classmethod
    def scan_args(self):
        """ Write the prompt '>' and get the user input in lower case formatted in arguments """
        return str_to_array(self.scan())
