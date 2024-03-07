from src.ShuntingYard.shunting_yard import ShuntingYard
from src.Automatas.NfaToDfa import NfaToDfa
from src.Automatas.Minimizer import Minimizer
from src.Automatas.Automata import Automata
from src.Automatas.Thompson import Thompson


class Regex:
    def __init__(self, regex: str):
        self.regex = regex
        self.dfa: Automata = self._build_dfa(regex)

    def search(self, string) -> bool:
        pass

    def match_finder(self, string: str):
        index = 0
        final_string = ""

        def get_next_char():
            nonlocal index, final_string
            if index < len(string):
                character = string[index]
                final_string += character
                index += 1
                return character
            return None

        current_state = self.dfa.get_initial()
        final_states = self.dfa.get_final()

        while current_state not in final_states:
            char = get_next_char()
            if char is None:
                return False

        return final_string

    @staticmethod
    def _build_dfa(regex: str):
        postfix_regex = ShuntingYard.convert_to_postfix(regex)
        thompson = Thompson(postfix_regex)
        nfa = thompson.make_afn()
        converter = NfaToDfa(nfa)
        dfa = converter.get_dfa()
        dfa.print_automata("_dfa")
        minimizer = Minimizer(dfa)
        minimized_dfa = minimizer.make_minimized_dfa()
        minimized_dfa.print_automata("_minimized")
        return minimized_dfa
