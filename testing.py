from src.Automatas.Automata import DeterministicFiniteAutomata, Automata
from src.Automatas.DirectConstruction import DirectConstruction
from src.Automatas.Minimizer import Minimizer
from src.Automatas.NfaToDfa import NfaToDfa
from src.Automatas.Thompson import Thompson
from src.ShuntingYard.shunting_yard import ShuntingYard


def test_construction():
    sy = ShuntingYard()
    regex_arr = sy.get_postfix_regex()
    postfix_regex = regex_arr[0]
    thompson = Thompson(postfix_regex)
    nfa = thompson.make_afn()
    nfa.print_automata()
    converter = NfaToDfa(nfa)
    dfa = converter.get_dfa()
    # dfa.print_automata("_dfa")
    minimizer = Minimizer(dfa)
    minimized_dfa = minimizer.make_minimized_dfa()
    minimized_dfa.remove_dead_states()
    minimized_dfa.print_automata("_minimized")
    return minimized_dfa
