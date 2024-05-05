from src.yalex.Yalex import Yalex
from src.regex.regex import Regex
from src.Automatas.Automata import DeterministicFiniteAutomata, Automata
from src.Automatas.Node import Node
from src.constants import EPSILON
from dataclasses import dataclass
from src.LexicalAnalizerGenerator.LexicalCode import *
import pickle
import os

OUT_PATH = "./lexicalOut/"



@dataclass
class LexicalAutomata:
    automata: Automata
    actions: dict
    final_node_precedence: dict


class LexicalAnalizerGenerator:
    def __init__(self, yalex_path: str, output_name: str):
        self.document = Yalex(yalex_path).get_document()
        self.format_header_trailer()
        self.output_name = output_name
        self.final_node_precedence = {}
        self.afn, self.actions = self.make_big_automata()
        self._serialize_automata()

    def get_document(self):
        return self.document

    def format_header_trailer(self):
        header = self.document["header-trailer"][0]
        trailer = self.document["header-trailer"][1]

        new_header = ""
        for line in header.split("\n"):
            new_header += "" + line + "\n"

        new_trailer = ""
        for line in trailer.split("\n"):
            new_trailer += "    " + line + "\n"

        self.document["header-trailer"][0] = new_header
        self.document["header-trailer"][1] = new_trailer


    def make_mini_automatas(self):
        rules = self.document["entrypoint"]["code"]
        variables = self.document["variables"]
        identifier_order = self.document["entrypoint"]["token_order"]
        final_node_precedence = {}
        dfas_actions = {}

        for identifier in rules.keys():
            if identifier in variables:
                dfa: DeterministicFiniteAutomata = Regex.build_dfa(variables[identifier])
                dfas_actions[dfa] = rules[identifier]
                for final in dfa.get_final():
                    final_node_precedence[final] = identifier_order[identifier]
            else:
                dfa: DeterministicFiniteAutomata = Regex.build_dfa(identifier)
                dfas_actions[dfa] = rules[identifier]
                for final in dfa.get_final():
                    final_node_precedence[final] = identifier_order[identifier]

        self.final_node_precedence = final_node_precedence



        return dfas_actions

    def make_big_automata(self):
        mini_automatas = self.make_mini_automatas()

        initial_node = Node()
        final_nodes = set()
        actions = {}
        alphabet = set()
        states = set()

        # We add an epsilon transition from the initial node to the initial node of each mini automata
        for dfa, action in mini_automatas.items():
            initial_node.add_transition(EPSILON, dfa.get_initial())
            alphabet = alphabet.union(dfa.get_alphabet())
            states = states.union(dfa.get_states())

            # We associate the final nodes of a dfa to its action through a dictionary
            for final in dfa.get_final():
                actions[final] = action

        # We add all the final nodes of the mini automatas to the final nodes of the big automata
        for dfa in mini_automatas.keys():
            final_nodes = final_nodes.union(dfa.get_final())

        afn = Automata(initial_node, final_nodes)
        afn.add_alphabet(alphabet)
        afn.add_states(states)

        return afn, actions

    def make_dfa(self, regex: str):
        return Regex.build_dfa(regex)

    def _serialize_automata(self):
        new_dir = "./" + OUT_PATH + self.output_name
        os.makedirs(new_dir, exist_ok=True)
        new_file_path_py = new_dir + "/lexicalAnalizer.py"
        pickle_file_path = new_dir + "/lexicalAnalizer.pkl"

        # We make the automata object to serialize
        lexical_automata = LexicalAutomata(self.afn, self.actions, self.final_node_precedence)

        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(lexical_automata, pickle_file)

        with open(new_file_path_py, 'w') as file:
            file.write(IMPORTS)
            file.write(self.document["header-trailer"][0])
            file.write(LEXICAL_ANALYZER_CODE)
            file.write(MIDDLE)
            file.write(self.document["header-trailer"][1])
