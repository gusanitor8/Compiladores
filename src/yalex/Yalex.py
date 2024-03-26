from src.regex.regex import Regex
from src.Automatas.Automata import Automata
from src.Automatas.Node import Node
from src.constants import EPSILON


class Yalex:
    def __init__(self, filename="./utils/yalex_files/slr-2.yal"):
        self.yal = self._read_yal(filename)
        self.string = str(self.yal)
        self.nfa: Automata = self._build_nfa()
        self.final_precedence = {}
        self.actions = {}

    @staticmethod
    def _read_yal(filename):
        """
        Reads the yal file
        :param filename: the path where the yal file is located
        :return: string with the content of the file
        """
        with open(filename, 'r') as f:
            data = f.read()

        return data

    def _build_nfa(self):
        """
        Generates de nfa which unites all the dfas for recognizing comments, variables and the entrypoint
        :return: nfa: Automata
        """
        any = '(' + Regex.generate_char_set_with_separator('!', '~') + '| )'
        az = "(" + Regex.generate_char_set_with_separator('a', 'z') + ")"
        azaz09 = "(" + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9') + ")"

        comment_dfa = Regex("'(''*'" + any + "'*'')'").get_dfa()
        variable_dfa = Regex("let +" + az + azaz09 + "* *= *" + any + "+\n").get_dfa()
        entrypoint_dfa = Regex("rule +" + az + azaz09 + "* += *\n").get_dfa()  # TODO: Add support for args

        # We add the initial node of the nfa and connect it to the initial nodes of the other dfas
        initial_node = Node()
        initial_node.add_transition(EPSILON, variable_dfa.get_initial())
        initial_node.add_transition(EPSILON, entrypoint_dfa.get_initial())
        initial_node.add_transition(EPSILON, comment_dfa.get_initial())

        # We obtain the parameters for the new nfa
        final_nodes = comment_dfa.get_final() + variable_dfa.get_final() + entrypoint_dfa.get_final()
        alphabet = comment_dfa.get_alphabet() + variable_dfa.get_alphabet() + entrypoint_dfa.get_alphabet()
        nodes = comment_dfa.get_nodes() + variable_dfa.get_nodes() + entrypoint_dfa.get_nodes()

        # We associate each of the final nodes with an action
        for final in comment_dfa.get_final():
            self.actions[final] = self._comment_found

        for final in variable_dfa.get_final():
            self.actions[final] = self._variable_found

        for final in entrypoint_dfa.get_final():
            self.actions[final] = self._entrypoint_found

        # We create the nfa
        nfa = Automata(initial_node, final_nodes)
        nfa.add_alphabet(alphabet)
        nfa.add_states(nodes)

        # Set precedence for each final node
        final_nodes_list = [entrypoint_dfa, variable_dfa, comment_dfa.get_nodes()]
        for index, set_ in enumerate(final_nodes_list):
            for node in set_:
                self.final_precedence[node] = index

        return nfa

    def _comment_found(self):
        pass

    def _variable_found(self):
        pass

    def _entrypoint_found(self):
        pass

    def _cut_string(self):
        self.string = self.string[1:]

    def _longest_match(self):
        longest_match_index = 0
        longest_match_state = None
        initial = self.nfa.get_initial()
        current = Automata.e_closure(initial)

        # We search for the longest match in the string
        for index, char in enumerate(self.string):
            if any(state in self.nfa.get_final() for state in current):
                longest_match_index = index + 1  # +1 because is exclusive in the tuple
                longest_match_state = current.intersection(self.nfa.get_final())

            current = Automata.move(current, char)
            current = Automata.e_closure(current)

            if not current:
                break

        # We pick the final node based on the precedence of the answer
        if longest_match_state:
            longest_match_state = max(longest_match_state, key=lambda x: self.final_precedence[x])
        else:
            return None

        response = {
            "node": longest_match_state,
            "start": 0,
            "end": longest_match_index
        }

        return response


