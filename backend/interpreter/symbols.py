class Symbol():
    
    def __init__(self, id, type, value, varType, typeOf = 'variable', size = 0):
        self.id = id
        self.type = type
        self.value = value
        self.varType = varType
        self.typeOf = typeOf
        self.size = size

        self.position = None
    def setEnvironment(self, environment):
        self.environment = environment

    def setPosition(self, position):
        self.position = position

class TablaSymbols():

    def __init__(self, symbols = {}, environment = "global"):
        self.symbols = symbols
        self.previous = None
        self.environment = environment
    
    def find(self, id, exception = []):
        if id in self.symbols:
            return self.symbols[id]
        elif self.previous != None:
            return self.previous.find(id)
        else:
            exception.append('Error, variable no encontrada desde symbol: ' + id)
            return None

    def firstSymbol(self):
        return self.symbols[0]

    def add(self, symbol):
        self.symbols[symbol.id] = symbol

    def get(self, id, exception = []):
        if not id in self.symbols:
            exception.append('Error, variable no encontrada')
        else:
            return self.symbols[id]
    
    def getFunctions(self):
        functions = []
        for symbol in self.symbols:
            symbol2 = self.symbols[symbol]
            if symbol2.typeOf == 'function' or symbol2.typeOf == 'interface':
                functions.append(symbol2)

        if self.previous != None:
            functions = functions + self.previous.getFunctions()

        return functions

    def put(self, id, value, exception = []):
        if not id in self.symbols:
            exception.append('Error, variable no encontrada')
        else:
            self.symbols[id].value = value

    def removeClassFunction(self):
        for symbol in self.symbols:
            symbol2 = self.symbols[symbol]

            if symbol2.typeOf == 'class' or symbol2.typeOf == 'function' or symbol2.typeOf == 'interface':
                symbol2.value = symbol2.typeOf

    def clear(self):
        self.symbols = {}

    def toJson(self):
        return {
            'symbols': self.symbols,
        }
