from src.regex.regex import Regex
from src.yalex.Yalex import Yalex


def run():
    any = '(' + Regex.generate_char_set_with_separator('(', '[', ']', '|') + ')'
    azAZ = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z') + ')'
    azAZ2 = '(' + Regex.generate_char_set_with_separator('a', 'b') + ')'
    azAZ09 = '(' + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9') + ')'
    variable_regex = "let +" + azAZ2 + azAZ2 + "* *= *" + azAZ2 + "+;*"
    comment_regex = " *'(''*' *" + azAZ2 + "+ *'*'')'"
    # regex = Regex(variable_regex)
    regex = Regex(comment_regex)
    print(regex.search("(*a*)"))

    # yalex = Yalex("utils/yalex_files/slr-2.yal")
    # yalex.read_yalex()


if __name__ == "__main__":
    run()
