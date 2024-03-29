from src.ShuntingYard.shunting_yard import ShuntingYard
from src.regex.regex import Regex
def test_get_postfix_regex():
    sy = ShuntingYard()

    assert False


def test_convert_to_postfix():
    assert False


def test__format_reg_ex():
    sy = ShuntingYard()
    res = sy._format_reg_ex("p(a|b)+p")
    assert res == "p.(a|b)+.p"

    res = sy._format_reg_ex("\\(a|b)+p")
    assert res == "\\.(a|b)+.p"

    regex = "('+')"
    res = sy._format_reg_ex(regex)
    assert res == regex

    regex = "(&|'''|'('|')'|'*'|'+')"
    res = sy._format_reg_ex(regex)
    assert res == regex

    regex = "(a|b)\n+"
    res = sy._format_reg_ex(regex)
    expected = "(a|b).\n+"
    assert res == expected

    regex = "'(''*'(a|b|c)*'*'')'"
    expected = "'('.'*'.(a|b|c)*.'*'.')'"
    res = sy._format_reg_ex(regex)
    assert res == expected

    regex = "(0|1|2|3|4|5|6|7|8|9)+('.'(0|1|2|3|4|5|6|7|8|9)+)?('E'('+'|'-')?(0|1|2|3|4|5|6|7|8|9)+)?"
    expected = "(0|1|2|3|4|5|6|7|8|9)+.('.'.(0|1|2|3|4|5|6|7|8|9)+)?.('E'.('+'|'-')?.(0|1|2|3|4|5|6|7|8|9)+)?"

    res = sy._format_reg_ex(regex)
    assert res == expected


def test__infix_to_postfix():

    assert False
