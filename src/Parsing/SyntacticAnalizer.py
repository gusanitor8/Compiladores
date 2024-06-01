from src.Parsing.Parser import Parser
class SyntacticAnalizer:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.stack = []
        self.input = []
        self.symbols = []