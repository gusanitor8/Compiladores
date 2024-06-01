from src.Parsing.Grammar import Grammar
from src.LR0.Builder import Builder
from src.constants import ENDMAKER


class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.builder = Builder(grammar.productions, grammar.production_adress)
        self.index_set_dic, self.lr0 = self.builder.get_item_sets()
        self.action = self._compute_action()
        self.goto = self._compute_goto()

    def _compute_action(self):
        action = {}
        initial_state = list(self.builder.initial_set)[0]
        s_prime, _, _ = self.builder.decode_item(initial_state)
        for state_no in self.index_set_dic.keys():
            for item in self.index_set_dic[state_no]:
                key, production, dot_position = self.builder.decode_item(item)

                # We check if the dot position is at the end of the production
                if dot_position >= len(production):
                    if key == s_prime:
                        if (state_no, ENDMAKER) in action:
                            raise ValueError("Grammar is not SLR(1)")

                        action[(state_no, ENDMAKER)] = "acc"
                    else:
                        if key in self.grammar.non_terminals:
                            follow_set = self.grammar.get_follow_set(key)
                            for symbol in follow_set:
                                # TODO: check if this is correct
                                if (state_no, symbol) in action:
                                    raise ValueError("Grammar is not SLR(1)")

                                action[(state_no, symbol)] = "r" + str(item[0])
                else:
                    symbol = production[dot_position]
                    if symbol in self.grammar.terminals:
                        # TODO: check if this is correct
                        goto_state = self.lr0[state_no][symbol]

                        if (state_no, symbol) in action:
                            raise ValueError("Grammar is not SLR(1)")

                        action[(state_no, symbol)] = "s" + str(goto_state)

        return action

    def _compute_goto(self):
        goto = {}
        for non_terminal in self.grammar.non_terminals:
            for state_no in self.index_set_dic.keys():
                if state_no in self.lr0:
                    if non_terminal in self.lr0[state_no]:
                        goto_state = self.lr0[state_no][non_terminal]
                        goto[(state_no, non_terminal)] = goto_state

        return goto

    def print_table(self):
        # we print the header
        print("state", end="\t")

        print("action", end="")
        print("\t" * (len(self.grammar.terminals)+1), end="")

        print("goto", end="")
        print("\t" * len(self.grammar.non_terminals), end="")
        print("", end="\n")

        print("", end="\t\t")
        for terminal in self.grammar.terminals:
            print(terminal, end="\t")

        # endmarker
        print(ENDMAKER, end="\t")

        for non_terminal in self.grammar.non_terminals:
            print(non_terminal, end="\t")
        print("", end="\n")

        for state_no in self.index_set_dic.keys():
            # we print the state number
            print(state_no, end="\t\t")

            # we print the action part of the table
            for terminals in self.grammar.terminals:
                if (state_no, terminals) in self.action:
                    print(self.action[(state_no, terminals)], end="\t")
                else:
                    print("", end="\t")

            # endmarker part
            if (state_no, ENDMAKER) in self.action:
                print(self.action[(state_no, ENDMAKER)], end="\t")
            else:
                print("", end="\t")

            # we print the goto part of the table
            for non_terminals in self.grammar.non_terminals:
                if (state_no, non_terminals) in self.goto:
                    print(self.goto[(state_no, non_terminals)], end="\t")
                else:
                    print("", end="\t")

            print("", end="\n")
