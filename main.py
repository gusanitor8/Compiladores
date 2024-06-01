from src.yapar.yaparReader import run as yapar_run
from src.LR0.Builder import Builder
from src.LexicalAnalizerGenerator.LexicalAnalizerGenerator import LexicalAnalizerGenerator
from src.yalex.tokenGetter import run as token_getter_run
from src.Parsing.Grammar import Grammar
from src.Parsing.Parser import Parser
from src.Parsing.SyntacticAnalizer import SyntacticAnalizer
from lexicalOut.lexical_analizer.lexicalAnalizer import run as lexical_analizer_run


def run():
    YALEX_PATH = "./utils/yalex_files/YALex2.txt"
    YAPAR_PATH = "./utils/yapar_files/YAPar5.txt"
    INPUT_PATH = "./In/text.txt"

    # TODO: NOTE: do NOT enter yapars with non ascii characters since it was not designed to handle them
    # We get the grammar from the yapar file
    tokens, productions, production_adress = yapar_run(YAPAR_PATH)

    # We get the tokens from the yalex file
    yalex_tokens = set(token_getter_run(YALEX_PATH))
    print(yalex_tokens)
    print(tokens)

    # if tokens do not match we raise an exception
    # if not tokens.issubset(yalex_tokens):
    #     raise Exception("Tokens missing in yapar file")

    # TODO: NOTE: it is not necessary to compile the yalex every time
    # We generate a lexical analizer based on the yalex file
    # LexicalAnalizerGenerator(YALEX_PATH, "lexical_analizer")

    # We get the token stream from the input
    token_stream = lexical_analizer_run(INPUT_PATH)

    grammar = Grammar(tokens, productions, production_adress, augment_grammar=True)
    parser = Parser(grammar)

    # We print the parsing table
    parser.print_table()

    # We parse the token stream
    analizer = SyntacticAnalizer(parser, token_stream)
    analizer.parse()


if __name__ == "__main__":
    run()
