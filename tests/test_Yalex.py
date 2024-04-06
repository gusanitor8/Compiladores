from src.yalex.Yalex import Yalex


def test__read_yal():
    assert False


def test__build_nfa():
    yalex = Yalex("./../utils/yalex_files/slr-2.yal")
    assert True


def test__replace_special_chars():
    string = "hello'_'hello_"
    res = Yalex._replace_special_chars(string)
    assert res == "hello'_'hello['!'-'~']"


def test__longest_match():
    assert False


def test_document_iterator():
    yalex = Yalex("./../utils/yalex_files/slr-2.yal")
    yalex.document_iterator()
    assert True


def test__regex_iterator():
    yalex = Yalex("./../utils/yalex_files/slr-extr.yal")
    assert True
