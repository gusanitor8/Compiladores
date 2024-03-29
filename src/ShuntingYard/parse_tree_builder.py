from src.ShuntingYard.tree_node import TreeNode


class ParseTree:
    def __init__(self, postfix_regex: str, display_tree=False, suffix=""):
        self.postfix_regex = postfix_regex
        self.unary_operators = ['?', '*', '+']
        self.binary_operators = ['|', '.']

        self._nodes: set = set()
        self._tree: TreeNode = self._build_tree()

        if display_tree:
            self.print_tree(suffix=suffix)

    def get_nodes(self):
        return self._nodes

    def get_tree(self):
        return self._tree

    def print_tree(self, suffix=""):
        self._tree.print_tree(suffix)

    def _build_tree(self):
        """
        Builds the parse tree
        :return: TreeNode
        """
        stack = []
        try:
            index = 0
            while index < len(self.postfix_regex):
                char = self.postfix_regex[index]

                # if the char is scaped
                if char == "'":
                    if index + 2 < len(self.postfix_regex):
                        if self.postfix_regex[index + 2] == "'":
                            new_char = "'" + self.postfix_regex[index + 1] + "'"
                            node = TreeNode(value=new_char)
                            stack.append(node)
                            self._nodes.add(node)  # Add the node to the set of nodes
                            index += 3
                            continue


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
                index += 1

            return stack.pop()
        except IndexError:
            raise Exception("Invalid Regular Expression")
