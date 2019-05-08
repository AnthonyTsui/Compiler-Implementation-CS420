from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')
        # Parenthesis
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')
        # Number
        self.lexer.add('NUM', r'\d+')
        self.lexer.add('TEST', r'\*')
        # Ignore spaces
        self.lexer.ignore('\s+')
        

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()