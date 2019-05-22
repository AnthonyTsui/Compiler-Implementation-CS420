import sys
import re
import os

(INTEGER, REAL, INT_NUM, REAL_NUM, PLUS, MINUS, EOF, MULT, INT_DIV, 
LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, DOT, SEMI, 
COMMA, COLON, FLOAT_DIV, VAR, PROGRAM, DOT, EQUAL, WRITELN, APOS, STRING_LITERAL) =('INTEGER', 'REAL', 'INT_NUM', 'REAL_NUM','PLUS', 'MINUS', 
'EOF', 'MULT', 'INT_DIV', '(', ')', 'ID', 'ASSIGN', 'BEGIN', 'END', 'DOT','SEMI', 'COMMA', 
'COLON', 'FLOAT_DIV', 'VAR', 'PROGRAM', 'DOT', 'EQUAL', 'WRITELN', "'", 'STRING_LITERAL')


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
            'IF': Token('IF','IF'),
            'ELSE': Token('ELSE', 'ELSE'),
            'PROGRAM': Token('PROGRAM', 'PROGRAM'),
            'VAR': Token('VAR', 'VAR'),
            'DIV': Token('INT_DIV', 'DIV'),
            'INTEGER':Token('INTEGER', 'INTEGER'),
            'REAL': Token('REAL','REAL'),
            'writeln': Token('WRITELN','WRITELN')}


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

    def skipSpace(self):        #Handling white space
        while self.currChar is not None and self.currChar.isspace():
            self.nextToken()

    def skipComment(self):      #For skipping comments
        while self.currChar != '}':
            self.nextToken()
        self.nextToken()
            
    def stringLiteral(self):
        returnString = ''
        while self.currChar != "'":
            returnString += self.currChar
            self.nextToken()
        self.nextToken()
        return Token(STRING_LITERAL, returnString)
    
    def allNumbers(self):
        result = ''
        while self.currChar is not None and self.currChar.isdigit():
            result += self.currChar
            self.nextToken()
        if self.currChar == '.':
            result += self.currChar
            self.nextToken()
            while(self.currChar is not None and  self.currChar.isdigit()):
                result += self.currChar
                self.nextToken()
            token = Token('REAL_NUM', float(result))
        else:
            token = Token('INT_NUM', int(result))
        return token

    def getNextToken(self):

        while self.currChar is not None:

            if self.currChar.isspace():
                self.skipSpace()
                continue

            if self.currChar == '{':
                self.nextToken()
                self.skipComment()
                continue

            if self.currChar.isalpha():
                return self._id()

            if self.currChar.isdigit():
                return self.allNumbers()

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
                return Token(FLOAT_DIV, '/')
                
            if self.currChar == '(':
                self.nextToken()
                return Token(LPAREN, '(')
            
            if self.currChar == ')':
                self.nextToken()
                return Token(RPAREN, ')')
           
            if self.currChar == ':' and self.checkNext() == '=':
                self.nextToken()
                self.nextToken()
                return Token(ASSIGN, ':=')

            if self.currChar == ';':
                self.nextToken()
                return Token(SEMI, ';')
            
            if self.currChar == '.':
                self.nextToken()
                return Token(DOT, '.')

            if self.currChar == ':':
                self.nextToken()
                return Token(COLON, ':')

            if self.currChar == ',':
                self.nextToken()
                return Token(COMMA, ',')
            
            if self.currChar == "'":
                self.nextToken()
                return self.stringLiteral()

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

class CompoundStateNode(ASTNode):
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

class Program(ASTNode):
    def __init__(self, progName, stateBlock):
        self.name = progName
        self.block = stateBlock
        
class stateBlock(ASTNode):
    def __init__(self, variables, statements):
        self.variables = variables
        self.statements = statements

class declareVarType(ASTNode):
    def __init__(self, varNode, typeNode):
        self.varNode = varNode
        self.typeNode = typeNode

class varType(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        #self.type = token.type      #EXCESS?

class writeStatement(ASTNode):
    def __init__(self, node):      #here token would be an expression?
        #self.token = token
        self.node = node
        self.value = node.value   #What to print I guess
        #Need to return a token that is both: "string" + Expression

class stringLiteral(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class visitNode(object):
    def visit(self, node):      #Easy way to dynamically call a visit function for each node
        method_name = 'visit' + type(node).__name__
        #print(method_name)
        visited = getattr(self, method_name, self.generic_visit)
        return visited(node)

    def generic_visit(self, node):      #for exception handling when finding invalid tokens
        #print('we are at error where with: ' + str(node))
        raise Exception('No visiting {} method found'.format(type(node).__name__))


class Parser(object):
    def __init__(self, Lexer):
        self.lexer = Lexer
        self.currToken = self.lexer.getNextToken()
    
    def error(self):
        raise Exception('Error parsing input')

    def removeToken(self, token_type):
        print(self.currToken)
        if self.currToken.type == token_type:
            self.currToken = self.lexer.getNextToken()
        else:
            print("we got " + token_type + "when we are holding: " + self.currToken.type)
            self.error()

    def getFactor(self):
        token = self.currToken

        if token.type == INTEGER:
            #print(token)
            self.removeToken(INTEGER)
            return Number(token)
        elif token.type == LPAREN:
            #print(token)
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
        elif token.type == INT_NUM:
            self.removeToken(INT_NUM)
            return Number(token)
        elif token.type == REAL_NUM:
            self.removeToken(REAL_NUM)
            return Number(token)
        else:
            node = self.isVariable()
            return node

    def getTerm(self):
        node = self.getFactor()
        termOps = (MULT, INT_DIV, FLOAT_DIV)

        while self.currToken.type in termOps:
            token = self.currToken
            print(token)
            if token.type == MULT:
                self.removeToken(MULT)
            elif token.type == INT_DIV:
                self.removeToken(INT_DIV)
            elif token.type == FLOAT_DIV:
                self.removeToken(FLOAT_DIV)
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
        root = CompoundStateNode()

        for node in nodeList:
            root.children.append(node)
        return root


    def pascalProg(self):
        self.removeToken(PROGRAM)
        variableNode = self.isVariable()
        progName = variableNode.value
        self.removeToken(SEMI)
        blockNode = self.stateBlock()
        progNode = Program(progName, blockNode)
        self.removeToken(DOT)
        return progNode

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
        elif self.currToken.type == WRITELN:
            node = self.writeState()
        else: 
            node = self.isEmpty()
        return node
       
    def writeState(self):           #WriteStatement ----Unfinished
        self.removeToken(WRITELN)
        self.removeToken(LPAREN)
        if self.currToken.type == ID:
            varNode = Variable(self.currToken)
            node = writeStatement(varNode)
            self.removeToken(ID)
        elif self.currToken.type == STRING_LITERAL:
            stringNode = Variable(self.currToken)
            node = writeStatement(stringNode)
            self.removeToken(STRING_LITERAL)
        self.removeToken(RPAREN)

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

    def stateBlock(self):
        varBlocksNode = self.declares()
        compoundStatementNode = self.compoundState()    #compoundState=after assignments
        node = stateBlock(varBlocksNode, compoundStatementNode)
        return node

    def declares(self):
        declaredVars = []
        if self.currToken.type == VAR:
            self.removeToken(VAR)
            while self.currToken.type == ID:
                varDeclare = self.variableDeclare()
                declaredVars.extend(varDeclare)
                self.removeToken(SEMI)
        return declaredVars

    def variableDeclare(self):
        #print('DId we make it in')
        variableNodes = [varType(self.currToken)]
        self.removeToken(ID)

        while self.currToken.type == COMMA:
            #print('Removing token comma with curr token: ' + self.currToken.type)
            self.removeToken(COMMA)
            variableNodes.append(varType(self.currToken))
            self.removeToken(ID)
        
        self.removeToken(COLON)
        type_node = self.typeSpec()
        variableDeclarations = [
            declareVarType(variableNode, type_node)
            for variableNode in variableNodes
        ]
        return variableDeclarations

    def typeSpec(self):
        token = self.currToken
        #print('We are in typeSpec with current token type: ' + token.type + ' ' + token.value)
        if self.currToken.type == INTEGER:
            self.removeToken(INTEGER)
        elif self.currToken.type == REAL:
            self.removeToken(REAL)
        node = varType(token)
        return node
    
    
    def parse(self):
        node = self.pascalProg()
        if self.currToken.type != EOF:
            self.error()
        return node


class Compiler(visitNode):
          

    def __init__(self, parse):
        self.parser = parse
        self.SYMBOL_TABLE = {}       #SYMBOL table for storing variables we encounter on the program
    
    def visitBinOp(self, node):
        if node.oper.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.oper.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.oper.type == MULT:
            #leftVal = self.visit(node.left)
            #rightVal = self.visit(node.right)
            return self.visit(node.left) * self.visit(node.right)
        elif node.oper.type == INT_DIV:
            #print('We are at INT_DIV')
            #print(self.visit(node.left))
            #print(self.visit(node.right))
            return self.visit(node.left) // self.visit(node.right)
        elif node.oper.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
        elif node.oper.tpye == EQUAL:
            return (self.visit(node.left) == self.visit(node.right))
    
    def visitNumber(self, node):
        #print('We are at visit number with:')
        #print(node.value)
        return node.value
    
    def visitUnaryOp(self, node):
        if node.oper.type == PLUS:
            return +self.visit(node.express)
        if node.oper.type == MINUS:
            return -self.visit(node.express)
    
    def visitCompoundStateNode(self, node):
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
    
    def visitProgram(self, node):
        self.visit(node.block)
    
    def visitstateBlock(self, node):
        for variable in node.variables:
            self.visit(variable)
        self.visit(node.statements)
    
    def visitdeclareVarType(self, node):
        pass
    
    def visitvarType(self, node):
        pass
    
    def visitwriteStatement(self, node):
        if node.node.token.type == ID:  #this is disgusting, need to redo
            toPrint = self.visitVariable(node.node)
        elif node.node.token.type == STRING_LITERAL:
            toPrint = node.node.value
        print(toPrint)
        #print (node.value)
        pass

    def compile(self):
        ASTree = self.parser.parse()
        if ASTree is None:
            return ''
        return self.visit(ASTree)

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

    for a, b in sorted(compiler.SYMBOL_TABLE.items()):
        print('{} = {}'.format(a, b))



if __name__ == '__main__':
    main()