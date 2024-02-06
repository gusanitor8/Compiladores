from ShuntingYard.tree_node import TreeNode

EPSILON = '𝜀'


class DirectConstruction:
    def __init__(self, parse_tree: TreeNode, nodes: set):
        self.nodes = nodes
        self.parse_tree = self._normalize_tree(parse_tree)
        self.parse_tree.print_tree()

        self.node_positions = self._set_node_positions()
        self._nullable_nodes = self._nullable()
        self.first_positions = self._firstpos()


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

    def _followpos(self, node: TreeNode, follow_pos_dict: dict):  
        '''
        This method calculates the followpos of the nodes in the parse tree
        :param node: TreeNode
        :param follow_pos_dict: dict
        :return: None'''
        if node.value == '.':
            for pos in self._lastpos(node.left):
                follow_pos_dict.setdefault(pos, set()).update(self._firstpos(node.right))
        elif node.value == '*':
            for pos in self._lastpos(node.left):
                follow_pos_dict.setdefault(pos, set()).update(self._firstpos(node.left))
        elif node.value == '#':
            pass  # '#' node does not have any follow positions
        elif node.value not in [EPSILON, '|']:
            pass  # other leaf nodes don't need follow positions

    def _create_initial_DFA_state(self):
        # initial_state = self.first_positions[self.parse_tree]  # Initial state is the firstpos of the root node
        # return initial_state
        pass


    def _transition_table(self):
        # transition_table = {}

        # for node, firstpos in self.first_positions.items():
        #     for symbol in alphabet:  # You need to define your alphabet
        #         next_state = set()
        #         for pos in firstpos:
        #             # Get the followpos of the position for the given symbol
        #             if pos in self.followpos and symbol in self.followpos[pos]:
        #                 next_state.update(self.followpos[pos][symbol])
        #         transition_table[(node, symbol)] = next_state

        # return transition_table
        pass
    
    def _final_states(self):
        # final_states = []

        # for node, firstpos in self.first_positions.items():
        #     if self.node_positions[self.parse_tree] in firstpos:
        #         final_states.append(node)

        # return final_states

        pass
