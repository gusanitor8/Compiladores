from src.LR0.Builder import Builder

def test_closure():
    grammar = [
        {"S": ["A", "B"]},
        {"A": ["a", "A"]},
        {"A": ["b"]},
        {"B": ["c"]}
    ]

    grammar_adresses = {
        "S": [0],
        "A": [1, 2],
        "B": [3]
    }

    builder = Builder(grammar, grammar_adresses)
    res = builder.closure({(0, 0)})
    print("hi")

def test_get_item_sets():
    grammar = [
        {"S": ["A", "B"]},
        {"A": ["a", "A"]},
        {"A": ["b"]},
        {"B": ["c"]}
    ]

    grammar_adresses = {
        "S": [0],
        "A": [1, 2],
        "B": [3]
    }

    builder = Builder(grammar, grammar_adresses)
    index_set_dic, lr0 = builder.get_item_sets()
    builder.draw_automaton(index_set_dic, lr0)
    print("hi")
