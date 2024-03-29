from src.regex.regex import Regex
from src.Automatas.Automata import Automata
from src.Automatas.Node import Node
from src.constants import EPSILON, SPECIAL_SYMBOLS


class Yalex:
    def __init__(self, filename="./utils/yalex_files/slr-2.yal"):
        self.final_precedence = {}
        self.actions = {}

        self.yal = self._read_yal(filename)
        self.string = str(self.yal)
        self.nfa: Automata = self._build_nfa()

        # We store data from the yal file in this dictionary
        self.document = {
            "comments": [],
            "variables": {},
            "entrypoint": {
                "args": [],
                "code": {}
            }
        }

        self.document_iterator()
        self._regex_iterator()
        self.variable_replacement_nfa()
        self._variable_iterator()
        print(self.document)

    def get_document(self):
        return self.document

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
        any_nospace = '(' + Regex.generate_char_set_with_separator('!', '~') + ')'
        az = "(" + Regex.generate_char_set_with_separator('a', 'z') + ")"
        azaz09 = "(" + Regex.generate_char_set_with_separator('a', 'z', 'A', 'Z', '0', '9') + ")"

        comment_dfa = Regex("'(''*'" + any + "*'*'')'").get_dfa()
        variable_dfa = Regex("let +" + az + azaz09 + "* *= *" + any + "+\n").get_dfa()
        entrypoint_dfa = Regex("rule +" + az + azaz09 + "* += *\n").get_dfa()  # TODO: Add support for args
        rules_dfa = Regex(" *'|'? *" + any_nospace + "+ +{" + any + "*} *").get_dfa()

        # We add the initial node of the nfa and connect it to the initial nodes of the other dfas
        initial_node = Node()
        initial_node.add_transition(EPSILON, variable_dfa.get_initial())
        initial_node.add_transition(EPSILON, entrypoint_dfa.get_initial())
        initial_node.add_transition(EPSILON, comment_dfa.get_initial())
        initial_node.add_transition(EPSILON, rules_dfa.get_initial())

        # We obtain the parameters for the new nfa
        final_nodes = comment_dfa.get_final() | variable_dfa.get_final() | entrypoint_dfa.get_final() | rules_dfa.get_final()
        alphabet = comment_dfa.get_alphabet() | variable_dfa.get_alphabet() | entrypoint_dfa.get_alphabet() | rules_dfa.get_alphabet()
        nodes = comment_dfa.get_states() | variable_dfa.get_states() | entrypoint_dfa.get_states() | rules_dfa.get_states()

        # We associate each of the final nodes with an action
        for final in comment_dfa.get_final():
            self.actions[final] = self._comment_found

        for final in variable_dfa.get_final():
            self.actions[final] = self._variable_found

        for final in entrypoint_dfa.get_final():
            self.actions[final] = self._entrypoint_found

        for final in rules_dfa.get_final():
            self.actions[final] = self._rule_found

        # We create the nfa
        nfa = Automata(initial_node, final_nodes)
        nfa.add_alphabet(alphabet)
        nfa.add_states(nodes)

        # Set precedence for each final node
        final_nodes_list = [entrypoint_dfa.get_final(), variable_dfa.get_final(), rules_dfa.get_final(),
                            comment_dfa.get_final()]
        for index, set_ in enumerate(final_nodes_list):
            for node in set_:
                self.final_precedence[node] = index

        return nfa

    def _build_preprocess_nfa(self):
        any = '(' + Regex.generate_char_set_with_separator('!', '~') + '| )'
        any2 = '(' + Regex.generate_char_set_with_separator('!', '~') + '| |\n|\t)'
        charset_regex = "[('''" + any + "'''-'''" + any + "''')+]"
        charset_regex = Regex(charset_regex).get_dfa()

        charset_regex2 = "[\"" + any2 + "+\"]"
        charset_regex2 = Regex(charset_regex2).get_dfa()

        initial = Node()
        initial.add_transition(EPSILON, charset_regex.get_initial())
        initial.add_transition(EPSILON, charset_regex2.get_initial())

        for final in charset_regex.get_final():
            self.actions[final] = self._charset_range

        for final in charset_regex2.get_final():
            self.actions[final] = self._charset_individuals

        final_nodes = charset_regex.get_final() | charset_regex2.get_final()
        alphabet = charset_regex.get_alphabet() | charset_regex2.get_alphabet()
        nodes = charset_regex.get_states() | charset_regex2.get_states()

        charset_nfa = Automata(initial, final_nodes)
        charset_nfa.add_alphabet(alphabet)
        charset_nfa.add_states(nodes)

        final_nodes_list = [charset_regex.get_final(), charset_regex2.get_final()]
        for index, set_ in enumerate(final_nodes_list):
            for node in set_:
                self.final_precedence[node] = index

        return charset_nfa

    def _cut_string(self, cut=1):
        self.string = self.string[cut:]

    def variable_replacement_nfa(self):
        keys = self.document["variables"].keys()
        initial = Node()
        key_nfas = []

        for key in keys:
            key_nfa = Regex(key).get_dfa()
            initial.add_transition(EPSILON, key_nfa.get_initial())
            key_nfas.append(key_nfa)

        final_nodes = set()
        for key_nfa in key_nfas:
            final_nodes |= key_nfa.get_final()

        alphabet = set()
        for key_nfa in key_nfas:
            alphabet |= key_nfa.get_alphabet()

        nodes = set()
        for key_nfa in key_nfas:
            nodes |= key_nfa.get_states()

        for nfa_final in final_nodes:
            self.actions[nfa_final] = self._identifier_found

        for final in final_nodes:
            self.final_precedence[final] = 0

        nfa = Automata(initial, final_nodes)
        return nfa

    def _longest_match(self):
        longest_match_index = 0
        longest_match_state = None
        initial = self.nfa.get_initial()
        current = Automata.e_closure(initial)

        # We search for the longest match in the string
        for index, char in enumerate(self.string):
            if any(state in self.nfa.get_final() for state in current):
                # TODO: puede que sumar uno no sea lo mejor porque de todas formas se agrega en la iteracion siguiente
                longest_match_index = index  # +1 because is exclusive in the tuple
                longest_match_state = current.intersection(self.nfa.get_final())

            current = Automata.move(current, char)
            current = Automata.e_closure_set(current)

            if not current:
                break

        # We check if the last state is a final state
        if any(state in self.nfa.get_final() for state in current):
            longest_match_index = index + 1  # +1 because is exclusive in the tuple
            longest_match_state = current.intersection(self.nfa.get_final())

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

    def _replace_special_chars(self, string):
        for special in SPECIAL_SYMBOLS:
            string = string.replace(special[0], special[1])
        return string

    def _regex_iterator(self):
        self.nfa = self._build_preprocess_nfa()

        for variable, regex in self.document["variables"].items():
            regex = self._replace_special_chars(regex)
            self.string = regex
            self.longest_matches_preprocessing("variables", variable)

    def longest_matches_preprocessing(self, section: str, identifier: str):
        string_copy = str(self.string)
        self.document[section][identifier] = ""

        while self.string:
            match = self._longest_match()
            if match:
                function = self.actions[match["node"]]
                function(match, section, identifier)
                self._cut_string(match["end"])

            else:
                self.document[section][identifier] += self.string[0]
                self._cut_string(1)


    def document_iterator(self):
        while self.string:
            match = self._longest_match()
            if match:
                function = self.actions[match["node"]]
                function(match)
                self._cut_string(match["end"] - 1)
            else:
                self._cut_string(1)

        return self.document

    def _variable_iterator(self):
        self.nfa = self.variable_replacement_nfa()

        for variable, regex in self.document["variables"].items():
            regex = self._replace_special_chars(regex)
            self.string = regex
            self.longest_matches_preprocessing("variables", variable)

    # ~~~~~~~~~~ Action associated methods below ~~~~~~~~~~
    def _identifier_found(self, range_, section, identifier):
        string = self.string[range_["start"]:range_["end"]]
        print("identifier found: ", string)

        self.document[section][identifier] += self.document[section][string]

    def _charset_range(self, range_, section, identifier):
        string = self.string[range_["start"]:range_["end"]]
        print("charset range found: ", string)

        string = string[1:-1]
        split_strings = [string[i:i + 7] for i in range(0, len(string), 7)]
        for index in range(len(split_strings)):
            split_string = split_strings[index]
            split_string = split_string.split("-")
            split_string[0] = split_string[0].strip("'")
            split_string[1] = split_string[1].strip("'")
            split_strings[index] = split_string

        flattened_list = [item for sublist in split_strings for item in sublist]
        regex = "(" + Regex.generate_char_set_with_separator(*flattened_list) + ")"
        self.document[section][identifier] += regex

    def _charset_individuals(self, range_, section, identifier):
        string = self.string[range_["start"]:range_["end"]]
        print("charset individual found: ", string)

        string = string[2:-2]
        chars = []

        index = 0
        while index < len(string):
            if string[index] == "'":
                if (index + 2) < len(string):
                    if string[index + 2] == "'":
                        chars.append("'" + string[index + 1] + "'")
                        index += 3
                        continue
            chars.append(string[index])
            index += 1

        res = ""
        for char in chars:
            res += char
            res += "|"
        res = res[:-1]
        res = "(" + res + ")"
        self.document[section][identifier] += res

    def _comment_found(self, range):
        string = self.string[range["start"]:range["end"]]
        self.document["comments"].append(string)

        print("comment found: ", string)

    def _variable_found(self, range):
        string = self.string[range["start"]:range["end"] - 1]
        string = string.strip()
        variable, value = string.split("=")
        variable = variable[4:]
        variable = variable.strip()
        value = value.strip()

        self.document["variables"][variable] = value

        print("variable found: ", string)

    def _rule_found(self, range):
        string = self.string[range["start"]:range["end"]]
        print("rule found: ", string)

        any_nospace = '(' + Regex.generate_char_set_with_separator('!', '~') + ')'
        identifier_regex = Regex(" *'|'? *" + any_nospace + "+")
        range = identifier_regex.longest_match(string)

        identifier = string[range[0]:range[1]]
        identifier = identifier.strip()
        if identifier[0] == "|":
            identifier = identifier[1:]
            identifier = identifier.strip()

        regex = string[range[1]:]
        regex = regex.strip()

        self.document["entrypoint"]["code"][identifier] = regex

    def _entrypoint_found(self, range):
        string = self.string[range["start"]:range["end"] - 1]
        print("entrypoint found: ", string)
        pass
