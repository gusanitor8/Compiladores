from src.Parsing.Parser import Parser
from src.Parsing.Grammar import Grammar
from src.constants import EPSILON


def test__compute_action():
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
    parser = Parser(grammar)
    print("hi")

    productions = [
        {'e': ['e', '+', 't']},
        {'e': ['t']},
        {'t': ['f', '*', 't']},
        {'t': ['f']},
        {'f': ['(', 'e', ')']},
        {'f': ['ID']}
    ]
    tokens = {'+', '*', '(', ')', 'ID'}
    production_adress = {'e': [0, 1], 't': [2, 3], 'f': [4, 5]}

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    parser = Parser(grammar)
    print()
    print("grammar productions: \n")
    for idx, prod in enumerate(grammar.productions):
        print(f"{idx}: {prod}")

    print("")
    parser.print_table()

    productions = [
        {'s': ['a', 'b']},
        {'s': ['b', 'a']},
        {'a': ['A']},
        {'b': ['A']}
    ]
    tokens = {"A"}
    production_adress = {'s': [0, 1], 'a': [2], 'b': [3]}

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    try:
        parser = Parser(grammar)
    except ValueError:
        assert True





