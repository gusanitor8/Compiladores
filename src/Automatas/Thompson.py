from typing import Set
from src.Automatas.Automata import Automata
from src.Automatas.Node import Node
from src.constants import EPSILON, ESCAPE


class Thompson:
    def __init__(self, postfix_regex: str):
        self.postfix_regex = postfix_regex
        self.binary_operators = {'|': self._union, '.': Thompson._concatenation}
        self.unary_operators = {'*': self._kleine_star, '+': self._kleine_plus, '?': self.question_mark}
        self._nodes: Set[Node] = set()
        self.alphabet = set()

    def make_afn(self):
        """
        This method iterates through the postfix regex and creates the automata
        :return: Automata
        """
        stack: [Automata] = []
        len_regex = len(self.postfix_regex)

        i = 0
        while i < len_regex:
            char = self.postfix_regex[i]

            if char == "'":
                if i + 2 < len_regex:
                    if self.postfix_regex[i + 2] == "'":
                        stack.append(self._make_automata(self.postfix_regex[i + 1]))
                        if char != EPSILON:
                            self.alphabet.add(self.postfix_regex[i + 1])
                        i += 3
                        continue


            if char in self.unary_operators:
                function = self.unary_operators[char]
                automata = function(stack.pop())
                stack.append(automata)

            elif char in self.binary_operators:
                function = self.binary_operators[char]
                aut1 = stack.pop()
                aut2 = stack.pop()
                automata = function(aut2, aut1)
                stack.append(automata)

            else:
                stack.append(self._make_automata(char))
                if char != EPSILON:
                    self.alphabet.add(char)
            i += 1

        automata = stack.pop()
        automata.add_states(self._nodes)
        automata.add_alphabet(self.alphabet)
        return automata

    def create_node(self):
        """
        This method creates a new node and adds it to the set of nodes
        :return: Node
        """
        node = Node()
        self._nodes.add(node)
        return node

    def _kleine_star(self, automata: Automata):
        """
        This method creates a kleene star automata
        :param automata:
        :return: Automata
        """
        q = self.create_node()
        f = self.create_node()
        final = automata.get_final()
        initial = automata.get_initial()

        q.add_transition(EPSILON, automata.get_initial())
        q.add_transition(EPSILON, f)

        final.add_transition(EPSILON, f)
        final.add_transition(EPSILON, initial)

        return Automata(q, f)

    def _kleine_plus(self, automata: Automata):
        """
        This method creates a kleene plus automata
        :param automata:
        :return: Automata
        """
        q = self.create_node()
        f = self.create_node()
        initial = automata.get_initial()
        final = automata.get_final()

        q.add_transition(EPSILON, initial)
        final.add_transition(EPSILON, f)
        final.add_transition(EPSILON, initial)

        return Automata(q, f)

    def question_mark(self, automata: Automata):
        """
        This method creates a question mark automata
        :param automata:
        :return: None
        """
        q = self.create_node()
        f = self.create_node()
        initial = automata.get_initial()
        final = automata.get_final()

        q.add_transition(EPSILON, f)
        q.add_transition(EPSILON, initial)
        final.add_transition(EPSILON, f)

        return Automata(q, f)

    def _union(self, automata1: Automata, automata2: Automata):
        """
        This method creates a union automata, since its a binary operator, it receives two automatas
        :param automata1:
        :param automata2:
        :return: Automata
        """
        q = self.create_node()
        f = self.create_node()

        q.add_transition(EPSILON, automata1.get_initial())
        q.add_transition(EPSILON, automata2.get_initial())

        automata1.get_final().add_transition(EPSILON, f)
        automata2.get_final().add_transition(EPSILON, f)

        return Automata(q, f)

    @staticmethod
    def _concatenation(automata1: Automata, automata2: Automata):
        """
        This method creates a concatenation automata, since its a binary operator, it receives two automatas
        :param automata1:
        :param automata2:
        :return: Automata
        """
        # automata1.get_final().add_transition(EPSILON, automata2.get_initial())
        #
        # return Automata(automata1.get_initial(), automata2.get_final())

        t1 = automata1.get_final()
        t2 = automata2.get_initial()

        t1.add_transitions(t2.transitions)

        return Automata(automata1.get_initial(), automata2.get_final())

    def _make_automata(self, char: str):
        """
        This method creates an automata with a single character
        :param char:
        :return: Automata
        """
        q = self.create_node()
        f = self.create_node()

        q.add_transition(char, f)

        return Automata(q, f)
