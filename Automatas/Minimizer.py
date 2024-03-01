from Automatas.Automata import DeterministicFiniteAutomata
from typing import Set, Dict, FrozenSet
from Automatas.Node import Node, EPSILON


class Minimizer:
    def __init__(self, dfa: DeterministicFiniteAutomata):
        self.dfa = dfa
        self.partitions = self._minimize()


    def _minimize(self):
        new_partition = [self.dfa.get_final(), self.dfa.get_states() - self.dfa.get_final()]
        initial_partition = []

        while new_partition != initial_partition:
            initial_partition = new_partition
            new_partition = self._get_next_partition(new_partition)

        return new_partition

    def _get_next_partition(self, partition: [Set[Node]]):
        new_partition = []

        for index, group in enumerate(partition):
            group_a = set()
            group_b = set()

            for node in group:
                for a in self.dfa.get_alphabet():
                    if node.transitions[a] not in group:
                        group_a.add(node)
                        break
                else:
                    group_b.add(node)

            new_partition.append(group_a)
            new_partition.append(group_b)

        new_partition = [item for item in new_partition if item]
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
                break

        # initial state
        initial_state = partitions[node_group_dict[self.dfa.get_initial()]]

        # final states
        final_states = set()
        old_final_states = self.dfa.get_final()
        for group, new_node in partitions.items():
            if group.issubset(old_final_states):
                final_states.add(new_node)

        return DeterministicFiniteAutomata(initial_state, final_states)
