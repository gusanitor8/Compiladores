from ShuntingYard.shunting_yard import ShuntingYard
from ShuntingYard.parse_tree_builder import ParseTree
from DirectConstruction import DirectConstruction

if __name__ == "__main__":
    regex = ShuntingYard().getPostfixRegex()
    tree = ParseTree(regex[0])  # TODO: add a # to the end of the regex

    # tree.print_tree()
    nodes = tree.get_nodes()
    tree = tree.get_tree()
    afd = DirectConstruction(tree, nodes)
    afd.print_dfa()
    afd.render_dfa_graph('dfa_graph')


