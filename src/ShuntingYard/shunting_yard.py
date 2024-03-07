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
        special_chars = [ESCAPE]
        res = ""

        for i in range(len(regex)):
            c1 = regex[i]

            if i + 1 < len(regex):
                c2 = regex[i + 1]

                res += c1

                if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in special_chars and c1 not in binaryOperators:
                    res += '.'

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
        stack = []
        postfix = ""
        isScapedChar = False

        for char in formatedRegex:
            if isScapedChar:
                postfix += char
                isScapedChar = False
                continue

            if char == ESCAPE:
                postfix += char
                isScapedChar = True
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

        while len(stack) > 0:
            postfix += stack.pop()

        return postfix
