from lexer import Lexer
from lexer2 import genToken
import re

text_input = """
print(4 + 4 - 2) * ;
"""

genLexer = Lexer().get_lexer()
tokens = genLexer.lex(text_input)



for token in tokens:
    print(token)

print('Test cases for re.split:')

row = 'print(4+2-1);'
print(re.split('(\W)', row))


testTokenizer = genToken()
testTokenizer.add_tokens(row.replace(' ', ''))

for token in testTokenizer.tokens:
    print(token)

'''
testList = []
testList.append([1,0])
testList.append(['Yeah','It works'])
print(testList)
print(testList[0][1])


testString = 'Yeah this is a b i g test +-4 () '
testString.split()
print(testString.split())

testString2 = 'print(4 + 4 - 2)'
for char in testString2:
    if(char.isalpha()):
        print(char+' is alpha')


testTokenizer = genToken()
testTokenizer.add_tokens(testString2)

for token in testTokenizer.tokens:
    print(token)
    '''


