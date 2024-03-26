from src.regex.regex import Regex


def run():
    regex = Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9')
    azAZ09_ = "( |" + regex + ")"
    azAZ09 = "(" + regex + ")"
    any = '(' + Regex.generate_char_set_with_separator('!', '~') + ')'
    az = "("  + Regex.generate_char_set_with_separator('a', 'z') + ")"


    comment_regex = "'(''*'" + azAZ09_ + "*'*'')'"
    variable_regex = "( *let +" + az + azAZ09 + "* *= *"+ any + "+\n*)+"


    regex_var = Regex(variable_regex)
    regex = Regex(comment_regex)
    print()


if __name__ == "__main__":
    run()
