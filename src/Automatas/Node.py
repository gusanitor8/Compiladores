from graphviz import Digraph
from src.constants import EPSILON


class Node:
    _id_counter = 1

    def __init__(self):
        self.id = Node._id_counter
        self.transitions = {EPSILON: []}
        self.graph = Digraph(comment='Finite Automaton', format='png', graph_attr={'rankdir': 'LR'})

        Node._id_counter += 1

    def add_transition(self, symbol, node):
        """
        This method adds a transition to the node
        :param symbol: The symbol that triggers the transition
        :param node: The node to which the transition goes
        :return: None
        """
        if symbol == EPSILON:
            self.transitions[symbol].append(node)
        else:
            self.transitions[symbol] = node

    def add_transitions(self, transition_dict):
        """
        This method adds a dictionary of transitions to the node
        :param transition_dict: A dictionary of the form {symbol: Node}
        :return: None
        """
        for key, value in transition_dict.items():
            if key == EPSILON:
                trans = set(self.transitions[key])
                trans2 = set(value)
                trans_def = trans.union(trans2)
                self.transitions[key] = list(trans_def)
                continue

            self.add_transition(key, value)

    def _make_automata_image(self):
        """
        This method iterates through the whole automata and creates the graph
        :return: None
        """
        visited_nodes = set()

        def visit(node):
            if node in visited_nodes:
                return

            # se visitan los nodos
            visited_nodes.add(node)
            for key in node.transitions:
                if key == EPSILON:
                    for transition in node.transitions[key]:
                        visit(transition)
                else:
                    visit(node.transitions[key])

            # Se comienza a dibujar el grafo
            for key in node.transitions:
                if key == EPSILON:
                    for node_transition in node.transitions[EPSILON]:
                        self.graph.edge(str(node.id), str(node_transition.id), label=EPSILON)
                else:
                    self.graph.edge(str(node.id), str(node.transitions[key].id), label=key)

        visit(self)

    def render_automata(self):
        """
        This method returns the graph of the automata to be handled by the Automata class
        :return:
        """
        self._make_automata_image()
        return self.graph
