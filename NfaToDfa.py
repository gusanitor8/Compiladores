from Automata import DeterministicFiniteAutomata, Automata
from Node import Node, EPSILON
from typing import Set


class NfaToDfa:
    def __init__(self, afn: Automata):
        self.DFA_states = {}
        self.initial_DFA_state: Node = None
        self.afn = afn

    def make_dfa(self):
        initial_eclosure = self.get_eclosure({self.afn.get_initial()})
        initial_afd_node = Node()
        self.initial_DFA_state = initial_afd_node
        self.DFA_states[frozenset(initial_eclosure)] = initial_afd_node

        def visit(afd_node_signature: Set[Node]):
            for letter in self.afn.get_alphabet():
                afn_states_reached_by_letter = NfaToDfa.get_letter_closure(initial_eclosure, letter)
                eclosure = self.get_eclosure(afn_states_reached_by_letter)

                if frozenset(eclosure) in self.DFA_states:
                    destination_afd_node = self.DFA_states[frozenset(eclosure)]
                    origin_afd_node = self.DFA_states[frozenset(afd_node_signature)]
                    origin_afd_node.add_transition(letter, destination_afd_node)
                else:
                    self.DFA_states[frozenset(eclosure)] = Node()
                    destination_afd_node = self.DFA_states[frozenset(eclosure)]
                    origin_afd_node = self.DFA_states[frozenset(afd_node_signature)]
                    origin_afd_node.add_transition(letter, destination_afd_node)
                    visit(eclosure)

        visit(initial_eclosure)

    def get_dfa(self):
        self.make_dfa()
        final_afd_nodes = set()

        for sets, node in self.DFA_states.items():
            if self.afn.get_final() in sets:
                final_afd_nodes.add(node)

        dfa = DeterministicFiniteAutomata(self.initial_DFA_state, final_afd_nodes)
        return dfa

    @staticmethod
    def _get_e_closure(initial_node: Node):
        e_closure = set()
        visited_nodes = set()

        def visit(node: Node):
            if node in visited_nodes:
                return

            visited_nodes.add(node)
            for transition in node.transitions[EPSILON]:
                e_closure.add(transition)
                visit(transition)

        visit(initial_node)
        e_closure.add(initial_node)
        return e_closure

    def get_eclosure(self, afn_nodes: Set[Node]):
        e_closure = set()
        for node in afn_nodes:
            e_closure = e_closure.union(self._get_e_closure(node))
        return e_closure

    @staticmethod
    def get_letter_closure(afn_nodes: Set[Node], letter: str):
        letter_closure = set()
        for node in afn_nodes:
            if letter in node.transitions and letter != EPSILON:
                letter_closure.add(node.transitions[letter])

        return letter_closure
