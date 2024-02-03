from ShuntingYard.tree_node import TreeNode


class ParseTree:
    def __init__(self, postfix_regex: str, display_tree=False):
        self.postfix_regex = postfix_regex
        self.unary_operators = ['?', '*', '+']
        self.binary_operators = ['|', '.']

        self._nodes: set = set()
        self._tree: TreeNode = self._build_tree()

    def get_nodes(self):
        return self._nodes

    def get_tree(self):
        return self._tree

    def print_tree(self):
        self._tree.print_tree()

    def _build_tree(self):
        """
        Builds the parse tree
        :return: TreeNode
        """
        stack = []
        try:
            for char in self.postfix_regex:
                if char in self.unary_operators:
                    node = TreeNode(value=char)
                    node.left = stack.pop()
                    stack.append(node)

                    self._nodes.add(node)  # Add the node to the set of nodes
                elif char in self.binary_operators:
                    node = TreeNode(value=char)
                    node.right = stack.pop()
                    node.left = stack.pop()
                    stack.append(node)

                    self._nodes.add(node)  # Add the node to the set of nodes
                else:
                    node = TreeNode(value=char)
                    stack.append(node)

                    self._nodes.add(node)  # Add the node to the set of nodes

            return stack.pop()
        except IndexError:
            raise Exception("Invalid Regular Expression")
