class ShuntingYard:
    # TODO: Add constructor which has filename as parameter

    # File reader
    @staticmethod
    def _readfile(filename, encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            data = f.read().splitlines()
        return data

    # Regex Formater
    @staticmethod
    def _format_reg_ex(regex):
        allOperators = ['|', '?', '+', '*', '^']
        binaryOperators = ['^', '|']
        res = ""

        for i in range(len(regex)):
            c1 = regex[i]

            if i + 1 < len(regex):
                c2 = regex[i + 1]

                res += c1

                if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binaryOperators:
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
    def _infix_to_postfix(self, formatedRegex):
        operators = ['|', '?', '+', '*', '^', '.', '(', ')']
        stack = []
        postfix = ""
        isScapedChar = False

        for char in formatedRegex:
            if isScapedChar:
                postfix += char
                isScapedChar = False
                continue

            if char == '\\':
                stack.append(char)
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

                elif self._get_precedence(peekedChar) >= self._get_precedence(char) and (peekedChar != '('):
                    postfix += stack.pop()
                    stack.append(char)

                else:
                    stack.append(char)
            else:
                postfix += char

        while len(stack) > 0:
            postfix += stack.pop()

        return postfix

    def getPostfixRegex(self, encoding='utf-8'):
        expressions = self._readfile('./ShuntingYard/regex.txt', encoding)

        postfixArr = []
        for regex in expressions:
            formatedRegex = self._format_reg_ex(regex)
            postfix = self._infix_to_postfix(formatedRegex)
            postfixArr.append(postfix)

        return postfixArr
