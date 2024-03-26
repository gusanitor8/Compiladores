from src.Automatas.Automata import DeterministicFiniteAutomata
from typing import Set, Dict, FrozenSet
from src.Automatas.Node import Node
from src.constants import EPSILON


class Minimizer:
    def __init__(self, dfa: DeterministicFiniteAutomata):
        self.dfa = dfa
        self.partitions = self._minimize()

    def _minimize(self):
        initial_partition = []
        curr_partition = [self.dfa.get_final(), self.dfa.get_states() - self.dfa.get_final()]
        alphabet = self.dfa.get_alphabet()
        group_table = self.init_group_table(curr_partition)
        calculation_table = self._init_calculation_table(group_table, alphabet)

        while initial_partition != curr_partition:
            group_table = self._update_group_table(group_table, calculation_table)
            initial_partition = curr_partition
            curr_partition = self._make_new_partition(curr_partition, group_table)
            calculation_table = self._init_calculation_table(group_table, alphabet)

        return curr_partition

    def init_group_table(self, initial_partition):
        group_table = {}
        for index, group in enumerate(initial_partition):
            for node in group:
                group_table[node] = index
        return group_table

    def _init_calculation_table(self, group_table, alphabet):
        calculation_table = {}
        for node in group_table.keys():
            code = []
            for char in alphabet:
                try:
                    dest = node.transitions[char]
                    group_no = group_table[dest]
                    code.append(group_no)
                except KeyError:
                    print("WARNING: No hay transición para el símbolo", char, "en el nodo", node)
                    if len(set(group_table.values())) == 1:
                        code.append(1)
                    else:
                        code.append(0)  # 0 es el estado de rechazo por lo que no esta en la particion de los finales

            calculation_table[node] = tuple(code)

        return calculation_table

    def _update_group_table(self, group_table, calculation_table):
        code_index: dict = {item: i for i, item in enumerate(set(calculation_table.values()))}

        for node in group_table.keys():
            group_table[node] = code_index[calculation_table[node]]

        return group_table

    def _make_new_partition(self, partition, group_table):
        new_partition = []
        for group in partition:
            code_group = {}
            for node in group:
                if group_table[node] in code_group:
                    code_group[group_table[node]].add(node)
                else:
                    code_group[group_table[node]] = {node}

            for new_group in code_group.values():
                new_partition.append(new_group)

        return new_partition

    def _make_node_group_dictionary(self, partition: [Set[Node]]):
        node_group_dict = {}
        for group in partition:
            for node in group:
                node_group_dict[node] = frozenset(group)
        return node_group_dict

    def make_minimized_dfa(self):
        node_group_dict = self._make_node_group_dictionary(self.partitions)
        partitions: Dict[FrozenSet[Node], Node] = {frozenset(group): Node() for group in self.partitions}

        for group, fda_node in partitions.items():
            new_node = partitions[group]

            for old_node in group:
                for symbol, transition in old_node.transitions.items():
                    if symbol == EPSILON:
                        continue

                    new_node_destination = partitions[frozenset(node_group_dict[transition])]
                    new_node.add_transition(symbol, new_node_destination)
                break  # TODO: puede que haya un bug aqui, el break se sale hasta el primer ciclo for y no hasta el segundo

        # initial state
        initial_state = partitions[node_group_dict[self.dfa.get_initial()]]

        # final states
        final_states = set()
        old_final_states = self.dfa.get_final()
        for group, new_node in partitions.items():
            if group.issubset(old_final_states):
                final_states.add(new_node)

        nodes = set(partitions.values())
        dfa = DeterministicFiniteAutomata(initial_state, final_states)
        dfa.add_alphabet(self.dfa.get_alphabet())
        dfa.add_states(nodes)

        return dfa
