import sys
import re
import os

(INTEGER, PLUS, MINUS, EOF, MULT, DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, PERIOD, SEMI) = ('INTEGER', 
'PLUS', 'MINUS', 'EOF', 'MULT', 'DIV', '(', ')', 'ID', 'ASSIGN', 'BEGIN', 'END', 'PERIOD',
'SEMI')


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

KEYWORDS = {'BEGIN': Token('BEGIN','BEGIN'),
            'END': Token('END', 'END'),
            'IF': Token('IF','IF"'),

            }


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

    def checkNext(self):
        checkPos = self.pos + 1
        if checkPos > len(self.input) - 1:
            return None
        else:
            return self.input[checkPos]

    def _id(self):
        result = ''
        while self.currChar is not None and self.currChar.isalnum():
            result += self.currChar
            self.nextToken()
        token = KEYWORDS.get(result, Token(ID, result))
        return token

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

            if self.currChar.isalpha():
                return self._id()
            
            if self.currChar == ':' and self.checkNext() == '=':
                self.nextToken()
                self.nextToken()
                return Token(ASSIGN, ':=')

            if self.currChar == ';':
                self.nextToken()
                return Token(SEMI, ';')
            
            if self.currChar == '.':
                self.nextToken()
                return Token(PERIOD, '.')

            self.error()

        return Token(EOF, None)


#List of nodes ##############################################################
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

class UnaryOp(ASTNode):
    def __init__(self, oper, express):
        self.token = self.oper = oper
        self.express = express

class CompoundState(ASTNode):
    def __init__(self):
        self.children = []

class AssignOp(ASTNode):
    def __init__(self, left, right, oper):
        self.left = left
        self.right = right
        self.oper = self.token = oper

class Variable(ASTNode):        #identifiers
    def __init__(self, token):
        self.token = token
        self.value = token.value

class EmptyStatement(ASTNode): #becase theres nothing between the Begin and End 
    pass

class visitNode(object):
    def visit(self, node):      #Easy way to dynamically call a visit function for each node
        method_name = 'visit' + type(node).__name__
        visited = getattr(self, method_name, self.generic_visit)
        return visited(node)

    def generic_visit(self, node):      #for exception handling when finding invalid tokens
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
        elif token.type == PLUS:
            #print (token)
            self.removeToken(PLUS)
            node = UnaryOp(token, self.getFactor())
            return node
        elif token.type == MINUS:
            #print (token)
            self.removeToken(MINUS)
            node = UnaryOp(token, self.getFactor())
            return node
        else:
            node = self.isVariable()
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
    
    def compoundState(self):
        self.removeToken(BEGIN)
        nodeList = self.listStates()
        self.removeToken(END)
        root = CompoundState()

        for node in nodeList:
            root.children.append(node)
        return root


    def pascalProg(self):
        node = self.compoundState()
        self.removeToken(PERIOD)
        return node

    def listStates(self):
        node = self.statements()
        results = [node]

        while self.currToken.type == SEMI:
            self.removeToken(SEMI)
            results.append(self.statements())

        if self.currToken.type == ID:
            self.error()
        
        return results
    
    def statements(self):
        if self.currToken.type == BEGIN:
            node = self.compoundState()
        elif self.currToken.type == ID:
            node = self.assignState()
        else: 
            node = self.isEmpty()
        return node
        

    def assignState(self):
        left = self.isVariable()
        token = self.currToken
        self.removeToken(ASSIGN)
        right = self.express()
        node = AssignOp(left, right, token)
        return node

    def isVariable(self):
        node = Variable(self.currToken)
        self.removeToken(ID)
        return node

    def isEmpty(self):
        return EmptyStatement()


    
    
    def parse(self):
        node = self.pascalProg()
        if self.currToken.type != EOF:
            self.error()
        return node


class Compiler(visitNode):
    SYMBOL_TABLE = {}

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
    
    def visitUnaryOp(self, node):
        if node.oper.type == PLUS:
            return +self.visit(node.express)
        if node.oper.type == MINUS:
            return -self.visit(node.express)
    
    def visitCompoundState(self, node):
        for nodes in node.children:
            self.visit(nodes)

    def visitAssignOp(self, node):
        varName = node.left.value
        self.SYMBOL_TABLE[varName] = self.visit(node.right)

    def visitVariable(self, node):
        varName = node.value
        val = self.SYMBOL_TABLE.get(varName)
        if val is None:
            raise NameError(repr(varName))
        else:
            return val

    def visitEmptyStatement(self, node):
        pass
    
    
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
    print(compiler.SYMBOL_TABLE)
    print(result)

if __name__ == '__main__':
    main()