from src.yalex.Yalex import Yalex
from src.ShuntingYard.shunting_yard import ShuntingYard
from src.ShuntingYard.parse_tree_builder import ParseTree


def run():
    yalex = Yalex("utils/yalex_files/slr-2.yal")
    document = yalex.get_document()
    regexes = []

    for identifier in document["entrypoint"]["code"].keys():
        if identifier in document["variables"]:
            regex = document["variables"][identifier]
            regexes.append(regex)

        else:
            regex = identifier
            regexes.append(regex)

    super_regex = ""
    for postfix in regexes:
        super_regex += "(" + postfix + ")|"

    super_regex = super_regex[:-1]
    postfix = ShuntingYard.convert_to_postfix(super_regex)
    ParseTree(postfix, display_tree=True, suffix="_super_tree")




if __name__ == "__main__":
    run()
