from src.yapar.lexicalAnalizer import run as yapar_run
from src.LR0.Builder import Builder
from src.LexicalAnalizerGenerator.LexicalAnalizerGenerator import LexicalAnalizerGenerator
from src.yalex.tokenGetter import run as token_getter_run


def run():
    tokens, productions, production_adress = yapar_run("./utils/yapar_files/slr-4.yalp")
    yalex_tokens = set(token_getter_run("./utils/yalex_files/slr-4.yal"))

    print(yalex_tokens)
    print(tokens)

    if not tokens.issubset(yalex_tokens):
        print("Tokens missing in yapar file")
        raise Exception

    builder = Builder(productions, production_adress)
    index_set_dic, lr0 = builder.get_item_sets()
    builder.draw_automaton(index_set_dic, lr0, "slr-4")


if __name__ == "__main__":
    run()
