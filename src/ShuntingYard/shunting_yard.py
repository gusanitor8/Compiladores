from src.constants import ESCAPE


class ShuntingYard:
    def __init__(self, filename='./src/ShuntingYard/regex.txt'):
        self.filename = filename

    def get_postfix_regex(self):
        expressions = self._readfile(self.filename)

        postfix_arr = []
        for regex in expressions:
            formated_regex = self._format_reg_ex(regex)
            postfix = self._infix_to_postfix(formated_regex)
            postfix_arr.append(postfix)

        return postfix_arr

    @staticmethod
    def convert_to_postfix(regex: str):
        formated_regex = ShuntingYard._format_reg_ex(regex)
        return ShuntingYard._infix_to_postfix(formated_regex)

    @staticmethod
    def _readfile(filename):
        with open(filename, 'r') as f:
            data = f.read().splitlines()
        return data

    @staticmethod
    def _format_reg_ex(regex):
        allOperators = ['|', '?', '+', '*', '^']
        binaryOperators = ['^', '|']
        special_chars = []

        len_regex = len(regex)
        res = ""
        i = 0
        is_scaped = False

        while i < len_regex - 1:
            c1 = regex[i]

            # We check for a scaped character between single quotes
            if c1 == "'":
                if i + 2 < len(regex):
                    if regex[i + 2] == "'":
                        is_scaped = True
                        res += c1
                        res += regex[i + 1]
                        res += regex[i + 2]


                        if i + 3 < len(regex):
                            c1 = regex[i + 3]

                            if c1 != ')' and c1 not in allOperators:
                                res += '.'

                        i += 3
                        continue
            is_scaped = False

            # Once we know there is not a scaped character we can continue with the normal process
            if i + 1 < len(regex):
                c2 = regex[i + 1]

                res += c1

                if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in special_chars and c1 not in binaryOperators:
                    res += '.'

            i += 1

        if regex[-1] != "'":
            res += regex[-1]

        return res

    # Gets Precedence of an operator
    @staticmethod
    def _get_precedence(c):
        precedences = {
            '(': 4,
            ')': 4,
            '|': 0,
            '.': 2,
            '?': 3,
            '*': 3,
            '+': 3,
            '^': 1,
            '$': 1,
        }
        return precedences.get(c, 0)

    # Converts infix to postfix
    @staticmethod
    def _infix_to_postfix(formatedRegex):
        operators = ['|', '?', '+', '*', '^', '.', '(', ')']
        regex_len = len(formatedRegex)
        stack = []
        postfix = ""
        is_scaped = False

        i = 0
        while i < len(formatedRegex):
            char = formatedRegex[i]

            if char == "'":
                if i + 2 < regex_len:
                    if formatedRegex[i + 2] == "'":
                        postfix += char
                        postfix += formatedRegex[i + 1]
                        postfix += formatedRegex[i + 2]
                        i += 3
                        continue

            if char == '(':
                stack.append(char)

            elif char in operators:
                peekedChar = stack[-1] if stack else None

                if char == ')':
                    while peekedChar != '(':
                        postfix += stack.pop()
                        peekedChar = stack[-1] if stack else None
                    stack.pop()
                    i += 1
                    continue

                if peekedChar == None:
                    stack.append(char)

                elif ShuntingYard._get_precedence(peekedChar) >= ShuntingYard._get_precedence(char) and (peekedChar != '('):
                    postfix += stack.pop()
                    stack.append(char)

                else:
                    stack.append(char)
            else:
                postfix += char

            i += 1

        while len(stack) > 0:
            postfix += stack.pop()

        return postfix
