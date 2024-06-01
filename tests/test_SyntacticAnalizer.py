from src.Parsing.SyntacticAnalizer import SyntacticAnalizer
from src.Parsing.Grammar import Grammar
from src.Parsing.Parser import Parser


def test_SyntacticAnalizer():
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
    analizer = SyntacticAnalizer(parser, ["ID", "+", "ID", "*", "ID", "*"])
    analizer.parse()
