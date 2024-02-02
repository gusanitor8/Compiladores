from ShuntingYard.shunting_yard import ShuntingYard
from ShuntingYard.parse_tree_builder import ParseTree

if __name__ == "__main__":
    regex = ShuntingYard().getPostfixRegex()
    tree = ParseTree(regex[0] + str("#."))  # TODO: add a # to the end of the regex

    tree.print_tree()
    tree = tree.get_tree()




