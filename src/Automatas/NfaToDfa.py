from src.Automatas.Automata import DeterministicFiniteAutomata, Automata
from src.Automatas.Node import Node, EPSILON
from typing import Set, Dict, FrozenSet


class NfaToDfa:
    def __init__(self, nfa: Automata):
        self.nfa = nfa
        self.dfa = self._make_dfa(self._subset_construction())

    def get_dfa(self):
        return self.dfa

    def _make_dfa(self, states: Dict[FrozenSet[Node], Dict[str, Set[Node]]]):
        dfa_node_dict = {}

        for key, _ in states.items():
            afd_node = Node()
            dfa_node_dict[key] = afd_node

        for key, value in states.items():
            dfa_node = dfa_node_dict[key]
            for symbol, nodes in value.items():
                # dead states are generated here with the empty set
                dfa_destination = dfa_node_dict[frozenset(nodes)]
                dfa_node.add_transition(symbol, dfa_destination)

        # Set the final states
        final_states = set()
        nfa_final = self.nfa.get_final()
        for key, value in states.items():
            for node in key:
                if node is nfa_final:
                    final_states.add(dfa_node_dict[key])

        # Set the initial state
        initial = self._e_closure(self.nfa.get_initial())
        initial_state = dfa_node_dict[frozenset(initial)]

        # nodes
        nodes = set(dfa_node_dict.values())

        dfa = DeterministicFiniteAutomata(initial_state, final_states)
        dfa.add_alphabet(self.nfa.get_alphabet())
        dfa.add_states(nodes)

        return dfa

    def _subset_construction(self) -> Dict:
        unmarked = [self._e_closure(self.nfa.get_initial())]
        marked = {}

        while unmarked:
            T = unmarked.pop()
            marked[frozenset(T)] = {}

            for a in self.nfa.get_alphabet():
                U = self._e_closure_set(self._move(T, a))
                if frozenset(U) not in marked and U not in unmarked:
                    unmarked.append(U)
                marked[frozenset(T)][a] = U

        return marked

    def _encode_node_set(self, node_set):
        """
        This method encodes a set of nodes into a tuple for debugging
        :param node_set:
        :return:
        """
        encoded = []
        for node in node_set:
            encoded.append(node.id)

        encoded.sort()
        return tuple(encoded)

    def _print_marked(self, marked):
        """
        This method prints the marked dictionary for debugging purposes
        :param marked:
        :return:
        """
        for key, value in marked.items():

            print('[', end='')
            for setA in key:
                print(setA, end=" ")
            print(']: ')

            for char, nodes in value.items():
                print("\t", char, end=" -> ")
                print(" [", end="")
                for node in nodes:
                    print(node, end=", ")
                print("]")

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

    def _e_closure_set(self, T: Set[Node]) -> Set[Node]:
        e_closure_set = set()
        for node in T:
            e_closure_set = e_closure_set.union(self._e_closure(node))
        return e_closure_set

    def _move(self, T: Set[Node], a: str):
        nodes_reached = set()

        for node in T:
            if (a in node.transitions) and (a != EPSILON):
                nodes_reached.add(node.transitions[a])

        return nodes_reached
