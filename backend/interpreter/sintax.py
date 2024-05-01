from instructions import *

def p_init(t) :
    'init            : instrs'
    t[0] = t[1]

def p_instrs_list(t):
    'instrs    : instrs instr'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrs_interfaces(t) :
    'instrs    : instrs interface_instr'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrs_instr(t) :
    'instrs    : instr'
    t[0] = [t[1]]

def p_instrs_interface(t) :
    'instrs    : interface_instr'
    t[0] = [t[1]]

def p_instr(t) :
    '''instr    : statement SEMICOLON
                | statement_pop SEMICOLON
                | statement_push SEMICOLON
                | if_instr
                | switch_instr
                | while_instr
                | for_instr
                | for_each_instr
                | break_instr
                | continue_instr
                | console_instr
                | function_instr
                | return_instr
                | function_call_instr SEMICOLON
                
    '''
    t[0] = t[1]

def p_interface(t):
    'interface_instr : INTERFACE ID LBRACE interface_params RBRACE'
    t[0] = Interface(t[2], t[4])


def p_interface_params(t) :
    'interface_params : interface_params ID COLON function_type SEMICOLON'
    t[1].append([t[2], t[4]])
    t[0] = t[1]

def p_interface_params_param(t) :
    'interface_params : ID COLON function_type SEMICOLON'
    t[0] = [[t[1], t[3]]]


def p_function(t) :
    'function_instr : FUNCTION ID LPAREN function_params RPAREN COLON function_type LBRACE instrs RBRACE'
    t[0] = Function(t[2], t[4], t[7], t[9])

def p_function_void(t) :
    'function_instr : FUNCTION ID LPAREN function_params RPAREN LBRACE instrs RBRACE'
    t[0] = Function(t[2], t[4], None, t[7])

def p_function_type(t) :
    '''function_type : TYPE matriz_dimensions
                | TYPE
                | ID matriz_dimensions
                | ID
    '''
    if len(t) == 3:
        t[0] = [t[1], t[2]]
    else:
        t[0] = t[1]

def p_function_params(t) :
    'function_params : function_params COMMA ID COLON function_type'
    t[1].append([t[3], t[5]])
    t[0] = t[1]

def p_function_params_param(t) :
    'function_params : ID COLON function_type'
    t[0] = [[t[1], t[3]]]

def p_function_params_null(t) :
    'function_params : '
    t[0] = []


def p_functino_call(t) :
    'function_call_instr : ID LPAREN values RPAREN'
    t[0] = FunctionCall(t[1], t[3])

def p_functino_call_empty(t) :
    'function_call_instr : ID LPAREN RPAREN'
    t[0] = FunctionCall(t[1], [])

def p_return_instr(t) :
    'return_instr : RETURN statement_assign_value SEMICOLON'
    t[0] = Return(t[2])

def p_console(t) :
    'console_instr : CONSOLE DOT LOG LPAREN values RPAREN SEMICOLON'
    t[0] = Console(t[5])

def p_statement_implicit(t) :
    'statement : var_type ID statement_assign'
    t[0] = Statement(t[1], t[2], t[3])

def p_statement_explicit(t) :
    'statement : var_type ID COLON statement_type statement_assign'
    t[0] = Statement(t[1], t[2], t[5], t[4])

def p_statement_simple(t) :
    'statement : ID statement_assign'
    t[0] = Statement(None, t[1], t[2])

def p_statement_matriz(t) :
    'statement : var_type ID COLON statement_type matriz_dimensions ASSIGN matriz_dimensions_values'
    t[0] = Statement(t[1], t[2], Matrix(t[7]), t[4], t[5])

def p_statment_type(t) :
    '''statement_type : TYPE
                | ID
    '''
    t[0] = t[1]

def p_statement_matriz2(t) :
    'statement : ID matriz_dimensions_access ASSIGN statement_assign_value'
    t[0] = MatrixAssign(t[1], t[2], t[4])

def p_statement_assign_interface0(t) :
    'statement : interface_dimensions_access statement_assign'
    t[0] = InterfaceAssign(t[1], t[2])


def p_interface_dimenssions_access(t) :
    'interface_dimensions_access : interface_dimensions_access DOT factor'
    t[1].append(t[3])
    t[0] = t[1]

def p_interface_dimenssions_access2(t) :
    'interface_dimensions_access : factor DOT factor'
    t[0] = [t[1], t[3]]
    
    
def p_statament_array_push(t) :
    'statement_push : factor DOT PUSH LPAREN statement_assign_value RPAREN'
    t[0] = ArrayUtils('push', t[1], t[5])


def p_statement_array_pop(t) :
    'statement_pop : factor DOT POP LPAREN RPAREN'
    t[0] = ArrayUtils('pop', t[1], None)

def p_statement_matriz_assign_dimensions(t) :
    'matriz_dimensions : matriz_dimensions LBRACKET RBRACKET'
    t[0] = t[1] + 1


def p_statement_matriz_assign_dimension(t) :
    'matriz_dimensions : LBRACKET RBRACKET'
    t[0] = 1

def p_statement_matriz_assign_value(t) :
    'matriz_dimensions_access : matriz_dimensions_access LBRACKET statement_assign_value RBRACKET'
    t[0] = t[1] + [t[3]]

def p_statement_matriz_assign_value2(t) :
    'matriz_dimensions_access : LBRACKET statement_assign_value RBRACKET'
    t[0] = [t[2]]

def p_statement_matriz_assign_value_single(t) :
    'matriz_dimensions_values : LBRACKET  elements RBRACKET'
    t[0] = t[2]


def p_statement_matriz_assign_value_list(t) :
    'matriz_dimensions_values : LBRACKET RBRACKET'
    t[0] = []

def p_elements(t) :
    'elements : elements COMMA element'
    t[1].append(t[3])
    t[0] = t[1]


def p_element2(t) :
    'elements : element'
    t[0] = [t[1]]

def p_element3(t) :
    'element : statement_assign_value'
    t[0] = t[1]

def p_element4(t) :
    'element : matriz_dimensions_values'
    t[0] = Matrix(t[1])

def p_values_list(t):
    'values    : values COMMA statement_assign_value'
    t[1].append(t[3])
    t[0] = t[1]

def p_values_value(t) :
    'values    : statement_assign_value'
    t[0] = [t[1]]
    
def p_var_type(t) :
    '''var_type : VAR
                | CONST'''
    t[0] = t[1]

def p_statement_assign(t) :
    '''statement_assign : ASSIGN statement_assign_value
                | ASSIGNMENTOPERATOR statement_assign_value
                | ASSIGNMENTOPERATOR2
                | ASSIGN LBRACE statement_assign_interface  RBRACE
                '''     
    if t[1] == '=':
        if t[2] == '{':
            t[0] = InterfaceCall(t[3])
        else:
            t[0] = t[2]
    elif t[1] == '++':
        t[0] = AssignmentOperator('+=', Factor('NUMBER', 1))
    elif t[1] == '--':
        t[0] = AssignmentOperator('-=', Factor('NUMBER', 1))
    else:
        t[0] = AssignmentOperator(t[1], t[2])

def p_statement_assign_interface(t) :
    'statement_assign_interface : statement_assign_interface COMMA ID COLON statement_assign_value'
    t[1].append([t[3], t[5]])
    t[0] = t[1]

def p_statement_assign_interface2(t) :
    'statement_assign_interface : ID COLON statement_assign_value'
    t[0] = [[t[1], t[3]]]

def p_statement_assign_value(t) :
    '''statement_assign_value : ternary_operator
                | logical
                | statement_pop
                | statement_push'''
    t[0] = t[1]

def p_ternary_operator(t) :
    'ternary_operator : relation QUESTIONMARK relation COLON relation'
    t[0] = TernaryOperator(t[1], t[3], t[5])

def p_if_instr(t) :
    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE'
    t[0] = IfElse(t[3], t[6])

def p_if_else_instr(t) :
    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE ELSE LBRACE instrs RBRACE'
    t[0] = IfElse(t[3], t[6], t[10])

def p_if_else_if_instr(t) :
    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE ELSE if_instr'
    t[0] = IfElse(t[3], t[6], t[9])

def p_switch_instr(t) :
    'switch_instr      : SWITCH LPAREN logical RPAREN LBRACE cases RBRACE'
    t[0] = Switch(t[3], t[6])

def p_cases_list(t):
    'cases    : cases case'
    t[1].append(t[2])
    t[0] = t[1]

def p_cases_case(t) :
    'cases    : case'
    t[0] = [t[1]]

def p_case(t) :
    'case    : CASE logical COLON instrs'
    t[0] = Case(t[2], t[4])

def p_default(t) :
    'case    : DEFAULT COLON instrs'
    t[0] = Default(t[3])

def p_break(t) :
    'break_instr    : BREAK SEMICOLON'
    t[0] = Break()

def p_continue(t) :
    'continue_instr    : CONTINUE SEMICOLON'
    t[0] = Continue()

def p_while_instr(t) :
    'while_instr    : WHILE LPAREN logical RPAREN LBRACE instrs RBRACE'
    t[0] = While(t[3], t[6])

def p_for_instr(t) :
    'for_instr    : FOR LPAREN statement SEMICOLON logical SEMICOLON statement RPAREN LBRACE instrs RBRACE'
    t[0] = For(t[3], t[5], t[7], t[10])

def p_for_each_instr(t) :
    'for_each_instr    : FOR LPAREN var_type ID OF factor RPAREN LBRACE instrs RBRACE'
    t[0] = ForEach(t[4], t[6], t[9])

def p_logical(t) :
    'logical : logical LOGICALOPERATOR relation'
    t[0] = Logical(t[2], t[1], t[3])

def p_logical_relation(t) :
    'logical : relation'
    t[0] = t[1]

def p_relation(t) :
    'relation : relation RELATIONALOPERATOR arithmetic'
    t[0] = Relational(t[2], t[1], t[3])

def p_relation_arithmetic(t) :
    'relation : arithmetic'
    t[0] = t[1]

def p_arithmetic(t):
    'arithmetic : arithmetic arithmetic_operador_low term'
    t[0] = Arithmetic(t[2], t[1], t[3])

def p_adic_term(t):
    'arithmetic : term'
    t[0] = t[1]

def p_term(t):
    'term : term ARITHMETICOPERATORHIGH factor_function'
    t[0] = Arithmetic(t[2], t[1], t[3])

def p_term_factor(t):
    'term : factor_function'
    t[0] = t[1]

def p_factor_functions(t):
    '''factor_function : factor DOT INDEXOF LPAREN factor RPAREN
                | factor DOT TOSTRING LPAREN RPAREN
                | factor DOT JOIN LPAREN RPAREN
                | factor DOT LENGTH
                | factor DOT TOLOWERCASE LPAREN RPAREN
                | factor DOT TOUPPERCASE LPAREN RPAREN
                | OBJECT DOT KEYS LPAREN factor RPAREN
                | OBJECT DOT VALUES LPAREN factor RPAREN
    '''

    t[3] = t[3].lower()
    if isinstance(t[1], str):
        t[1] = t[1].lower()

    if t[3] == 'indexof':
        t[0] = ArrayUtils(t[3], t[1], t[5])
    elif t[3] == 'join':
        t[0] = ArrayUtils(t[3], t[1], None)
    elif t[1] == 'object':
        t[0] = InterfaceUtils(t[3], t[5], None)
    else: 
        t[0] = FactorUtils(t[3], t[1])

def p_factor_functions_natives(t):
    '''factor_function : PARSEINT LPAREN factor RPAREN
                | PARSEFLOAT LPAREN factor RPAREN
    '''
    t[0] = FactorUtils(t[1].lower(), t[3])

def p_factor_functions_factor(t):
    'factor_function : factor'
    t[0] = t[1]

def p_factor_interface(t):
    'factor_function : interface_dimensions_access'
    t[0] = InterfaceAccess(t[1])

def p_factor_typeof(t):
    'factor : TYPEOF factor'
    t[0] = FactorUtils('typeof', t[2])

def p_factor(t):
    'factor : ID '
    t[0] = Factor('ID', t[1])

def p_factor_double(t):
    'factor : FLOAT '
    t[0] = Factor('FLOAT', t[1])

def p_factor_text(t):
    'factor : STRING'
    t[0] = Factor('STRING', t[1])

def p_factor_number(t):
    'factor : NUMBER '
    t[0] = Factor('NUMBER', t[1])

def p_factor_matrix(t):
    'factor : ID matriz_dimensions_access'
    t[0] = MatrixAccess(t[1], t[2])

def p_factor_logical(t):
    'factor : LPAREN logical RPAREN '
    t[0] = t[2]

def p_factor_negation_number(t):
    'factor : MINUS LPAREN NUMBER RPAREN'
    t[0] = NegationUnary('NUMBER', t[3])

def p_factor_negation_double(t):
    'factor : MINUS LPAREN FLOAT RPAREN'
    t[0] = NegationUnary('-', t[3])

def p_factor_negation(t):
    'factor : LOGICALNEGATION factor'
    t[0] = NegationUnary('!', t[2])

def p_factor_boolean(t):
    '''factor : TRUE
                | FALSE'''
    t[0] = Factor('BOOLEAN', t[1])

def p_factor_call_function(t):
    'factor : function_call_instr'
    t[0] = t[1]

def p_arithmetic_operator_low(t):
    '''arithmetic_operador_low : PLUS
                | MINUS'''
    t[0] = t[1]

def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'")
        from main import putLexerError
        putLexerError("Error de sintaxis en línea " + str(p.lineno) + ", columna "+ str(p.lexpos) + ": Token inesperado "+ str(p.value) )
    else:
        print("Error de sintaxis")
        from main import putLexerError
        putLexerError("Error lexico")


