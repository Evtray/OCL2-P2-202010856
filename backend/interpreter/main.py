from lexer import *
from sintax import *
from symbols import *
import ply.lex as Lex
import ply.yacc as yacc
lexer = Lex.lex()
parser = yacc.yacc()
from tabulate import tabulate
from generator import Generator
import os

# declare static array errorsLexer
lexerErrors = []

def putLexerError(text):
    global lexerErrors
    lexerErrors.append(text)

def parse(input) :
    return parser.parse(input)

def execute(intrs, ts, console, exceptions, execute, gen):
    print('Ejecutando', intrs)
    for instr in intrs:
        if execute:
            print(instr)
            instr.execute(ts, console, exceptions, gen)
        else:
            if isinstance(instr, Function) or isinstance(instr, Interface): 
                instr.execute(ts, console, exceptions, gen)

def interpretText(text):
    global lexerErrors
    lexerErrors = []
    instrucciones = parse(text)
    ts = TablaSymbols()
    ts.clear()
    console = []
    exceptions = []
    gen = Generator()

    execute(instrucciones, ts, console, exceptions, False, gen)
    execute(instrucciones, ts, console, exceptions, True, gen)

    return ts, console, exceptions, lexerErrors, gen

if __name__ == '__main__':
    input_text = ""

    root = os.path.dirname(os.path.abspath(__file__))        
    with open(os.path.join(root, 'text.txt'), 'r') as file:
        input_text = file.read()

    lexerErrors = []
    instrucciones = parse(input_text)
    ts = TablaSymbols()
    console = []
    exceptions = []
    try:
        execute(instrucciones, ts, console, exceptions)
        execute(instrucciones, ts, console, exceptions, True)
    except Exception as e:
        print("Error", e)

    print('Tabla de símbolos')
    print(tabulate([[symbol.id, symbol.type, symbol.value, symbol.varType, symbol.typeOf, symbol.size] for symbol in ts.symbols.values()], headers=['ID', 'Type', 'Value', 'VarType', 'TypeOf', 'Size'], tablefmt='orgtbl'))
    print('\n')
    print('Consola')
    for c in console:
        print(c)

    print('\n')
    print('Errores')
    for e in exceptions:
        print(e)

    print('Errores lexicos')
    for e in lexerErrors:
        print(e)
