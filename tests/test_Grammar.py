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
    assert nullable is False

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
    assert nullable is False