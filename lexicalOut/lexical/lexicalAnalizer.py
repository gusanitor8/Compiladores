
import pickle
from src.LexicalAnalizerGenerator.LexicalAnalizerGenerator import LexicalAutomata
from src.Automatas.Automata import Automata


tokens = set()
productions = []

def token_found(token_str: str):
    token_str = token_str.strip()
    token_str = token_str[7:]

    tokens.add(token_str)

def production_found(token_str: str):
    item = token_str.split(":")
    rhs = item[1].strip()
    lhs = item[0].strip()

    rhs = rhs.split("|")

    for i in range(len(rhs)):
        if rhs[i][-1] == ";":
            rhs[i] = rhs[i][:-1]

        rhs[i] = rhs[i].strip()
        rhs[i] = rhs[i].split(" ")

        for j in range(len(rhs[i])):
            rhs[i][j] = rhs[i][j].strip()

    dic = {str(lhs): rhs}
    productions.append(dic)



def get_file_name():
    file_name = str(input("Enter the file name: "))
    return file_name


def get_file_content(file_name: str):
    with open(file_name, "r") as file:
        content = file.read()
    return content


def search_tokens(automata: Automata, final_node_precedence: dict, actions: dict, string: str):
    """
    This method searches for tokens in a file
    :param automata: Automata
    :param actions: dict
    :return: None
    """

    while string:
        token = find_token(automata, string)

        if token is None:
            string = string[1:]
        else:
            token_states = token[0]
            token_length = token[1]
            token_string = string[:token_length]

            token_state = min(token_states, key=lambda x: final_node_precedence[x])
            action = actions[token_state]
            print("t: " + token_string, end=" ")
            eval(action)
            string = string[token_length:]


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
            break

        # We check if the current state is a final state
        if any(state in automata.get_final() for state in current):
            longest_match_states = current.intersection(automata.get_final())

        index += 1

    if not longest_match_states:
        print("Invalid token: ", word[0])
        return None

    result = (longest_match_states, index)
    return result


def unpickle():
    with open("./lexicalAnalizer.pkl", "rb") as file:
        automata = pickle.load(file)
    return automata            

def run(file_path: str):
    lexical_automata: LexicalAutomata = unpickle()
    automata: Automata = lexical_automata.automata
    actions = lexical_automata.actions
    final_node_precedence = lexical_automata.final_node_precedence

    content = get_file_content(file_path)

    search_tokens(automata, final_node_precedence, actions, content)
    
    print("done")
    

if __name__ == "__main__":
    run("text.txt")
    print(tokens)
    print(productions)