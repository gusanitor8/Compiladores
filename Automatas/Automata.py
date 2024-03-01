from Automatas.Node import Node
from typing import Set
from graphviz import Digraph

EPSILON = '𝜀'


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
