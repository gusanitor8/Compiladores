from src.yalex.Yalex import Yalex

def test__read_yal():
    assert False


def test__build_nfa():
    yalex = Yalex("./../utils/yalex_files/slr-2.yal")
    yalex._build_nfa()
    assert True


def test__longest_match():
    assert False
