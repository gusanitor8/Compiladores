from typing import Tuple, Set
from src.constants import EPSILON, ENDMAKER


class Grammar:
    def __init__(self, tokens, productions, production_adress, augment_grammar=False):
        self.tokens = tokens
        self.productions = productions
        self.production_adress = production_adress
        self.terminals = set()
        self.non_terminals = set()

        if augment_grammar:
            self.augment_grammar()

        self.symbols = self._get_symbols()
        self.initial_item = self.get_initial_item()
        self._classify_symbols()

    def _classify_symbols(self):
        for symbol in self.symbols:
            if symbol.islower():
                self.non_terminals.add(symbol)
            else:
                self.terminals.add(symbol)

    def _get_symbols(self):
        symbols = set()

        for dic in self.productions:
            for key in dic.keys():
                for symbol in dic[key]:
                    symbols.add(symbol)

        return symbols

    def get_initial_item(self):
        if len(self.productions) > 0:
            dic = self.productions[0]
            keys = list(dic.keys())
            lista = dic[keys[0]]

            if len(lista) > 0:
                return 0, 0

        raise Exception("Grammar is empty")

    def augment_grammar(self):
        """
        This method augments the grammar by adding a new production S' -> S where S is the start symbol
        :return:
        """
        start_symbol = list(self.productions[0].keys())[0]
        self.productions.insert(0, {"S'": [start_symbol]})

        for key in self.production_adress.keys():
            self.production_adress[key] = [i + 1 for i in self.production_adress[key]]

        self.production_adress["s'"] = [0]

    # TODO: this should be part of the parsing table since the decoding/encoding of a grammar item might change \
    #  depending on the parsing table
    def decode_grammar_item(self, grammar_item: Tuple):
        """
        This method decodes an item
        :param grammar_item: Tuple
        :return:
        """
        key = list(self.productions[grammar_item[0]].keys())[0]
        production = self.productions[grammar_item[0]][key]
        dot_position = grammar_item[1]
        return key, production, dot_position

    def first(self, symbol) -> Tuple[bool, Set]:
        """
        :param symbol:
        :return: a set of symbols, and True if its nullable or False if its not
        """
        nullable_ = False
        if symbol not in self.non_terminals:
            return False, {symbol}

        if symbol == EPSILON:
            return True, {EPSILON}

        first_ = set()
        symbol_idxs = self.production_adress[symbol]

        for symbol_idx in symbol_idxs:
            production = self.productions[symbol_idx][symbol]
            nullable, first_set = self.first_production(production, symbol)
            first_ = first_set | first_
            nullable_ = nullable or nullable_

        return nullable_, first_

    def first_production(self, production, symbol=None) -> Tuple[bool, Set]:
        first_ = set()

        if symbol is not None:
            # We check if its left recursive
            if production[0] == symbol:
                # return False, set()
                is_nullable, first_set_ = self.handle_left_recursion(symbol)
                return is_nullable, first_set_

        idx = 0
        nullable = True

        while nullable:
            if idx < len(production):
                nullable, first_set = self.first(production[idx])
                first_ = first_ | first_set
                idx += 1
            else:
                return True, first_

        first_ = first_ - {EPSILON}
        return False, first_

    def handle_left_recursion(self, symbol) -> Tuple[bool, Set]:
        # We find the productions that are left recursive
        left_recursive_productions_idxs = set()
        production_idxs = self.production_adress[symbol]
        for production_idx in production_idxs:
            if self.productions[production_idx][symbol][0] == symbol:
                left_recursive_productions_idxs.add(production_idx)

        # if there is more than one production that is left recursive
        if len(left_recursive_productions_idxs) > 1:
            raise Exception("There are more than one left recursive productions")

        # We find the first set of the non left recursive productions
        first_ = set()
        nullable_ = False
        for production_idx in production_idxs:
            if production_idx not in left_recursive_productions_idxs:
                production = self.productions[production_idx][symbol]
                nullable, first_set = self.first_production(production, symbol)
                first_ = first_set | first_
                nullable_ = nullable or nullable_

        if nullable_:
            for left_recursive_production_idx in left_recursive_productions_idxs:
                nullable = True
                production = self.productions[left_recursive_production_idx][symbol]
                if len(production) > 1:
                    idx = 1

                    while nullable:
                        if idx < len(production):
                            nullable, first_set = self.first(production[idx])
                            first_ = first_ | first_set
                            idx += 1
                        else:
                            return True, first_

                    first_ = first_ - {EPSILON}
                    return False, first_

        return nullable_, first_

    def follow(self):
        def get_follow_set_length(follow_set_):
            size = 0
            for value in follow_set_.values():
                size += len(value)

            return size

        key, _, _ = self.decode_grammar_item((0, 0))
        follow_set = {key: ENDMAKER}

        old_len = 0
        new_len = get_follow_set_length(follow_set)

        while new_len != old_len:
            old_len = new_len
            for full_production in self.productions:
                symbol = list(full_production.keys())[0]
                production = full_production[symbol]

                for index, symbol in enumerate(production):

                    # Si es el primer elemento de la produccion
                    # if index == 0:
                    #     continue
                    if symbol not in self.non_terminals:
                        continue

                    # Si el elemento es el ultimo de la produccion
                    if index == len(production) - 1:
                        continue

                    lookahead = production[index + 1]
                    nullable, first_set = self.first(lookahead)
                    if nullable:
                        first_set = first_set - {EPSILON}
                        # TODO: manejar el caso, todo lo que es follow de rhs es follow de lhs
                        if lookahead in follow_set and symbol in follow_set:
                            follow_set[symbol] = follow_set[symbol] | follow_set[lookahead]
                        elif lookahead in follow_set:
                            follow_set[symbol] = follow_set[lookahead]

                    if symbol in follow_set:
                        follow_set[symbol] = follow_set[symbol] | first_set
                    else:
                        follow_set[symbol] = first_set

                new_len = get_follow_set_length(follow_set)

        return follow_set
