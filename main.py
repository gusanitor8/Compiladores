from ShuntingYard.shunting_yard import ShuntingYard
from ShuntingYard.parse_tree_builder import ParseTree
from DirectConstruction import DirectConstruction
from Automata import Automata, DeterministicFiniteAutomata
from Simulator import DFASimulator, NFASimulator
from Minimizer import Minimizer
from Thompson import Thompson
from NfaToDfa import NfaToDfa

if __name__ == "__main__":

    def menu():
        print("Choose an option to simulate:")
        print("1. Direct Construction")
        print("2. Thompson (NFA)")
        print("3. NFA to DFA (DFA)")
        print("4. Minimized (DFA)")
        print("5. Exit")


    def shunting_yard():
        regex = ShuntingYard().getPostfixRegex()
        tree = ParseTree(regex[0])
        nodes = tree.get_nodes()
        tree = tree.get_tree()

        return regex[0], tree, nodes


    def direct_construction(tree, tree_nodes):
        direct_construction_ = DirectConstruction(tree, tree_nodes)
        dfa = direct_construction_.get_dfa()
        dfa.print_automata("_direct_construction")
        return dfa


    def thompson_nfa(pf_regex: str, to_print: bool = True):
        thompson = Thompson(pf_regex)
        nfa = thompson.make_afn()
        if to_print:
            nfa.print_automata("_nfa")
        return nfa


    def nfa_to_dfa(nfa: Automata, to_print: bool = True):
        converter = NfaToDfa(nfa)
        dfa = converter.get_dfa()
        if to_print:
            dfa.print_automata("_dfa")
        return dfa


    def minimized(dfa: DeterministicFiniteAutomata):
        minimizer = Minimizer(dfa)
        minimized_dfa = minimizer.make_minimized_dfa()
        minimized_dfa.print_automata("_minimized")
        return minimized_dfa


    def print_accepted(value: bool):
        if value:
            print("String accepted\n")
        else:
            print("String rejected\n")


    def run():
        regex, tree, nodes = shunting_yard()

        is_running = True
        while is_running:
            menu()
            option = input("Enter option: ")
            if option == "1":
                dfa = direct_construction(tree, nodes)
                simulator = DFASimulator(dfa)
                string = input("Enter string to simulate: ")
                value = simulator.simulate(string)  # print
                print_accepted(value)

            elif option == "2":
                nfa = thompson_nfa(regex)
                simulator = NFASimulator(nfa)
                string = input("Enter string to simulate: ")
                value = simulator.simulate(string)  # print
                print_accepted(value)

            elif option == "3":
                nfa = thompson_nfa(regex, False)
                dfa = nfa_to_dfa(nfa)
                simulator = DFASimulator(dfa)
                string = input("Enter string to simulate: ")
                value = simulator.simulate(string)  # print
                print_accepted(value)

            elif option == "4":
                nfa = thompson_nfa(regex, False)
                dfa = nfa_to_dfa(nfa, False)
                minimized_dfa = minimized(dfa)
                simulator = DFASimulator(minimized_dfa)
                string = input("Enter string to simulate: ")
                value = simulator.simulate(string)  # print
                print_accepted(value)

            elif option == "5":
                is_running = False


    run()
