# Constants that include operands, reserved words, and function calls
# 

reservedSymbols = [
 ':=', '+', '-', '*', '/', '%', '=', '<>', '<' '>', '<=', '>=',
 '[', ']', '(', ')', '{', '}',';', ':'
]


operatorsDict = {
    ':=': ('TOKEN_ASSIGN', 'assign'),
    '+': ('TOKEN_ADDITION', 'add'),
    '-': ('TOKEN_SUBTRACTION', 'subtract'),
    '*': ('TOKEN_MULTIPLICATION', 'multiply'),
    '/': ('TOKEN_DIVISION', 'division'),
    '%': ('TOKEN_MOD', 'mod'),
    '=': ('TOKEN_EQUAL', 'equal'),
    '<>': ('TOKEN_INEQUAL', 'inequal'),
    '<': ('TOKEN_LESSTHAN', 'lessthan'),
    '>': ('TOKEN_GREATERTHAN', 'greaterthan'),
    '<=': ('TOKEN_LTOE', 'ltoequal'),
    '>=': ('TOKEN_GTOE', 'gtoequal')
}


symbolsDict = {
    '[':  ('TOKEN_LEFTBRACKET', 'leftbracket'),
    ']':  ('TOKEN_RIGHTBRACKET', 'rightbracket'),
    '(':  ('TOKEN_LEFTPAREN', 'leftparen'),
    ')':  ('TOKEN_RIGHTPAREN', 'rightparen'),
    '{':  ('TOKEN_LEFTCURLY', 'leftcurly'),
    '}':  ('TOKEN_RIGHTCURLY', 'rightcurly'),
    ';':  ('TOKEN_SEMICOLON', 'semicolon'),
    ':':  ('TOKEN_COLON', 'colon')
}


reservedDict = {
    'if': ('TOKEN_IF', 'if'),
    'while': ('TOKEN_WHILE', 'while'),
    'var': ('TOKEN_VAR', 'var'),
    'writeln': ('TOKEN_WRITELN', 'writeln'),
    'begin': ('TOKEN_BEGIN', 'begin'),
    'end': ('TOKEN_END', 'end'),
    'program': ('TOKEN_PROGRAM', 'program'),
    'goto': ('TOKEN_GOTO', 'goto')
}

