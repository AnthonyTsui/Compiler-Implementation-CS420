import sys
import re
import os

INTEGER, PLUS, MINUS, EOF, MULT, DIV, LPAREN, RPAREN = 'INTEGER', 'PLUS', 'MINUS', 'EOF', 'MULT', 'DIV', '(', ')'


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
                
            if self.currChar == '(':
                self.nextToken()
                return Token(LPAREN, '*')
            
            if self.currChar == ')':
                self.nextToken()
                return Token(RPAREN, '/')

            self.error()

        return Token(EOF, None)

class ASTNode(object):
    pass

class BinOp(ASTNode):
    def __init__(self, left, right, oper):
        self.left = left
        self.right = right
        self.oper = self.token = oper

class Number(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class visitNode(object):
    def visit(self, node):
        method_name = 'visit' + type(node).__name__
        visited = getattr(self, method_name, self.generic_visit)
        return visited(node)

    def generic_visit(self, node):
        raise Exception('No visiting {} method found'.format(type(node).__name__))


class Parser(object):
    def __init__(self, Lexer):
        self.lexer = Lexer
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

        if token.type == INTEGER:
            print(token)
            self.removeToken(INTEGER)
            return Number(token)
        elif token.type == LPAREN:
            print(token)
            self.removeToken(LPAREN)
            node = self.express()
            self.removeToken(RPAREN)
            return node
        

    def getTerm(self):
        node = self.getFactor()
        termOps = (MULT, DIV)

        while self.currToken.type in termOps:
            token = self.currToken
            print(token)
            if token.type == MULT:
                self.removeToken(MULT)
            elif token.type == DIV:
                self.removeToken(DIV)
            node = BinOp(left = node, oper = token, right = self.getFactor())
        return node

    def express(self):   #for addition and subtraction, since we perform getTerm() on multiplicatin and division first

        node = self.getTerm()
        expOps = (PLUS, MINUS)

        while self.currToken.type in expOps:
            token = self.currToken
            print(token)
            if token.type == PLUS:
                self.removeToken(PLUS)
            elif token.type == MINUS:
                self.removeToken(MINUS)
            node = BinOp(left = node, oper = token, right = self.getTerm())
        return node
    
    def parse(self):
        return self.express()


class Compiler(visitNode):
    def __init__(self, parse):
        self.parser = parse
    
    def visitBinOp(self, node):
        if node.oper.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.oper.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.oper.type == MULT:
            return self.visit(node.left) * self.visit(node.right)
        elif node.oper.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visitNumber(self, node):
        return node.value
    
    def compile(self):
        ASTree = self.parser.parse()
        return self.visit(ASTree) #inherited from visitNode class

def main():
    path = os.getcwd()
    path = path + '\\newApproach\\testfile.txt' #passing in the testfile
    #print(path)
    with open(path, 'r') as file:
        testInput = file.read()
        print(testInput)

    #testline = '14 + 2 * 3 - 6 / 2'
    #testcompiler = Parser(testInput)
    #result = testcompiler.express()
    #print(result)


    lexer = Lexer(testInput)
    parser = Parser(lexer)
    compiler = Compiler(parser)
    result = compiler.compile()
    print(result)

if __name__ == '__main__':
    main()