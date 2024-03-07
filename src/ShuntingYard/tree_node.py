from graphviz import Graph


class TreeNode:
    latest_id = 0
    tree_graph = Graph(format='png')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

        TreeNode.latest_id += 1
        self.id = TreeNode.latest_id

    def make_tree(self):
        """
        This method shouldn't be called directly. It's called by the TreeNode class to make the tree
        To render the tree, call the print_tree method
        :return:
        """
        TreeNode.tree_graph.node(str(self.id), self.value)

        if self.left:
            TreeNode.tree_graph.edge(str(self.id), str(self.left.id))
            self.left.make_tree()

        if self.right:
            TreeNode.tree_graph.edge(str(self.id), str(self.right.id))
            self.right.make_tree()

    @staticmethod
    def _render_tree():
        """
        This method renders the tree on the screen
        :return:
        """
        TreeNode.tree_graph.render('out/tree', view=True)

    def print_tree(self):
        """
        This method displays the tree
        :return:
        """
        self.make_tree()
        self._render_tree()
