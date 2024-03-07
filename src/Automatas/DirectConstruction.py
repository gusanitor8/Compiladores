from src.ShuntingYard.tree_node import TreeNode
from src.Automatas.Node import Node
from src.Automatas.Automata import DeterministicFiniteAutomata
import graphviz
from src.constants import EPSILON


class DirectConstruction:
    def __init__(self, parse_tree: TreeNode, nodes: set):
        self.nodes = nodes
        self.parse_tree = self._normalize_tree(parse_tree)
        self.parse_tree.print_tree()

        self.node_positions = self._set_node_positions()
        self._nullable_nodes = self._nullable()
        self.first_positions = self._firstpos()
        self.last_positions = self._lastpos()
        self.follow_positions = self._followpos()

        # Inicializar el conjunto de estados de aceptación
        self.accepting_states = set()

        # Construir DFA después de inicializar todos los atributos necesarios
        self.dfa = self._construct_dfa()

        self.dfa = self.get_dfa()


    def _normalize_tree(self, tree: TreeNode):
        """
        This method normalizes the tree by adding a '.' at the root of the tree
        where the left child is the tree and the right child is the '#' symbol
        :param tree: TreeNode
        :return: TreeNode
        """
        concat_node = TreeNode('.')
        concat_node.left = tree
        hashtag_node = TreeNode('#')
        concat_node.right = hashtag_node

        # Adds the nodes to the set of nodes
        self.nodes.add(concat_node)
        self.nodes.add(hashtag_node)

        return concat_node

    def _set_node_positions(self):
        """
        This methods sets a position (or id) to each outer leaf node in the tree
        :return: a dictionary of the form {position: TreeNode}
        """
        index = 0  # This is the position of the node in the tree
        node_positions = {}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                nonlocal index
                node_positions[node] = index
                index += 1

        visit(self.parse_tree)
        return node_positions

    def _nullable(self):
        """
        This method returns a dictionary of the form {TreeNode: bool} where the value is True if the node is nullable
        :return:
        """
        nullable = {item: False for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value == EPSILON:
                    nullable[node] = True
            else:
                if node.value == '|':
                    nullable[node] = nullable[node.left] or nullable[node.right]
                elif node.value == '.':
                    nullable[node] = nullable[node.left] and nullable[node.right]
                elif node.value in ['?', '*']:
                    nullable[node] = True

        visit(self.parse_tree)
        return nullable

    def _firstpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of first positions
        :return:
        """
        first_positions = {item: set() for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value != EPSILON:
                    first_positions[node].add(self.node_positions[node])
            else:
                if node.value == '|':
                    first_positions[node] = first_positions[node.left].union(first_positions[node.right])
                elif node.value == '.':
                    if self._nullable_nodes[node.left]:
                        first_positions[node] = first_positions[node.left].union(first_positions[node.right])
                    else:
                        first_positions[node] = first_positions[node.left]
                elif node.value in ['?', '*']:
                    first_positions[node] = first_positions[node.left]

        visit(self.parse_tree)
        return first_positions

    def _lastpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of last positions
        :return:
        """
        last_positions = {item: set() for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value != EPSILON:
                    last_positions[node].add(self.node_positions[node])
            else:
                if node.value == '|':
                    last_positions[node] = last_positions[node.left].union(last_positions[node.right])
                elif node.value == '.':
                    if self._nullable_nodes[node.right]:
                        last_positions[node] = last_positions[node.left].union(last_positions[node.right])
                    else:
                        last_positions[node] = last_positions[node.right]
                elif node.value in ['?', '*']:
                    last_positions[node] = last_positions[node.left]

        visit(self.parse_tree)
        return last_positions

    def _followpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of follow positions
        :return: {TreeNode: set()}
        """
        follow_positions = {}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if node.value == '.':  # If the node is a concatenation node
                lastpos = self.last_positions[node.left]
                firstpos = self.first_positions[node.right]

                for pos in lastpos:
                    follow_positions[pos] = follow_positions.get(pos, set()).union(firstpos)

            elif node.value == '*':  # If the node is a kleene star node
                lastpos = self.last_positions[node]
                firstpos = self.first_positions[node]

                for pos in lastpos:
                    follow_positions[pos] = follow_positions.get(pos, set()).union(firstpos)

        visit(self.parse_tree)
        return follow_positions

    def _construct_dfa(self):
        # Calcular el alfabeto del DFA
        alphabet = set()
        for node in self.nodes:
            if node.value not in ['.', '|', '*', '?', EPSILON]:
                alphabet.add(node.value)

        # Inicializar con el estado inicial: firstpos de la raíz
        initial_state = frozenset(self.first_positions[self.parse_tree])
        self.states = {initial_state: {}}
        unmarked_states = [initial_state]  # Estados sin marcar (pendientes de procesar)

        # Diccionario de posiciones y nodos
        node_positions_inverse = {pos: node for node, pos in self.node_positions.items()}
        self.node_positions_inverse = node_positions_inverse

        # Mientras haya estados sin marcar
        while unmarked_states:
            current_state = unmarked_states.pop()  # Tomar un estado sin marcar y marcarlo
            # Para cada símbolo del alfabeto
            for symbol in alphabet:
                # Calcula el conjunto U de followpos para cada posición en current_state que corresponde al símbolo
                U = set()
                for pos in current_state:
                    node = self.node_positions_inverse[pos]
                    if node.value == symbol:
                        U.update(self.follow_positions.get(pos, set()))
                U = frozenset(U)
                # Si U no es un estado existente y no es un estado vacío, añádelo
                if U and U not in self.states:
                    self.states[U] = {}
                    unmarked_states.append(U)
                # Añadir transición si U no es un estado vacío
                if U:
                    self.states[current_state][symbol] = U

            # Identificar estados de aceptación
            if any(self.node_positions_inverse[pos].value == '#' for pos in current_state):
                self.accepting_states.add(current_state)

            # Eliminar el estado vacío si está presente
            if frozenset() in self.states:
                del self.states[frozenset()]

        return self.states


    def get_dfa(self):

        node_dict = {frozenset(state): Node() for state in self.states}

        for state in self.states:
            new_node = node_dict[frozenset(state)]

            for symbol, transition in self.states[state].items():
                new_node.add_transition(symbol, node_dict[frozenset(transition)])

        # Set the initial state
        new_initial = node_dict[frozenset(self.first_positions[self.parse_tree])]

        # Set the final states
        final_states = set()
        for state in self.accepting_states:
            new_final = node_dict[frozenset(state)]
            final_states.add(new_final)

        dfa = DeterministicFiniteAutomata(new_initial, final_states)

        return dfa

    # Esto es extra para imprimir el dfa y generar la imagen con label originales
    def print_dfa(self):
        for state, transitions in self.states.items():
            print(f"Estado {state}:")
            for symbol, dest_state in transitions.items():
                print(f"  Con {symbol} -> {dest_state}")


    def generate_dot_representation(self):
        dot = graphviz.Digraph()

        # Agregar estados
        for state, transitions in self.dfa.items():
            state_label = ', '.join(map(str, state))
            shape = 'doublecircle' if state in self.accepting_states else 'circle'
            dot.node(state_label, shape=shape)

        # Agregar transiciones
        for state, transitions in self.dfa.items():
            for symbol, next_state in transitions.items():
                state_label = ', '.join(map(str, state))
                next_state_label = ', '.join(map(str, next_state))
                dot.edge(state_label, next_state_label, label=str(symbol))

        return dot

    def render_dfa_graph(self, filename='dfa_graph'):
        dot = self.generate_dot_representation()
        dot.render('out/' + filename, format='png', cleanup=True)
