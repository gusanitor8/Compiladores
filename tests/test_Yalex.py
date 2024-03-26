from src.yalex.Yalex import Yalex

def test__read_yal():
    assert False


def test__build_nfa():
    yalex = Yalex("./../utils/yalex_files/slr-2.yal")
    assert True


def test__longest_match():
    assert False

def test_document_iterator():
    yalex = Yalex("./../utils/yalex_files/slr-2.yal")
    yalex.document_iterator()
    assert True
