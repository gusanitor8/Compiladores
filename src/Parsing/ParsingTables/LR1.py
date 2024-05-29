from src.Parsing.Grammar import Grammar
from typing import Tuple
from src.constants import ENDMAKER


class Lr1:
    def __init__(self, grammar: Grammar):
        self.grammar: Grammar = grammar

    def closure(self, item_set) -> Tuple[set, dict]:
        look_aheads = {self.grammar.initial_item: {ENDMAKER}}

        def _set_look_ahead(item_, look_ahead: set):
            nonlocal look_aheads
            if item_ not in look_aheads:
                look_aheads[item_] = look_ahead
            else:
                look_aheads[item_] = look_ahead | look_aheads[item_]

        def _get_look_ahead(item_set_):
            nonlocal look_aheads
            if item_set_ in look_aheads:
                return look_aheads[item_set_]
            else:
                return set()

        res = item_set.copy()
        j = list(item_set)

        # while there is an item in the list
        while j:
            item = j.pop(0)
            key, production, dot_position = self._decode_grammar_item(item)

            # We check that the dot is not at the end of the production
            if dot_position > len(production):
                continue

            # non terminal B
            B = production[dot_position]

            # We check that the symbol is a terminal
            if B not in self.grammar.non_terminals:
                continue

            beta = None
            if dot_position + 1 < len(production):
                beta = production[dot_position + 1]

            # for each production of the non terminal B
            for prod_idx in self.grammar.production_adress[B]:
                alpha = list(_get_look_ahead(item))

                if beta is not None:
                    beta_alpha = [beta] + alpha
                else:
                    beta_alpha = alpha

                _, first_beta_alpha = self.grammar.first_production(beta_alpha)
                first_beta_alpha = set(first_beta_alpha)
                b_item = (prod_idx, 0)
                _set_look_ahead(b_item, first_beta_alpha)

                # We add the item to the answer
                res.add(b_item)
                # We also add the item to the stack
                j.append(b_item)

        return res, look_aheads

    def go_to(self, item_set, symbol):
        j = set()
        for item in item_set:
            key, production, dot_position = self._decode_grammar_item(item)

            # We check that the dot is not at the end of the production
            if dot_position >= len(production):
                continue

            if production[dot_position] == symbol:
                j.add((key, dot_position + 1))

        return self.closure(j)

    def get_item_sets(self):
        pass

    def _decode_grammar_item(self, grammar_item: Tuple):
        """
        This method decodes an item
        :param grammar_item: Tuple
        :return:
        """
        key = list(self.grammar.productions[grammar_item[0]].keys())[0]
        production = self.grammar.productions[grammar_item[0]][key]
        dot_position = grammar_item[1]
        return key, production, dot_position
