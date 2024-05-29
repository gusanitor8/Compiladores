from src.yapar.yaparReader import run as yapar_run
from src.Parsing.Grammar import Grammar
from src.constants import EPSILON


def test_grammar():
    productions = [{'s': ['s', 'x']},
                   {'s': ['y']},
                   {'x': ['X']},
                   {'y': ['Y']}]
    tokens = {'X', 'Y'}
    production_adress = {'s': [0, 1], 'x': [2], 'y': [3]}

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    nullable, first_set = grammar.first('s')
    expected_set = {'Y'}
    assert nullable is False
    assert first_set == expected_set

    productions = [{'s': ['s', 'x']},
                   {'s': ['y']},
                   {'x': ['X']},
                   {'x': [EPSILON]},
                   {'y': ['Y']},
                   {'y': [EPSILON]}]
    tokens = {'X', 'Y'}
    production_adress = {'s': [0, 1], 'x': [2, 3], 'y': [4, 5]}

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    nullable, first_set = grammar.first('s')
    expected_set = {'Y', 'X', EPSILON}
    assert nullable is True
    assert expected_set == first_set

    productions = [
        {'e': ['t', "e'"]},
        {"e'": ["+", 't', "e'"]},
        {"e'": [EPSILON]},
        {'t': ['f', "t'"]},
        {"t'": ["*", 'f', "t'"]},
        {"t'": [EPSILON]},
        {'f': ['(', 'e', ')']},
        {'f': ['ID']}
    ]
    tokens = {'+', '*', '(', ')', 'ID'}
    production_adress = {'e': [0], "e'": [1, 2], 't': [3], "t'": [4, 5], 'f': [6, 7]}

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    nullable, first_set = grammar.first('f')
    assert nullable is False
    assert first_set == {'(', 'ID'}

    nullable, first_set = grammar.first("e'")
    assert nullable is True
    assert first_set == {'+', EPSILON}


def test_follow():
    productions = [
        {'e': ['t', "e'"]},
        {"e'": ["+", 't', "e'"]},
        {"e'": [EPSILON]},
        {'t': ['f', "t'"]},
        {"t'": ["*", 'f', "t'"]},
        {"t'": [EPSILON]},
        {'f': ['(', 'e', ')']},
        {'f': ['ID']}
    ]
    tokens = {'+', '*', '(', ')', 'ID'}
    production_adress = {'e': [0], "e'": [1, 2], 't': [3], "t'": [4, 5], 'f': [6, 7]}
    print()
    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    for non_terminal in grammar.non_terminals:
        nullable, first_set = grammar.first(non_terminal)
        print(non_terminal, end="\t\t")
        print(first_set, end="\t\t")
        print(nullable)

