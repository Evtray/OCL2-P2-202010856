# OLC 2 | PROYECTO 1  
## OLCScript IDE

# 📋 Indice

- [Indice](#Indice)
- [Información](#Información)
- [Manual de usuario](#Manual-de-usuario)
    - [Archivos](#Archivos)
    - [Editar](#Editar)
    - [Acerca De](#Acerca-De)
    - [Consolas](#Consolas)
    - [Reportes](#Reportes)
    - [Ejecutar](#Ejecutar)
- [Manual técnico](#Manual-técnico)
    - [Gramatica](#Gramatica)
    - [Análisis](#Análisis)
    - [Diagrama sintáctico](#Diagrama-sintáctico)
    - [Herramientas utilizadas](#Herramientas-utilizadas)

# Información
OLCScript IDE es un entorno de desarrollo que provee las herramientas para la escritura de programas en lenguaje OLCScript. Este IDE nos da la posibilidad de visualizar tanto la salida en consola de la ejecución del archivo fuente como los reportes de simbolos, funciones, errores y el cst. La Interfaz gráfica está basada en una página web realizada con Html, Css y JavaScript.

<div align="center">
    <a href="" target="_blank"><img src="https://i.imgur.com/sS1hrYd.png" style="width:30rem"></a>
</div>

# Manual de usuario
El usuario cuenta con las herramientas para el análisis de código a traves de una área de código, donde se cuenta con consolas de salida, errores, y tambien reportes de errores, símbolos, funciones, y árbol CST.

## Archivos
Se cuenta con la opción de cargar archivos y guardar el archivo.

<div align="center">
    <a href="" target="_blank"><img src="https://imgur.com/sS1hrYd.png" style="width:10rem"></a>
</div>

## Editar
Es la opción habilita la opción de escribir y/o modificar el texto en el área de código para su análisis.

<div align="center">
    <a href="" target="_blank"><img src="https://imgur.com/ifPgswx.png" style="width:25rem"></a>
</div>

## Consolas
Se puede ver tanto la salida del código en consola, y el listado de los errores.
<div align="center">
    <a href="" target="_blank"><img src="https://imgur.com/nXKzp5m.png" style="width:30rem"></a>
</div>

## Reportes
Muestra tanto los reportes de símbolos, funciones, errores y el cst. Pudiendo el usuario elegir cual reporte visualizar.

<div align="center">
    <a href="" target="_blank"><img src="https://imgur.com/MIRRywQ.png" style="width:17.5rem"></a>
</div>

## Ejecutar
Ejecuta el código escrito en el área de código.
<div align="center">
    <a href="" target="_blank"><img src="https://imgur.com/sS1hrYd.png" style="width:30rem"></a>
</div>

# Manual técnico

Para la realización de este proyecto se utilizó el lenguaje de programación Python con la libreria PLY, el cual nos permite realizar el análisis léxico, sintáctico y semántico del lenguaje OLCScript. Para la realización de la interfaz gráfica se utilizó Html, Css y JavaScript con el framework VUE.

## Gramatica

Gramatica utilizada con atlr4 para la realización del analizador sintáctico.

```

    'init            : instrs'

    'instrs    : instrs instr'

    'instrs    : instrs interface_instr'

    'instrs    : instr'

    'instrs    : interface_instr'

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

    'interface_instr : INTERFACE ID LBRACE interface_params RBRACE'


    'interface_params : interface_params ID COLON function_type SEMICOLON'


    'interface_params : ID COLON function_type SEMICOLON'


    'function_instr : FUNCTION ID LPAREN function_params RPAREN COLON function_type LBRACE instrs RBRACE'

    'function_instr : FUNCTION ID LPAREN function_params RPAREN LBRACE instrs RBRACE'

    '''function_type : TYPE matriz_dimensions
                | TYPE
                | ID matriz_dimensions
                | ID
    '''

    'function_params : function_params COMMA ID COLON function_type'

    'function_params : ID COLON function_type'

    'function_params : '

    'function_call_instr : ID LPAREN values RPAREN'

    'function_call_instr : ID LPAREN RPAREN'

    'return_instr : RETURN statement_assign_value SEMICOLON'

    'console_instr : CONSOLE DOT LOG LPAREN values RPAREN SEMICOLON'

    'statement : var_type ID statement_assign'

    'statement : var_type ID COLON statement_type statement_assign'

    'statement : ID statement_assign'
    t[0] = Statement(None, t[1], t[2])

    'statement : var_type ID COLON statement_type matriz_dimensions ASSIGN matriz_dimensions_values'

    '''statement_type : TYPE
                | ID
    '''

    'statement : ID matriz_dimensions_access ASSIGN statement_assign_value'

    'statement : interface_dimensions_access statement_assign'

    'interface_dimensions_access : interface_dimensions_access DOT factor'

    'interface_dimensions_access : factor DOT factor'
    
    'statement_push : factor DOT PUSH LPAREN statement_assign_value RPAREN'

    'statement_pop : factor DOT POP LPAREN RPAREN'

    'matriz_dimensions : matriz_dimensions LBRACKET RBRACKET'

    'matriz_dimensions : LBRACKET RBRACKET'

    'matriz_dimensions_access : matriz_dimensions_access LBRACKET statement_assign_value RBRACKET'

    'matriz_dimensions_access : LBRACKET statement_assign_value RBRACKET'

    'matriz_dimensions_values : LBRACKET  elements RBRACKET'

    'matriz_dimensions_values : LBRACKET RBRACKET'

    'elements : elements COMMA element'

    'elements : element'

    'element : statement_assign_value'


    'element : matriz_dimensions_values'


    'values    : values COMMA statement_assign_value'

    'values    : statement_assign_value'
    
    '''var_type : VAR
                | CONST'''

    '''statement_assign : ASSIGN statement_assign_value
                | ASSIGNMENTOPERATOR statement_assign_value
                | ASSIGNMENTOPERATOR2
                | ASSIGN LBRACE statement_assign_interface  RBRACE
                '''     

    'statement_assign_interface : statement_assign_interface COMMA ID COLON statement_assign_value'

    'statement_assign_interface : ID COLON statement_assign_value'

    '''statement_assign_value : ternary_operator
                | logical
                | statement_pop
                | statement_push'''

    'ternary_operator : relation QUESTIONMARK relation COLON relation'

    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE'

    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE ELSE LBRACE instrs RBRACE'

    'if_instr      : IF LPAREN logical RPAREN LBRACE instrs RBRACE ELSE if_instr'

    'switch_instr      : SWITCH LPAREN logical RPAREN LBRACE cases RBRACE'

    'cases    : cases case'

    'cases    : case'

    'case    : CASE logical COLON instrs'

    'case    : DEFAULT COLON instrs'

    'break_instr    : BREAK SEMICOLON'

    'continue_instr    : CONTINUE SEMICOLON'

    'while_instr    : WHILE LPAREN logical RPAREN LBRACE instrs RBRACE'

    'for_instr    : FOR LPAREN statement SEMICOLON logical SEMICOLON statement RPAREN LBRACE instrs RBRACE'

    'for_each_instr    : FOR LPAREN var_type ID OF factor RPAREN LBRACE instrs RBRACE'

    'logical : logical LOGICALOPERATOR relation'

    'logical : relation'

    'relation : relation RELATIONALOPERATOR arithmetic'

    'relation : arithmetic'

    'arithmetic : arithmetic arithmetic_operador_low term'

    'arithmetic : term'

    'term : term ARITHMETICOPERATORHIGH factor_function'

    'term : factor_function'

    '''factor_function : factor DOT INDEXOF LPAREN factor RPAREN
                | factor DOT TOSTRING LPAREN RPAREN
                | factor DOT JOIN LPAREN RPAREN
                | factor DOT LENGTH
                | factor DOT TOLOWERCASE LPAREN RPAREN
                | factor DOT TOUPPERCASE LPAREN RPAREN
                | OBJECT DOT KEYS LPAREN factor RPAREN
                | OBJECT DOT VALUES LPAREN factor RPAREN
    '''

    '''factor_function : PARSEINT LPAREN factor RPAREN
                | PARSEFLOAT LPAREN factor RPAREN
    '''

    'factor_function : factor'

    'factor_function : interface_dimensions_access'

    'factor : TYPEOF factor'

    'factor : ID '

    'factor : FLOAT '

    'factor : STRING'

    'factor : NUMBER '

    'factor : ID matriz_dimensions_access'

    'factor : LPAREN logical RPAREN '

    'factor : MINUS LPAREN NUMBER RPAREN'

    'factor : MINUS LPAREN FLOAT RPAREN'

    'factor : LOGICALNEGATION factor'

    '''factor : TRUE
                | FALSE'''

    'factor : function_call_instr'

    '''arithmetic_operador_low : PLUS
                | MINUS'''





```

## Herramientas utilizadas

- Python
- Html y Css
- JavaScript
- Ply
- Bootstrap
- Vue