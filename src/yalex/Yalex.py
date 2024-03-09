from src.regex.regex import Regex


class Yalex:
    def __init__(self, filename: str):
        self.read_file = self.read_file(filename)
        self.str_right_side = self.read_file
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

    def read_yalex(self):
        comment_rec: Regex = self._comment_recognizer()
        variable_rec: Regex = self._variable_recognizer()

        res_com = comment_rec.longest_match(self.str_right_side)
        res_var = variable_rec.longest_match(self.str_right_side)

        while res_com is not None and res_var is not None:
            break

    def _comment_recognizer(self, ):
        any = '(' + Regex.generate_char_set_with_separator('(', '[', ']', '|') + ')'
        comment_regex = " *(\* *" + any + "* *)+"
        regex = Regex(comment_regex)
        return regex

    def _variable_recognizer(self, ):
        any = '(' + Regex.generate_char_set_with_separator('(', '[', ']', '|') + ')'
        azAZ = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z') + ')'
        azAZ09 = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9') + ')'
        variable_regex = "(let +" + azAZ + azAZ09 + "* *= *" + any + "+ +;+)"
        regex = Regex(variable_regex)
        return regex
