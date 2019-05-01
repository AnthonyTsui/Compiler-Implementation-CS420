import re

operands = {
    '(':'L_PAREN',
    ')':'R_PAREN',
    '+':'ADD',
    '-':'SUB',
    ';':'SEMI',
    '*':'MULT',
    'print':'PRINT',
}

test = 'rtwee'
class genToken():
    def __init__(self):
        self.tokens = []

    def add_tokens(self, string):
        for preToken in re.split('(\W)', string):
            if not preToken == '':
                self.tokens.append(self.check_token(preToken))


    def check_token(self, rawInput):
        if(rawInput in operands):
            return ['TOKEN',rawInput,operands[rawInput]]
        else:
            return['TOKEN',rawInput,'VAR']

    def get_lexer(self):
        return self.tokens