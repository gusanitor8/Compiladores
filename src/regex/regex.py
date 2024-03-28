from src.ShuntingYard.shunting_yard import ShuntingYard
from src.Automatas.NfaToDfa import NfaToDfa
from src.Automatas.Minimizer import Minimizer
from src.Automatas.Automata import Automata
from src.Automatas.Thompson import Thompson
from src.constants import REGEX_SYMBOLS


class Regex:
    def __init__(self, regex: str):
        self.regex = regex
        self.dfa: Automata = self._build_dfa(regex)

    def get_dfa(self):
        return self.dfa

    def shortest_search(self, string) -> tuple:
        flag = self.shortest_match(string)
        offset = 0

        while flag is None and string != "":
            string = string[1:]
            flag = self.shortest_match(string)
            offset += 1

        if flag is not None:
            return (flag[0] + offset, flag[1] + offset)

    def longest_search(self, string) -> tuple:
        """
        This method returns the range of the longest match for a given regex
        :param string: String to be matched
        :return: The range of the longest match or None if no match is found
        """

        flag = self.longest_match(string)
        offset = 0

        while flag is None and string != "":
            string = string[1:]
            flag = self.longest_match(string)
            offset += 1

        if flag is not None:
            return tuple((flag[0] + offset, flag[1] + offset))

    def _sanitize_regex(self, string: str):
        any = '(' + self.generate_char_set_with_separator('(', '|') + ')'
        regex = "['" + any + "'-'" + any + "']"

    @staticmethod
    def generate_char_set_with_separator(*ranges):
        """Generates a string containing all characters between specified start and end characters, separated by a separator.

        Args:
            separator: The separator to use between character ranges. Defaults to '|'.
            *ranges: An even number of characters representing start and end pairs for character ranges.

        Returns:
            A string containing all characters between the specified start and end characters, separated by the separator.

        Raises:
            ValueError: If an odd number of ranges is provided.
        """
        separator: str = '|'

        if len(ranges) % 2 != 0:
            raise ValueError("An even number of character ranges must be provided.")

        char_set = []
        for i in range(0, len(ranges), 2):
            start, end = ranges[i], ranges[i + 1]
            # Use a list comprehension to create the escaped characters explicitly
            escaped_chars = ["'" + chr(c) + "'" if chr(c) in REGEX_SYMBOLS else chr(c) for c in
                             range(ord(start), ord(end) + 1)]
            char_set.extend(escaped_chars)

        return separator.join(char_set)

    def longest_match(self, string: str):
        """
        This method returns the string indexes of the longest match for a given regex
        :param string: String to be matched
        :return: The range of the longest match or None if no match is found
        """

        idx = 0
        str_len = len(string)
        char = string[idx] if str_len > 0 else ""
        flag = True

        def next_char_idx():
            nonlocal idx
            if idx < str_len:
                idx += 1
                return idx
            return None

        acceptance_strings_idx = []
        current_state = self.dfa.get_initial()
        final_states = self.dfa.get_final()

        while idx is not None and flag:
            if current_state in final_states:
                acceptance_strings_idx.append(idx)

            if char not in current_state.transitions:
                flag = False
                continue

            current_state = current_state.transitions[char]
            idx = next_char_idx()
            char = string[idx] if (idx is not None and idx < str_len) else None

        if acceptance_strings_idx:
            max_difference_idx = max(acceptance_strings_idx)
            # TODO: change the second value to exclusive, since inclusive could lead to errors for empty strings
            return tuple((0, max_difference_idx))
        else:
            return None

    def substitute(self, regex: str, string: str):
        """
        This method substitutes the regex in the string with the string
        :param regex: The regex to be substituted
        :param string: The string to be substituted
        :return: The new string
        """
        raise NotImplementedError

    def shortest_match(self, string: str):
        """
        This function takes a string and returns the range of the first match of the regex in the string
        :param string:
        :return: a tuple (start, end) start is inclusive end is exclusive, None if no match is found
        """
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

            if char in current_state.transitions:
                current_state = current_state.transitions[char]
            else:
                return None

            if char is None:
                return None

        return (0, index)

    @staticmethod
    def _build_dfa(regex: str):
        postfix_regex = ShuntingYard.convert_to_postfix(regex)
        thompson = Thompson(postfix_regex)
        nfa = thompson.make_afn()
        converter = NfaToDfa(nfa)
        dfa = converter.get_dfa()
        # TODO: activar minimizacion
        minimizer = Minimizer(dfa)
        minimized_dfa = minimizer.make_minimized_dfa()
        dfa.remove_dead_states()
        # minimized_dfa.print_automata("_minimized")
        return minimized_dfa
