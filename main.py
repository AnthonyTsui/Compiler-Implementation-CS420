from lexer import Lexer
from lexer2 import genToken
import re
from tokenizer import tokenizer



text_input = """
print(4 + 4 - 2) * ;
"""

genLexer = Lexer().get_lexer()
tokens = genLexer.lex(text_input)
#for token in tokens:
#    print(token)

print('Test cases for re.split:')

row = 'writeln(4+2-1);thenwe checkif this thing actuall works int main() {4+4+2*4^3}; :='
#print(re.split('(\W)', row))


testTokenizer = genToken()
testTokenizer.add_tokens(row)

for token in testTokenizer.tokens:
    print(token)


print('Below is the test for our token function')


tokenizerClass = tokenizer()
testTokens = []

#row = 'print(4+2-1);thenwe checkif this thing actuall works int main() {4+4+2*4^3}; :='


for preToken in re.split('(\W)', row):
            if not preToken == '' and not preToken == ' ':
                    testTokens.append(tokenizerClass.parse_and_tokenize(preToken))

for token in testTokens:
        print(token)