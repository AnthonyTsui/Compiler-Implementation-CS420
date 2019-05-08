from constantSymbols import symbolsDict
from constantSymbols import reservedDict
from constantSymbols import operatorsDict
from constantSymbols import reservedSymbols
from tokenClass import token
import re


class tokenizer:
    def __init__(self):
        self.currToken = None
        self.prevToken = None  
        self.nextToken = None  #Honestly not sure if I even need these right now 

    def parse_and_tokenize(self, toTokenize):
        token_val = None
        token_type = None
        token_action = None

        token_val = toTokenize
        token_type = self.find_type(toTokenize)
        token_action = self.find_action(toTokenize)

        newToken = token(token_val = token_val, token_type = token_type, token_action = token_action)
        return newToken

    
    def create(self, toTokenize):
        newToken = self.parse_and_tokenize(toTokenize)
        return newToken
    
    def find_type(self, tokenVal):
        if tokenVal in reservedSymbols:
            if tokenVal in operatorsDict:
                return operatorsDict[tokenVal][0]
            else:
                return symbolsDict[tokenVal][0]
        if tokenVal in reservedDict:
            return reservedDict[tokenVal][1]
        # Not reserved symbol or keyword so it must be a literal
        if self.isInt(tokenVal):
            return "TOKEN_LITERAL_INT"
        if self.isFloat(tokenVal):
            return "TOKEN_LITERAL_BOOL"
        #Reached this point so it must be a var identity and not a number
        return "TOKEN_IDENTITY"

    def find_action(self, tokenVal):
        if tokenVal in symbolsDict:
            return symbolsDict[tokenVal][1]
        if tokenVal in operatorsDict:
            return operatorsDict[tokenVal][1]
        if tokenVal in reservedDict:
            return reservedDict[tokenVal][1]
        if self.isFloat(tokenVal) or self.isInt(tokenVal):
            return "number" #number literal but thats too long
        return "identity"
        
        
    def isInt(self,tokenVal):
        try: 
            test = float(tokenVal)
            testFloat = int(test)
        except ValueError:
            return False
        else:
            return test == testFloat     #Checks equivalence of type

    def isFloat(self, tokenVal):
        try:
            test = float(tokenVal)
        except ValueError:
            return False
        else:
            return True

    
        
        
    

