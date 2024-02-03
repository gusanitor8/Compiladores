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

    def _followpos(self, node: TreeNode):
        pass

    def _create_initial_dfa_state(self):
        pass

    def _transition_table(self):
        pass

    def _final_states(self):
        pass
