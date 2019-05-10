INTEGER, PLUS, MINUS, EOF, MULT, DIV = 'INTEGER', 'PLUS', 'MINUS', 'EOF', 'MULT', 'DIV'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.currChar = self.input[self.pos]

    def error(self):
        raise Exception('Bad character in lexer')

    def nextToken(self):
        self.pos += 1
        if self.pos > len(self.input) - 1:
            self.currChar = None 
        else:
            self.currChar = self.input[self.pos]

    def skipSpace(self):
        while self.currChar is not None and self.currChar.isspace():
            self.nextToken()
            
    def integer(self):
        result = ''
        while self.currChar is not None and self.currChar.isdigit():
            result += self.currChar
            self.nextToken()
        return int(result)

    def getNextToken(self):

        while self.currChar is not None:

            if self.currChar.isspace():
                self.skipSpace()
                continue

            if self.currChar.isdigit():
                return Token(INTEGER, self.integer())

            if self.currChar == '+':
                self.nextToken()
                return Token(PLUS, '+')

            if self.currChar == '-':
                self.nextToken()
                return Token(MINUS, '-')

            if self.currChar == '*':
                self.nextToken()
                return Token(MULT, '*')
            
            if self.currChar == '/':
                self.nextToken()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

class Compiler(object):
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.currToken = self.lexer.getNextToken()
    
    def error(self):
        raise Exception('Error parsing input')

    def removeToken(self, token_type):
        if self.currToken.type == token_type:
            self.currToken = self.lexer.getNextToken()
        else:
            self.error()


    def getFactor(self):
        token = self.currToken
        self.removeToken(INTEGER)
        return token.value

    def getTerm(self):
        result = self.getFactor()
        termOps = (MULT, DIV)

        while self.currToken.type in termOps:
            token = self.currToken
            if token.type == MULT:
                self.removeToken(MULT)
                result = result * self.getFactor()
            elif token.type == DIV:
                self.removeToken(DIV)
                result = result / self.getFactor()
        return result

    def express(self):   #for addition and subtraction, since we perform getTerm() on multiplicatin and division first

        result = self.getTerm()
        expOps = (PLUS, MINUS)

        while self.currToken.type in expOps:
            token = self.currToken
            if token.type == PLUS:
                self.removeToken(PLUS)
                result = result + self.getTerm()
            elif token.type == MINUS:
                self.removeToken(MINUS)
                result = result - self.getTerm()
        return result


def main():
    testline = '1+2*10/2+5'
    testcompiler = Compiler(testline)
    result = testcompiler.express()
    print(result)



if __name__ == '__main__':
    main()