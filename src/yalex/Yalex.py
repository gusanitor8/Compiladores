from src.regex.regex import Regex


class Yalex:
    def __init__(self, filename: str):
        self.read_file = self.read_file(filename)
        self.header = ""
        self.comments = []
        self.regex = []
        self.rules = []
        self.trailer = ""

    def read_file(self, filename: str):
        with open(filename, "r") as file:
            lines = file.readlines()
            string = " "
            string = string.join(lines)
            string = string.replace('\n', ';')

        return string


    def _comment_recognizer(self,):
        any = '(' + Regex.generate_char_set_with_separator('(', '|') + ')'
        comment_regex = " *(\* *" + any + "* *)+"
        regex = Regex(comment_regex)

    def _variable_recognizer(self,):
        any = '(' + Regex.generate_char_set_with_separator('(', '[', ']', '|') + ')'
        azAZ = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z') + ')'
        azAZ09 = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9') + ')'
        variable_regex = "(let +" + azAZ + azAZ09 + "* *= *" + any + "+ +;+)"
        regex = Regex(variable_regex)




