from src.Parsing.ParsingTables.LR1 import Lr1
from src.Parsing.Grammar import Grammar

def test_closure():
    productions = [
        {"s'": ["s"]},
        {"s": ["c", "c"]},
        {"c": ["C", "c"]},
        {"c": ["D"]}
    ]
    tokens = {"C", "D"}
    production_adress = {"s'": [0], "s": [1], "c": [2, 3]}
    grammar = Grammar(tokens, productions, production_adress, augment_grammar=False)
    lr1 = Lr1(grammar)
    res = lr1.closure({(0, 0)})
    print(res)
