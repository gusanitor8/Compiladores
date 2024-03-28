from src.regex.regex import Regex
from src.constants import EPSILON


def test_generate_char_set_with_separator():
    """
    This functioncs checks if the generate_char_set_with_separator function works as expected
    :return:
    """
    res = Regex.generate_char_set_with_separator('!', '0')
    expected = "!|\"|#|$|%|&|'''|'('|')'|'*'|'+'|,|-|'.'|/|0"
    assert res == expected

    any = Regex.generate_char_set_with_separator('!', '~')
    expected = "!|\"|#|$|%|&|'''|'('|')'|'*'|'+'|,|-|'.'|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|'?'|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|'|'|}|~"
    assert any == expected


def test__build_dfa():
    """
    This functions checks if the dfa was built with no apparent errors
    :return:
    """
    test_regex = "(!|\"|#|$|%|&|'''|'('|')'|'*'|'+'|,|-|'.'|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|'?'|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|'|'|}|~)"
    automaton = Regex._build_dfa(test_regex)
    assert automaton is not None

    regex = Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9')
    azAZ09 = "(" + regex + ")"
    any = '(' + Regex.generate_char_set_with_separator('!', '~') + '| )'
    az = "(" + Regex.generate_char_set_with_separator('a', 'z') + ")"

    variable_regex = "( *let +" + az + azAZ09 + "* *= *" + any + "+\n*)+"
    regex_var = Regex(variable_regex)
    assert regex_var is not None

    string = "let a = hello\n"
    result = regex_var.longest_match(string)
    assert result == (0, 14)

    comment_regex = "'(''*'" + any + "*'*'')'"
    regex_comm = Regex(comment_regex)
    assert regex_comm is not None

    string = "(*hola q tal*)"
    result = regex_comm.longest_match(string)
    assert result == (0, 14)

    rules_dfa = Regex(" *('|'|" + EPSILON + ") *" + az + azAZ09 + "* *= *{" + any + "*} *")
    string = "ws        { return WHITESPACE } "
    match = rules_dfa.longest_match(string)
    new_string = string[match[1] - 1:]
    assert match == (0, 30)


def test_shortest_match():
    test_regex = "hello"
    regex = Regex(test_regex)

    assert regex.shortest_match("hello") == (0, 5)
    assert regex.shortest_match(" hello") is None

    test_regex = "ba*"
    regex = Regex(test_regex)

    assert regex.shortest_match("ba") == (0, 1)
    assert regex.shortest_match(" ba") is None

    test_regex = "a*"
    regex = Regex(test_regex)

    assert regex.shortest_match("a") == (0, 0)


def test_longest_match():
    test_regex = "hello"
    regex = Regex(test_regex)

    assert regex.longest_match("hello") == (0, 5)
    assert regex.longest_match(" hello") is None

    test_regex = "ba*"
    regex = Regex(test_regex)

    assert regex.longest_match("ba") == (0, 2)
    assert regex.longest_match(" ba") is None


def test_shortest_search():
    test_regex = "hello"
    regex = Regex(test_regex)

    assert regex.shortest_search("hello") == (0, 5)
    assert regex.shortest_search(" hello") == (1, 6)

    test_regex = "ba*"
    regex = Regex(test_regex)

    assert regex.shortest_search("ba") == (0, 1)
    assert regex.shortest_search(" ba") == (1, 2)

    test_regex = "a*"
    regex = Regex(test_regex)

    assert regex.shortest_search("a") == (0, 0)
    assert regex.shortest_search(" a") == (0, 0)
    assert regex.shortest_search("") == (0, 0)


def test_longest_search():
    test_regex = "hello"
    regex = Regex(test_regex)

    assert regex.longest_search("hello") == (0, 5)
    assert regex.longest_search(" hello") == (1, 6)

    test_regex = "a*"
    regex = Regex(test_regex)

    assert regex.longest_search(" ") == (0, 0)

    any = '(' + Regex.generate_char_set_with_separator('!', '~') + '| )'
    regex = charset_regex2 = "[\"" + any + "+\"]"
    charset_regex2 = Regex(charset_regex2)
    string = "[\"\s\\t\\n\"]"

    assert charset_regex2.longest_search(string) == (0, 10)

