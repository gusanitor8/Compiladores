from ShuntingYard.shunting_yard import ShuntingYard
from ShuntingYard.parse_tree_builder import ParseTree
from DirectConstruction import DirectConstruction
from Thompson import Thompson
from NfaToDfa import NfaToDfa

if __name__ == "__main__":
    regex = ShuntingYard().getPostfixRegex()
    tree = ParseTree(regex[0])  # TODO: add a # to the end of the regex

    # # tree.print_tree()
    # nodes = tree.get_nodes()
    # tree = tree.get_tree()
    # afd = DirectConstruction(tree, nodes)

    thompson = Thompson(regex[0])
    afn = thompson.make_afn()
    afn.print_automata()

    converter = NfaToDfa(afn)
    dfa = converter.get_dfa()
    dfa.print_automata()











