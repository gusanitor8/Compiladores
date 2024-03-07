from src.Automatas.Automata import Automata, DeterministicFiniteAutomata
from src.Automatas.Node import Node
from typing import Set
from src.constants import EPSILON


class DFASimulator:
    def __init__(self, dfa: DeterministicFiniteAutomata):
        self.dfa = dfa

    def simulate(self, string: str):
        """
        Simulates the DFA
        :param string: str
        :return: bool
        """
        current_state = self.dfa.get_initial()
        try:
            for symbol in string:
                current_state = current_state.transitions[symbol]
        except KeyError:
            print("Invalid string")
            return False

        return current_state in self.dfa.get_final()


class NFASimulator:
    def __init__(self, nfa: Automata):
        self.nfa = nfa

    def simulate(self, string: str):
        current_states = self._e_closure(self.nfa.get_initial())
        accepted = False

        for symbol in string:
            current_states = self._move(current_states, symbol)
            current_states = self._e_closure_set(current_states)

        if self.nfa.get_final() in current_states:
            accepted = True

        return accepted

    def _e_closure(self, s: Node) -> Set[Node]:
        visited = set()

        def visit(node: Node):
            if node in visited:
                return
            visited.add(node)
            for transition in node.transitions[EPSILON]:
                visit(transition)

        visit(s)
        return visited

    def _move(self, T: Set[Node], a: str):
        nodes_reached = set()

        for node in T:
            if (a in node.transitions) and (a != EPSILON):
                nodes_reached.add(node.transitions[a])

        return nodes_reached

    def _e_closure_set(self, T: Set[Node]) -> Set[Node]:
        e_closure_set = set()
        for node in T:
            e_closure_set = e_closure_set.union(self._e_closure(node))
        return e_closure_set
