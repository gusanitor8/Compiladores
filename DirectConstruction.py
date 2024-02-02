from ShuntingYard.tree_node import TreeNode

EPSILON = '𝜀'

class DirectConstruction:
    def __init__(self, parse_tree: TreeNode):
        self.parse_tree = self._normalize_tree(parse_tree)
        self.node_positions = self._set_node_positions()
        self.first_positions = self._firstpos()
        self.parse_tree.print_tree()

    @staticmethod
    def _normalize_tree(tree: TreeNode):
        """
        This method normalizes the tree by adding a '.' at the root of the tree
        where the left child is the tree and the right child is the '#' symbol
        :param tree: TreeNode
        :return: TreeNode
        """
        concat_node = TreeNode('.')
        concat_node.left = tree
        concat_node.right = TreeNode('#')

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
                node_positions[index] = node
                index += 1

        visit(self.parse_tree)
        return node_positions

    def _nullable(self):
        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value == EPSILON:
                    pass
                pass

        visit(self.parse_tree)

    def _firstpos(self, node: TreeNode):
        return TreeNode("")  # TODO: Implement this method


    def _lastpos(self, node: TreeNode):
        pass

    def _followpos(self, node: TreeNode):
        pass

    def _create_initial_dfa_state(self):
        pass

    def _transition_table(self):
        pass

    def _final_states(self):
        pass
