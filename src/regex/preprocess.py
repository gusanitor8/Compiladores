from src.regex.regex import Regex


class Preprocessing:
    def __init__(self, string: str):
        self.string = string

    def preprocess(self, regex: str):
        pass

    def _build_nfa(self):
        any = '(' + Regex.generate_char_set_with_separator('!', '~') + '| )'
        charset_regex = "[('''" + any + "'''-'''" + any + "''')+]"
        charset_regex = Regex(charset_regex)

        charset_regex2 = "[\""+any+"+\"]"
        charset_regex2 = Regex(charset_regex2)


