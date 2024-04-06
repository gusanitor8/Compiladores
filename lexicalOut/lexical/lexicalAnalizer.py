import pickle
from src.LexicalAnalizerGenerator.LexicalAnalizerGenerator import LexicalAutomata
from src.Automata.automata import Automata

def run():
    lexical_automata: LexicalAutomata = unpickle()
    automata: Automata = lexical_automata.automata
    actions = lexical_automata.actions


def find_token(automata: Automata, word: str):
    """
    This method finds the token of a word
    :param automata: Automata
    :param actions: dict
    :param word: str
    :return: str
    """
    index = 0
    longest_match_states = set()
    current = automata.get_initial()
    current = Automata.e_closure(current)

    for char in word:
        current = Automata.e_closure_set(current)
        current = Automata.move(current, char)

        # We check if the current state is empty
        if not current:
            print("Invalid token: ", word)
            return None

        # We check if the current state is a final state
        if any(state in automata.get_final() for state in current):
            longest_match_states = current

        index += 1

    if not longest_match_states:
        print("Invalid token: ", word)
        return None

    result = (longest_match_states, index)



def unpickle():
    with open("./lexicalAnalizer.pkl", "rb") as file:
        automata = pickle.load(file)
    return automata


if __name__ == "__main__":
    run()
