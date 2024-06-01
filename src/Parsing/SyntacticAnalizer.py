from src.Parsing.Parser import Parser
from src.constants import ENDMAKER


class SyntacticAnalizer:
    def __init__(self, parser: Parser, input_: list):
        self.parser = parser
        self.stack = [0]  # Initial state
        self.input = input_
        self.input.append(ENDMAKER)
        self.symbols = []

    def parse(self):
        to_parse = True
        last_symbol = ""
        last_state = -1

        # # We always shift as a first step
        # self.symbols.append(self.input.pop(0))
        # self.stack.append(int(self.parser.action[(self.stack[-1], self.symbols[-1])][1:]))

        while to_parse:
            peeked_input = self.input[0]
            try:
                action = self.parser.action[(self.stack[-1], peeked_input)]
            except KeyError:
                keys = self.parser.action.keys()
                a_tuples = [t[1] for t in keys if t[0] == self.stack[-1]]
                print(f"Error: No action found for state {self.stack[-1]} and input {peeked_input}")
                print(f"Expected: {a_tuples}")
                exit(0)

            if action == "acc":
                to_parse = False
                print("string accepted")
                break

            if action[0] == "s":
                self.shift(action)

            elif action[0] == "r":
                self.reduce(action)

    def shift(self, res):
        number = int(res[1:])

        self.symbols.append(self.input.pop(0))
        self.stack.append(number)

    def reduce(self, res):
        number = int(res[1:])
        full_production = self.parser.grammar.productions[number]
        prod_symbol = list(full_production.keys())[0]
        production = full_production[prod_symbol]
        len_prod = len(production)
        self.stack = self.stack[:-len_prod]
        self.symbols = self.symbols[:-len_prod]

        self.symbols.append(prod_symbol)
        self.stack.append(self.parser.goto[(self.stack[-1], prod_symbol)])
