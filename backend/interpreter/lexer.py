reservadas = {
    'var':'VAR',
    'const':'CONST',
    'if':'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'console':'CONSOLE',
    'switch':'SWITCH',
    'case':'CASE',
    'default':'DEFAULT',
    'push':'PUSH',
    'pop':'POP',
    'indexof':'INDEXOF',
    'join':'JOIN',
    'length':'LENGTH',
    'log':'LOG',
    'parseint':'PARSEINT',
    'parsefloat':'PARSEFLOAT',
    'tostring':'TOSTRING',
    'tolowercase':'TOLOWERCASE',
    'touppercase':'TOUPPERCASE',
    'typeof':'TYPEOF',
    'of':'OF',
    'object':'OBJECT',
    'keys':'KEYS',
    'values':'VALUES',
    'interface':'INTERFACE',
}

tokens = [
    'TYPE', 
    'ASSIGNMENTOPERATOR', 
    'ASSIGNMENTOPERATOR2', 
    'RELATIONALOPERATOR', 
    'ARITHMETICOPERATORHIGH', 
    'LOGICALOPERATOR',
    'LOGICALNEGATION',
    'ASSIGN',
    'QUESTIONMARK', 
    'LPAREN', 
    'RPAREN',
    'LBRACE', 
    'RBRACE',
    'SEMICOLON', 
    'COMMA',
    'COLON', 
    'DOT', 
    'LBRACKET', 
    'RBRACKET', 
    'PLUS',
    'MINUS',
    'FLOAT',
    'NUMBER',
    'STRING',    
    'ID',

] + list(reservadas.values())

t_VAR  = r'var'
t_CONSOLE  = r'console'
t_CONST  = r'const'
t_IF  = r'if'
t_ELSE  = r'else'
t_WHILE  = r'while'
t_FOR  = r'for'
t_FUNCTION  = r'function'
t_RETURN  = r'return'
t_BREAK  = r'break'
t_CONTINUE  = r'continue'
t_TRUE  = r'true'
t_FALSE  = r'false'
t_SWITCH  = r'switch'
t_CASE  = r'case'
t_DEFAULT  = r'default'
t_PUSH  = r'push'
t_POP  = r'pop'
t_JOIN  = r'join'
t_LENGTH  = r'length'
t_LOG  = r'log'
t_TYPEOF  = r'typeof'
t_OBJECT  = r'object'
t_KEYS  = r'keys'
t_VALUES  = r'values'
t_INTERFACE  = r'interface'

t_ASSIGNMENTOPERATOR = r'\+=|-='
t_ASSIGNMENTOPERATOR2 = r'\+\+|--'
t_RELATIONALOPERATOR = r'==|!=|<=|>=|<|>'

t_PLUS = r'\+'
t_MINUS = r'-'
t_ARITHMETICOPERATORHIGH = r'\*|/|%|\^'
t_LOGICALOPERATOR = r'&&|\|\|'
t_LOGICALNEGATION = r'!'
t_ASSIGN = r'='
t_QUESTIONMARK = r'\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_ignore = " \t"

def t_TYPE(t):
    r'number|string|boolean|float|char'
    t.type = 'TYPE'
    return t

def t_STRING(t):
    r'\"(.+?)?\"'
    t.type = 'STRING'
    try:
        t.value = str(t.value)
    except ValueError:
        print("Error %d", t.value)
        from main import lexerErrors
        lexerErrors.append("Error en variable string")
        t.value = ''
    return t

def t_FLOAT(t):
    r'\d+(\.\d+)?'
    try:
        # validate if value contains a dot
        if t.value.find('.') != -1:
            t.value = float(t.value)
            t.type = 'FLOAT'
        else:
            t.value = int(t.value)
            t.type = 'NUMBER'

    except ValueError:
        t.value = 0
        t.type = 'FLOAT'
        from main import lexerErrors

        lexerErrors.append("Error en variable FLOAT")

    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t


def t_COMMENTLINE(t):
    r'\/\/.*'
    t.lexer.lineno += t.value.count("\n")

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')  

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Error Léxico '%s'" % t.value[0])
    from main import lexerErrors
    lexerErrors.append("Error Léxico '%s'" % t.value[0])
    t.lexer.skip(1)