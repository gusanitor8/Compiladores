from typing import List, Dict, Set, Tuple
from graphviz import Digraph


class Builder:
    def __init__(self, grammar: List[Dict], grammar_adresses: Dict[str, List[int]]):
        self.grammar = grammar
        self.lhs_set = grammar_adresses

        # manage symbols
        self.symbols = self._get_symbols()
        self.terminals = set()
        self.non_terminals = set()
        self._classify_symbols()

        self.initial_set = self._get_initial_item()

    def _classify_symbols(self):
        for symbol in self.symbols:
            if symbol.islower():
                self.non_terminals.add(symbol)
            else:
                self.terminals.add(symbol)

    def _decode_item(self, item: Tuple) -> Tuple:
        """
        This method decodes an item
        :param item: Tuple
        :return:
        """
        key = list(self.grammar[item[0]].keys())[0]
        production = self.grammar[item[0]][key]
        dot_position = item[1]
        return key, production, dot_position

    def _augment_grammar(self):
        """
        This method augments the grammar by adding a new production S' -> S where S is the start symbol
        :return:
        """
        start_symbol = list(self.grammar[0].keys())[0]
        self.grammar.insert(0, {"S'": [start_symbol]})

        for key in self.lhs_set.keys():
            self.lhs_set[key] = [i + 1 for i in self.lhs_set[key]]

        self.lhs_set["S'"] = [0]

    def _get_initial_item(self) -> Set:
        if len(self.grammar) > 0:
            dic = self.grammar[0]
            keys = list(dic.keys())
            lista = dic[keys[0]]

            if len(lista) > 0:
                return {(0, 0)}

        raise Exception("Grammar is empty")

    def _get_symbols(self) -> Set:
        symbols = set()

        for dic in self.grammar:
            for key in dic.keys():
                for symbol in dic[key]:
                    symbols.add(symbol)

        return symbols

    def closure(self, item_set: Set[Tuple]) -> Set:
        """
        This method returns the closure of an item set
        :param item_set: an item set is a set of tuples with two elements the former
        is the index of the production and the latter is the index of the dot
        :return:
        """
        res = item_set.copy()
        j = list(item_set)

        while j:
            item = j.pop(0)
            key = list(self.grammar[item[0]].keys())[0]

            if len(self.grammar[item[0]][key]) - 1 >= item[1]:  # If the dot is not at the end of the production
                symbol = self.grammar[item[0]][key][item[1]]

                if symbol not in self.lhs_set:  # If the symbol is a terminal
                    continue

                for symbol_indexes in self.lhs_set[symbol]:
                    if (symbol_indexes, 0) not in res:
                        j.append((symbol_indexes, 0))
                        res.add((symbol_indexes, 0))

        return res

    def go_to(self, item_set: Set, symbol: str) -> Set:
        """
        This method returns the goto of an item set
        :param item_set: an item set is a set of tuples with two elements the former
        is the index of the production and the latter is the index of the dot
        :param symbol: str
        :return:
        """
        res = set()

        for item in item_set:
            key = list(self.grammar[item[0]].keys())[0]
            production = self.grammar[item[0]][key]

            if len(production) > item[1]:  # If the dot is not at the end of the production
                if production[item[1]] == symbol:
                    res.add((item[0], item[1] + 1))

        return self.closure(res)

    # def get_item_sets(self) -> List[Set]:
    #     """
    #     This method returns the item sets of the LR(0) automaton
    #     :return:
    #     """
    #     self._augment_grammar()
    #     initial_item = self._get_initial_item()
    #     initial_set = self.closure(initial_item)
    #     grammar_symbols = self._get_symbols()
    #     c = {frozenset(initial_set)}
    #     c_copy = list(c.copy())
    #
    #     while c_copy:
    #         item_set = c_copy.pop(0)
    #         for symbol in grammar_symbols:
    #             goto = self.go_to(item_set, symbol)
    #             if goto and goto not in c:
    #                 c.add(frozenset(goto))
    #                 c_copy.append(goto)
    #
    #     return list(c)

    def get_item_sets(self):
        """
        This method returns the item sets of the LR(0) automaton
        :return:
        """
        self._augment_grammar()
        initial_item = self._get_initial_item()
        initial_set = self.closure(initial_item)
        grammar_symbols = self._get_symbols()
        c = {frozenset(initial_set)}
        c_copy = list(c.copy())

        index_set_dic = {0: initial_set}
        set_index_dic = {frozenset(initial_set): 0}
        lr0 = {}
        counter = 1

        while c_copy:
            item_set = c_copy.pop(0)
            for symbol in grammar_symbols:
                goto = self.go_to(item_set, symbol)
                if goto:
                    if goto not in c:
                        c.add(frozenset(goto))
                        c_copy.append(goto)

                        index_set_dic[counter] = goto
                        set_index_dic[frozenset(goto)] = counter

                        orig_idx = set_index_dic[frozenset(item_set)]

                        if orig_idx in lr0:
                            lr0[orig_idx][symbol] = counter
                        else:
                            lr0[orig_idx] = {symbol: counter}

                        counter += 1
                    else:
                        orig_idx = set_index_dic[frozenset(item_set)]
                        dest_idx = set_index_dic[frozenset(goto)]

                        if orig_idx in lr0:
                            lr0[orig_idx][symbol] = dest_idx
                        else:
                            lr0[orig_idx] = {symbol: dest_idx}

        return index_set_dic, lr0

    def draw_automaton(self, index_set_dic, lr0, filename:str  = 'LR0_prueba'):
        automaton = Digraph('automaton', node_attr={'shape': 'record'}, format='png')

        for idx, item_set in index_set_dic.items():
            item_html = f'<<I>I</I><SUB>{idx}</SUB><BR/>'

            for item in item_set:
                head, body, dot_position = self._decode_item(item)

                item_html += f'<I>{head}</I> &#8594; '

                for symbol_idx, symbol in enumerate(body):

                    if symbol_idx == dot_position:
                        item_html += f'&#8226; '
                    if symbol in self.non_terminals:
                        item_html += f'<I>{symbol}</I>'
                    elif symbol in self.terminals:
                        item_html += f'<B>{symbol}</B>'
                    else:
                        item_html += f'{symbol}'

                    if symbol_idx >= len(body) - 1 and dot_position == len(body):
                        item_html += f'&#8226;'

                item_html += '<BR ALIGN="LEFT"/>'
            automaton.node(f'I{idx}', f'{item_html}>')

        for node_idx, transitions in lr0.items():
            for symbol, dest_idx in transitions.items():
                automaton.edge(f'I{node_idx}', f'I{dest_idx}', label=symbol)

        automaton.render(filename=f'{filename}', directory="./out/lr0_out/", cleanup=True, format='png', view=True)
        print('Automata LR(0) generado exitosamente, guardado en /lr0_out')
