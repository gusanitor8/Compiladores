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
        for state_no in self.lr0.keys():
            for item in self.index_set_dic[state_no]:
                key, production, dot_position = self.builder.decode_item(item)

                # We check if the dot position is at the end of the production
                if dot_position >= len(production):
                    if key == s_prime:
                        action[(state_no, ENDMAKER)] = "accept"
                    else:
                        if key in self.grammar.non_terminals:
                            follow_set = self.grammar.get_follow_set(key)
                            for symbol in follow_set:
                                # TODO: check if this is correct
                                action[(state_no, symbol)] = "r" + str(self.grammar.production_adress[key])
                else:
                    symbol = production[dot_position]
                    if symbol in self.grammar.terminals:
                        # TODO: check if this is correct
                        goto_state = self.lr0[state_no][symbol]
                        action[(state_no, symbol)] = "s" + str(goto_state)

        return action

    def _compute_goto(self):
        goto = {}
        for non_terminal in self.grammar.non_terminals:
            for state_no in self.lr0.keys():
                if non_terminal in self.lr0[state_no]:
                    goto_state = self.lr0[state_no][non_terminal]
                    goto[(state_no, non_terminal)] = goto_state

        return goto



