from src.Automatas.Node import Node
from typing import Set
from graphviz import Digraph
from src.constants import EPSILON

class Automata:
    def __init__(self, initial: Node, final: Node):
        self._initial = initial
        self._final = final
        self._states = set()
        self._alphabet = set()

    def print_automata(self, file_id: str = ''):
        """
        This method prints the automata on the screen and saves it as a .png file
        :return: None
        """
        graph: Digraph = self._initial.render_automata()

        # final
        graph.node(str(self._final.id), shape='doublecircle')

        # initial
        graph.node('invisible_node', label='', width='0', height='0', style='invis')
        graph.edge('invisible_node', str(self._initial.id), label='')

        graph.render('out/automata' + file_id, view=True)

    def add_states(self, states: Set[Node]):
        """
        Sets the set of nodes that represent all the states of the automata
        :param states: Set[Node]
        :return: None
        """
        self._states.update(states)

    def add_alphabet(self, alphabet: Set[str]):
        """
        Sets the alphabet of the automata
        :param alphabet: Set[str]
        :return: None
        """
        self._alphabet.update(alphabet)

    def get_states(self):
        """
        Returns the set of nodes that represent all the states of the automata
        :return: Set[Node]
        """
        return self._states

    def get_alphabet(self):
        """
        Returns the alphabet of the automata
        :return: Set[str]
        """
        return self._alphabet

    def get_initial(self):
        """
        Returns the initial state of the automata
        :return: Node
        """
        return self._initial

    def get_final(self):
        """
        Returns the final state of the automata
        :return: Node
        """
        return self._final


class DeterministicFiniteAutomata:
    def __init__(self, initial: Node, final: set[Node]):
        self._initial = initial
        self._final = final
        self._states = set()
        self._alphabet = set()

    def print_automata(self, file_id: str = ""):
        """
        This method prints the automata on the screen and saves it as a .png file
        :return: None
        """
        graph: Digraph = self._initial.render_automata()

        # final
        for final_node in self._final:
            graph.node(str(final_node.id), shape='doublecircle')

        # initial
        graph.node('invisible_node', label='', width='0', height='0', style='invis')
        graph.edge('invisible_node', str(self._initial.id), label='')

        graph.render('out/automata' + file_id, view=True)

    def remove_dead_states(self):
        """
        This method removes the dead states from the automata
        :return: None
        """
        states = self.get_states()
        dead_states = self._identify_dead_states()

        for state in states:
            for key in self._alphabet:
                node = state.transitions[key]
                if node in dead_states:
                    del state.transitions[key]

        self._states = self._states - dead_states


    def _identify_dead_states(self):
        """
        This method identifies the dead states of the automata
        :return: a set of the dead states
        """
        states = self.get_states() - self.get_final()
        alphabet = self.get_alphabet()
        dead_states = set()

        for state in states:
            # if the state has no transitions then its a dead state
            if state.transitions == {EPSILON: []}:
                dead_states.add(state)
                continue

            # if the state has only transitions to itself then its a dead state
            for char in alphabet:
                if state.transitions[char] is not state:
                    break
                dead_states.add(state)

        return dead_states


    def add_states(self, states: Set[Node]):
        """
        Sets the set of nodes that represent all the states of the automata
        :param states: Set[Node]
        :return: None
        """
        self._states.update(states)

    def add_alphabet(self, alphabet: Set[str]):
        """
        Sets the alphabet of the automata
        :param alphabet: Set[str]
        :return: None
        """
        self._alphabet.update(alphabet)

    def get_states(self):
        """
        Returns the set of nodes that represent all the states of the automata
        :return: Set[Node]
        """
        return self._states

    def get_alphabet(self):
        """
        Returns the alphabet of the automata
        :return: Set[str]
        """
        return self._alphabet

    def get_initial(self):
        """
        Returns the initial state of the automata
        :return: Node
        """
        return self._initial

    def get_final(self):
        """
        Returns the final state of the automata
        :return: Node
        """
        return self._final
