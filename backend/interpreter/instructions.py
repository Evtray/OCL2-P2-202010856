from symbols import *
from value import Value


class Instruccion:
    """Clase abs de instrucciones"""

    def execute(self, exp, ts, consola, exception, gen):
        pass

    def prepareValues(left, right):
        posl = left.position
        posr = right.position

        if isinstance(left.position.value, Value):
            posl = left.position.value
        print("posl", posl.value)

        if isinstance(right.position.value, Value):
            posr = right.position.value
        print("posr", posr.value)

        return posl, posr


class Factor(Instruccion):
    """Clase abs de factores"""

    def __init__(self, type, value, typeOf="variable"):
        self.type = type
        self.value = value
        self.typeOf = typeOf
        self.position = None

    def execute(self, ts, consola, exception, gen):
        result = self.value
        type2 = self.type
        typeOf = "variable"
        temp = gen.new_temp()
        nameId = ""
        isTemp = False

        if self.type == "STRING":
            if self.value[0] == '"' or self.value[0] == "'":
                result = self.value[1:-1]
                result = self.converterEscapeSequences(result)

            nameId = "str_" + str(temp)
            gen.variable_data(nameId, "string", str(self.value))

        if self.type == "ID":
            symbol = ts.find(self.value, exception)
            if symbol == None:
                exception.append("Error, variable no encontrada")
                nameId = ""
                type2 = "NULL"
                result = ""
            else:
                result = symbol.value
                type2 = symbol.type
                typeOf = symbol.typeOf
                nameId = symbol.position
        else:
            if self.type == "FLOAT":
                gen.add_br()
                gen.comment("Agregando un primitivo numerico")
                gen.add_li("t0", str(self.value))
                gen.add_li("t3", str(temp))
                gen.add_sw("t0", "0(t3)")
                result = float(result)
                nameId = str(temp)
                isTemp = True
            elif self.type == "NUMBER":
                gen.add_br()
                gen.comment("Agregando un primitivo numerico")
                gen.add_li("t0", str(self.value))
                gen.add_li("t3", str(temp))
                gen.add_sw("t0", "0(t3)")
                result = int(result)
                nameId = str(temp)
                isTemp = True
            elif self.type == "BOOLEAN":
                result = result == "true"
                isTemp = True
                gen.add_br()
                gen.comment("Agregando un primitivo booleano")
                if result:
                    gen.add_li("t0", "1")
                else:
                    gen.add_li("t0", "0")
                gen.add_li("t3", str(temp))
                gen.add_sw("t0", "0(t3)")
                nameId = str(temp)
            elif self.type == "CHAR":
                result = str(result)
                nameId = "char_" + str(temp)
                gen.variable_data(nameId, "byte", "'" + str(self.value) + "'")

        factor2 = Factor(type2, result, typeOf)
        factor2.position = Value(nameId, isTemp, self.type, [], [], [])

        return factor2

    def converterEscapeSequences(self, value):
        return (
            value.replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
            .replace("\\t", "\t")
            .replace("\\'", "'")
        )


class FactorUtils(Instruccion):
    """Clase abs de factor utils"""

    def __init__(self, type, exp, exp2=None):
        self.type = type
        self.exp = exp
        self.exp2 = exp2

    def execute(self, ts, consola, exception, gen):
        if self.type == "length":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf == "matrix":
                return Factor("NUMBER", len(result.value))

            if result.type == "STRING":
                return Factor("NUMBER", len(result.value))

            exception.append("Error, tipo de dato no valido para length")

        if self.type == "parseint":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.type == "STRING":
                try:
                    return Factor("NUMBER", int(result.value))
                except:
                    exception.append("Error, no se pudo convertir a entero")
            else:
                exception.append("Error, tipo de dato no valido para parseInt")

        if self.type == "parsefloat":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.type == "STRING":
                try:
                    return Factor("FLOAT", float(result.value))
                except:
                    exception.append("Error, no se pudo convertir a FLOAT")
            else:
                exception.append("Error, tipo de dato no valido para parseFloat")

        if self.type == "tostring":
            result = self.exp.execute(ts, consola, exception, gen)
            return Factor("STRING", str(result.value))

        if self.type == "tolowercase":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.type == "STRING":
                return Factor("STRING", result.value.lower())
            else:
                exception.append("Error, tipo de dato no valido para toLowerCase")

        if self.type == "touppercase":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.type == "STRING":
                return Factor("STRING", result.value.upper())
            else:
                exception.append("Error, tipo de dato no valido para toUpperCase")

        if self.type == "typeof":
            result = self.exp.execute(ts, consola, exception, gen)

            if (
                result.typeOf == "variable"
                or result.typeOf == "dict"
                or result.typeOf == "matrix"
            ):
                return Factor("STRING", result.type)
            else:
                return Factor("STRING", result.typeOf)

        return None


class Statement(Instruccion):
    """Clase abs de statement"""

    def __init__(self, varType, id, expression, type=None, size=0):
        self.varType = varType
        self.id = id
        self.expression = expression
        self.type = type
        self.size = size

    def execute(self, ts, consola, exception, gen):
        typeOf = "variable"
        if isinstance(self.expression, AssignmentOperator):
            self.expression.setID(self.id)

        if isinstance(self.expression, InterfaceCall):
            typeOf = "dict"
            self.expression.setID(self.type)

        if self.type != None:
            self.type = self.type.upper()

        if isinstance(self.expression, Matrix):
            typeOf = "matrix"
            self.expression.setType(self.type)

        result = self.expression.execute(ts, consola, exception, gen)
        valid = True

        if self.varType == None:
            symbol = ts.find(self.id)
            if symbol == None:
                exception.append("Error, variable no encontrada" + self.id)
            else:
                # validate if the variable is a constant
                if symbol.varType == "const":
                    exception.append("Error, variable es constante" + symbol.id)
                else:
                    if symbol.type == result.type:
                        symbol.value = result.value
                    else:
                        if symbol.type == "FLOAT" and result.type == "NUMBER":
                            symbol.value = float(result.value)
                        else:
                            valid = False
                            exception.append(
                                "Error, tipo de dato no coincide "
                                + symbol.type
                                + " "
                                + result.type
                                + " en"
                                + self.id
                            )

                   
                    if valid:
                        if result.position.isTemp:
                            gen.add_li("t0", result.position.value)
                            gen.add_lw("t1", "0(t0)")
                        else:
                            gen.add_li("t1", str(result.value))

                        gen.add_li("t3", str(symbol.position.value))
                        gen.add_sw("t1", "0(t3)")

                        gen.comment("Fin asignacion")
        else:
            # validate if the variable already exists
            symbol = ts.find(self.id)
            if symbol != None:
                exception.append("Error, variable ya existe: " + self.id)
            else:
                if self.type == None:
                    isType = result.type
                else:
                    isType = self.type

                if (isType == result.type) or (
                    self.type == "FLOAT" and result.type == "NUMBER"
                ):
                    symbol2 = Symbol(
                        self.id, isType, result.value, self.varType, typeOf, self.size
                    )
                    print("result position", result.position.value)
                    symbol2.setPosition(result.position)
                    symbol2.setEnvironment(ts.environment)
                    ts.add(symbol2)
                else:
                    exception.append(
                        "Error, tipo de dato no coincide "
                        + isType
                        + " "
                        + result.type
                        + " en"
                        + self.id
                    )

        # except:
        #     exception.append("Error al declara variable: " + self.id)

        return None
class AssignmentOperator(Instruccion):
    """Clase abs de operadores de asignacion"""

    def __init__(self, type, expression):
        self.type = type
        self.expression = expression

    def setID(self, id):
        self.id = id

    def execute(self, ts, consola, exception, gen):
        result = self.expression.execute(ts, consola, exception, gen)

        symbol = ts.find(self.id)
        if symbol == None:
            exception.append("Error, variable no encontrada" + self.id)
        else:
            # validate if the variable is a constant
            if symbol.varType == "const":
                exception.append("Error, variable es constante" + symbol.id)
            else:
                # validate if the type of the variable is the same as the result
                if symbol.type == result.type:
                    # validate type same text, number or FLOAT
                    if (
                        symbol.type == "STRING"
                        or symbol.type == "NUMBER"
                        or symbol.type == "FLOAT"
                    ):
                        if self.type == "+=":
                            result.value = symbol.value + result.value
                        elif self.type == "-=":
                            result.value = symbol.value - result.value
                    else:
                        exception.append(
                            "tipo de dato no valido para operador de asignacion"
                            + self.type
                            + " "
                            + symbol.type
                            + " "
                            + result.type
                            + " en"
                            + self.id
                        )
                else:
                    exception.append(
                        "Error, tipo de dato no coincide "
                        + symbol.type
                        + " "
                        + result.type
                        + " en"
                        + self.id
                    )

        return result


class Arithmetic(Instruccion):
    """Clase abs de operaciones aritmeticas"""

    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right

    def execute(self, ts, consola, exception, gen):
        left = self.left.execute(ts, consola, exception, gen)
        right = self.right.execute(ts, consola, exception, gen)
        op = ""
        comesString = left.type == "STRING" or right.type == "STRING"

        if self.type == "+":
            if left.type == "STRING" and right.type == "STRING":
                return Factor("STRING", str(left.value) + str(right.value))

        if comesString:
            exception.append(
                "Error, tipo de dato no valido para operador aritmetico "
                + self.type
                + " "
                + left.type
                + " "
                + right.type
            )
            return None

        validLeft = left.type == "NUMBER" or left.type == "FLOAT"
        validRight = right.type == "NUMBER" or right.type == "FLOAT"
        comesFLOAT = left.type == "FLOAT" or right.type == "FLOAT"

        returnType = "FLOAT" if comesFLOAT else "NUMBER"
        returnValue = 0
        if not (validLeft and validRight):
            exception.append(
                "Error, tipo de dato no valido para operador aritmetico "
                + self.type
                + " "
                + left.type
                + " "
                + right.type
            )
            return None

        if self.type == "+":
            returnValue = left.value + right.value
            op = "add"
        if self.type == "-":
            returnValue = left.value - right.value
            op = "sub"
        elif self.type == "*":
            returnValue = left.value * right.value
            op = "mul"
        elif self.type == "/":
            if right.value == 0:
                exception.append(
                    "Error, division por cero"
                    + self.type
                    + " "
                    + left.type
                    + " "
                    + right.type
                )
                return None
            returnValue = left.value / right.value
            op = "div"
        elif self.type == "%":
            if right.value == 0:
                exception.append(
                    "Error, division por cero"
                    + self.type
                    + " "
                    + left.type
                    + " "
                    + right.type
                )
                return None
            returnValue = left.value % right.value
            op = "rem"
        elif self.type == "^":
            returnValue = left.value**right.value
            op = "mul"

        

        gen.add_operation_values(left, right)
        nameId = gen.add_operation_arit(op)

        factor = Factor(returnType, returnValue)
        factor.position = Value(nameId, True, returnType, [], [], [])

        return factor


class Relational(Instruccion):
    """Clase abs de operaciones relacionales"""

    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right

    def execute(self, ts, consola, exception, gen):
        left = self.left.execute(ts, consola, exception, gen)
        right = self.right.execute(ts, consola, exception, gen)
        result = None

        gen.add_br()
        gen.comment("Realizando operacion")

        gen.add_operation_values(left, right)

        temp = gen.new_temp()

        trueLvl = gen.new_label()
        falseLvl = gen.new_label()

        if self.type == "==":
            result = Factor("BOOLEAN", left.value == right.value)
            gen.add_beq("t1", "t2", trueLvl)
        elif self.type == "!=":
            result = Factor("BOOLEAN", left.value != right.value)
            gen.add_bne("t1", "t2", trueLvl)
        elif self.type == ">":
            result = Factor("BOOLEAN", left.value > right.value)
            gen.add_bgt("t1", "t2", trueLvl)
        elif self.type == "<":
            print("menor", left.value)
            print("asdfasdf", right.value)
            result = Factor("BOOLEAN", left.value < right.value)
            gen.add_blt("t1", "t2", trueLvl)
        elif self.type == ">=":
            result = Factor("BOOLEAN", left.value >= right.value)
            gen.add_bge("t1", "t2", trueLvl)
        elif self.type == "<=":
            result = Factor("BOOLEAN", left.value <= right.value)
            gen.add_ble("t1", "t2", trueLvl)

        gen.add_jump(falseLvl)
        result2 = Value(temp, True, "BOOLEAN", [], [], [])
        result2.truelvl.append(trueLvl)
        result2.falselvl.append(falseLvl)

        newLabel = gen.new_label()
        for lvl in result2.truelvl:
            gen.new_body_label(lvl)

            gen.add_li("t0", str(1))
            gen.add_li("t3", temp)
            gen.add_sw("t0", "0(t3)")
            gen.add_jump(newLabel)

        for lvl in result2.falselvl:
            gen.new_body_label(lvl)

            gen.add_li("t0", str(0))
            gen.add_li("t3", temp)
            gen.add_sw("t0", "0(t3)")

        gen.new_body_label(newLabel)

        result.position = result2

        return result


class Logical(Instruccion):
    """Clase abs de operaciones logicas"""

    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right

    def execute(self, ts, consola, exception, gen):
        left = self.left.execute(ts, consola, exception, gen)
        right = self.right.execute(ts, consola, exception, gen)
        result = None

        if self.type == "&&":
            result = Factor("BOOLEAN", left.value and right.value)
        elif self.type == "||":
            result = Factor("BOOLEAN", left.value or right.value)

        if self.type == "&&":
            type2 = "and"
        else:
            type2 = "or"

        gen.add_operation_values(left, right)
        nameId = gen.add_operation_arit(type2)
        result.position = Value(nameId, True, "BOOLEAN", [], [], [])

        return result


class NegationUnary(Instruccion):
    """Clase abs de operaciones de negacion unaria"""

    def __init__(self, type, value):
        self.value = value
        self.type = type

    def execute(self, ts, consola, exception, gen):
        type2 = "BOOLEAN"
        if self.type == "!":
            result = self.value.execute(ts, consola, exception, gen)
            if result.type != "BOOLEAN":
                exception.append(
                    "Error, tipo de dato no valido para operador unario "
                    + self.type
                    + " "
                    + result.type
                )
                factor = Factor("BOOLEAN", False)
                nameId = ""
            else:
                factor = Factor("BOOLEAN", not result.value)

                bool = 1 if result.value else 0
                gen.add_operation_values_simple(1, bool)
                nameId = gen.add_operation_arit("xor")
        else:
            factor = Factor(self.type, self.value * -1)
            gen.add_operation_values_simple(-1, str(self.value))
            nameId = gen.add_operation_arit("mul")
            type2 = "NUMBER"

        factor.position = Value(nameId, True, type2, [], [], [])

        return factor


class TernaryOperator(Instruccion):
    """Clase abs de operador ternario"""

    def __init__(self, condition, trueValue, falseValue):
        self.condition = condition
        self.trueValue = trueValue
        self.falseValue = falseValue

    def execute(self, ts, consola, exception, gen):
        condition = self.condition.execute(ts, consola, exception, gen)
        if condition.value:
            return self.trueValue.execute(ts, consola, exception, gen)
        else:
            return self.falseValue.execute(ts, consola, exception, gen)


def executeInstrs(instrs, ts, consola, exception, gen):
    result = None
    for instr in instrs:
        result = instr.execute(ts, consola, exception, gen)

        if result == "break" or result == "continue" or result != None:
            return result

    return result


class If(Instruccion):
    """Clase abs de If"""

    def __init__(self, condition, instrs):
        self.condition = condition
        self.instrs = instrs

    def execute(self, ts, consola, exception, gen):
        return None


class IfElse(Instruccion):
    """Clase abs de IfElse"""

    def __init__(self, condition, instrs=[], elseInstrs=None):
        self.condition = condition
        self.instrs = instrs
        self.elseInstrs = elseInstrs

    def execute(self, ts, consola, exception, gen):

        tsLocal = TablaSymbols({})
        tsLocal.previous = ts

        condition = self.condition.execute(ts, consola, exception, gen)
        temp = gen.new_temp()
        gen.add_br()
        gen.comment("Agregando un primitivo booleano")
        gen.add_li("t0", "1")
        gen.add_li("t3", temp)
        gen.add_sw("t0", "0(t3)")

        gen.add_operation_values(condition, temp)

        trueLvl = gen.new_label()
        falseLvl = gen.new_label()

        exit = gen.new_label()

        gen.add_beq("t1", "t2", trueLvl)
        gen.add_jump(falseLvl)

        gen.new_body_label(trueLvl)

        executeInstrs(self.instrs, tsLocal, consola, exception, gen)

        gen.add_jump(exit)

        gen.new_body_label(falseLvl)
        if self.elseInstrs != None:
            if isinstance(self.elseInstrs, IfElse):
                self.elseInstrs.execute(tsLocal, consola, exception, gen)
            else:
                executeInstrs(self.elseInstrs, tsLocal, consola, exception, gen)

        gen.new_body_label(exit)


class Switch(Instruccion):
    """Clase abs de Switch"""

    def __init__(self, value, cases):
        self.value = value
        self.cases = cases

    def execute(self, ts, consola, exception, gen):
        exit = gen.new_label()
        gen.BreakLabel = exit

        casesres = []

        for i in range(len(self.cases)):
            temp1 = gen.new_temp()
            gen.add_br()
            gen.comment("Agregando un primitivo booleano")
            gen.add_li("t0", "1")
            gen.add_li("t3", temp1)
            gen.add_sw("t0", "0(t3)")

            case = self.cases[i]
            condicionMain = self.value

            if case.value == None:
                condition1 = Factor("BOOLEAN", True)
                condicionMain = condition1
            else:
                condition1 = case.value

            condition = Relational("==", condition1, condicionMain)
            condition = condition.execute(ts, consola, exception, gen)
            temp = gen.new_temp()
            gen.add_br()
            gen.comment("Agregando un primitivo booleano")
            gen.add_li("t0", "1")
            gen.add_li("t3", temp)
            gen.add_sw("t0", "0(t3)")

            gen.add_operation_values(condition, temp)

            trueLvl = gen.new_label()
            gen.add_beq("t1", "t2", trueLvl)

            casesres.append({
                "instrs": case.instrs,
                "label": trueLvl
            })


        for case in casesres:
            gen.new_body_label(case["label"])
            executeInstrs(case["instrs"], ts, consola, exception, gen)

        gen.new_body_label(exit)


class Break(Instruccion):
    """Clase abs de Break"""

    def __init__(self):
        pass

    def execute(self, ts, consola, exception, gen):
        gen.add_jump(gen.BreakLabel)


class Case(Instruccion):
    """Clase abs de Case"""

    def __init__(self, value, instrs):
        self.value = value
        self.instrs = instrs


class Default(Instruccion):
    """Clase abs de Default"""

    def __init__(self, instrs):
        self.instrs = instrs
        self.value = None


class Return(Instruccion):
    """Clase abs de Return"""

    def __init__(self, expression):
        self.expression = expression

    def execute(self, ts, consola, exception, gen):
        return self.expression.execute(ts, consola, exception, gen)


class Continue(Instruccion):
    """Clase abs de Continue"""

    def __init__(self):
        pass

    def execute(self, ts, consola, exception, gen):
        gen.add_jump(gen.ContinueLabel)


class While(Instruccion):
    """Clase abs de While"""

    def __init__(self, condition, instrs):
        self.condition = condition
        self.instrs = instrs

    def execute(self, ts, consola, exception, gen):
        print("while", ts)
        tsLocal = TablaSymbols({}, ts.environment)
        tsLocal.previous = ts
        lbinit = gen.new_label()
        gen.new_body_label(lbinit)

        lbbreak = gen.new_label()
        gen.BreakLabel = lbbreak
        gen.ContinueLabel = lbinit
        
        condition = self.condition.execute(ts, consola, exception, gen)
        temp = gen.new_temp()
        gen.add_br()
        gen.comment('condition')
        gen.add_li('t0', '1')
        gen.add_li('t3', str(temp))
        gen.add_sw('t0', '0(t3)')

        gen.add_br()
        gen.add_li('t3', str(condition.position.value))
        gen.add_lw('t1', '0(t3)')
        gen.add_li('t3', str(temp))
        gen.add_lw('t2', '0(t3)')

        trueLvl = gen.new_label()
        gen.comment('conditmero mero ion')
        gen.add_beq('t1', 't2', trueLvl)
        gen.add_jump(lbbreak)

        gen.new_body_label(trueLvl)
        executeInstrs(self.instrs, tsLocal, consola, exception, gen)
        gen.add_jump(lbinit)
        gen.new_body_label(lbbreak)

        gen.BreakLabel = ""
        gen.ContinueLabel = ""
        
class For(Instruccion):
    """Clase abs de For"""

    def __init__(self, statement1, condition, statement2, instrs):
        self.statement1 = statement1
        self.condition = condition
        self.statement2 = statement2
        self.instrs = instrs

    def execute(self, ts, consola, exception, gen):

        tsLocal = TablaSymbols({})
        tsLocal.previous = ts
        self.statement1.execute(tsLocal, consola, exception)
        condition = self.condition.execute(tsLocal, consola, exception)

        while condition.value:
            result = executeInstrs(self.instrs, tsLocal, consola, exception)

            if result == "break":
                return None

            if result == "continue":
                self.statement2.execute(tsLocal, consola, exception)
                condition = self.condition.execute(tsLocal, consola, exception)
                continue

            if result != None:
                return result
            self.statement2.execute(tsLocal, consola, exception)
            condition = self.condition.execute(tsLocal, consola, exception)
            save = tsLocal.find(self.statement1.id)
            tsLocal.symbols = {}
            tsLocal.add(save)

        return None


class ForEach(Instruccion):
    """Clase abs de ForEach"""

    def __init__(self, id, array, instrs):
        self.id = id
        self.array = array
        self.instrs = instrs

    def execute(self, ts, consola, exception, gen):
        array = self.array.execute(ts, consola, exception, gen)
        tsLocal = TablaSymbols({})
        tsLocal.previous = ts

        symbol = Symbol(self.id, array.type, None, "const", "variable")
        for value in array.value:
            tsLocal.symbols = {}
            tsLocal.add(symbol)

            symbol.value = value

            result = executeInstrs(self.instrs, tsLocal, consola, exception)
            if result == "break":
                return None

            if result == "continue":
                continue

            if result != None:
                return result

        return None


class Matrix(Instruccion):
    """Clase abs de Matrix"""

    def __init__(self, exps):
        self.exps = exps

    def execute(self, ts, consola, exception, gen):
        result = []
        for exp in self.exps:
            if isinstance(exp, Matrix):
                exp.setType(self.type)
                result2 = exp.execute(ts, consola, exception, gen)
                if result2.type != self.type:
                    exception.append(
                        "Error, tipo de dato no coincide "
                        + self.type
                        + " "
                        + result2.type
                    )
                    return Factor(self.type, [], "matrix")

                result.append(result2.value)
            else:
                result2 = exp.execute(ts, consola, exception, gen)
                if result2.type != self.type:
                    exception.append(
                        "Error, tipo de dato no coincide "
                        + self.type
                        + " "
                        + result2.type
                    )
                    return Factor(self.type, [], "matrix")
                result.append(result2.value)

        return Factor(self.type, result, "matrix")

    def setType(self, type):
        self.type = type


# class ArrayAccess(Instruccion):
#     '''Clase abs de ArrayAccess'''
#     def __init__(self, id, index):
#         self.id = id
#         self.index = index

#     def execute(self, ts, consola, exception, gen):
#         symbol = ts.find(self.id, exception)
#         if symbol == None:
#             exception.append('Error, variable no encontrada')
#             return Factor('TEXT', 'Error, variable no encontrada')

#         index = self.index.execute(ts, consola, exception, gen)
#         if index.type != 'NUMBER':
#             exception.append('Error, tipo de dato no coincide NUMBER ' + index.type)
#             return Factor('TEXT', 'Error, tipo de dato no coincide NUMBER ' + index.type)

#         if index.value < 0 or index.value >= len(symbol.value):
#             exception.append('Error, indice fuera de rango')
#             return Factor('TEXT', 'Error, indice fuera de rango')

#         return Factor(symbol.type, symbol.value[index.value])


class MatrixAccess(Instruccion):
    """Clase abs de MatrixAccess"""

    def __init__(self, id, index):
        self.id = id
        self.index = index

    def execute(self, ts, consola, exception, gen):
        symbol = ts.find(self.id, exception)
        if symbol == None:
            exception.append("Error, variable no encontrada " + self.id)
            return None

        if symbol.typeOf != "matrix":
            exception.append("Error, variable no es una matriz " + self.id)
            return None

        if len(self.index) != symbol.size:
            exception.append("Error, dimensiones no coinciden " + self.id)
            return None

        indexes = []
        sizeIndex = 1
        for index in self.index:
            result = index.execute(ts, consola, exception, gen)
            if result.type != "NUMBER":
                exception.append(
                    "Error, tipo de dato no coincide NUMBER " + result.type
                )
                return None

            if result.value < 0 or sizeIndex > symbol.size:
                exception.append("Error, indice fuera de rango")
                return None

            sizeIndex += 1
            indexes.append(result.value)

        try:
            return Factor(symbol.type, self.getValue(symbol.value, indexes))
        except:
            exception.append("Error, lista fuera de rango" + self.id)
            return None

    def getValue(self, matrix, indexes):
        if len(indexes) == 1:
            return matrix[indexes[0]]

        return self.getValue(matrix[indexes[0]], indexes[1:])


class Console(Instruccion):
    """Clase abs de Console"""

    def __init__(self, exps):
        self.exps = exps

    def execute(self, ts, consola, exception, gen):

        text = ""
        for exp in self.exps:
            result2 = exp.execute(ts, consola, exception, gen)
            text += str(result2.value)
            if isinstance(result2.position.value, Value):
                position = result2.position.value
            else:
                position = result2.position
            if result2 == None:
                continue
            elif position.type == "NULL":
                return None
            elif position.type == "NUMBER":
                # Imprimiendo expresion
                print("Imprimiendo expresion", position.value)
                gen.add_br()
                if "t" in str(position.value):
                    gen.add_move("t3", str(position.value))
                else:
                    gen.add_li("t3", str(position.value))
                gen.add_lw("a0", "0(t3)")
                gen.add_li("a7", "1")
                gen.add_system_call()
            elif position.type == "STRING" or position.type == "CHAR":
                gen.add_br()
                if "t" in str(position.value) and len(str(position.value)) < 2:
                    gen.add_move("a0", str(position.value))
                else:
                    gen.add_la("a0", str(position.value))
                gen.add_li("a7", "4")
                gen.add_system_call()
            elif position.type == "BOOLEAN":
                # Agregando un primitivo booleano
                temp = gen.new_temp()
                gen.add_br()
                gen.comment("Agregando un primitivo booleano")
                gen.add_li("t0", "1")
                gen.add_li("t3", str(temp))
                gen.add_sw("t0", "0(t3)")
                # Creando temporales
                gen.add_br()
                gen.add_li("t3", str(position.value))
                gen.add_lw("t1", "0(t3)")
                gen.add_li("t3", str(temp))
                gen.add_lw("t2", "0(t3)")
                # Generando etiquetas
                trueLvl = gen.new_label()
                falseLvl = gen.new_label()
                # Agregando condición
                gen.add_beq("t1", "t2", trueLvl)
                # Agregando salto
                gen.add_jump(falseLvl)
                # Result
                result = Value("", False, "BOOLEANO", [], [], [])
                result.truelvl.append(trueLvl)
                result.falselvl.append(falseLvl)
                # Etiqueta de salida
                newLabel = gen.new_label()
                # Se agregan las etiquetas verdaderas
                for lvl in result.truelvl:
                    gen.new_body_label(lvl)
                # Imprimiendo expresion
                gen.add_br()
                gen.add_la("a0", "str_true")
                gen.add_li("a7", "4")
                gen.add_system_call()
                # Imprimiendo salto de linea
                gen.add_br()
                gen.add_li("a0", "10")
                gen.add_li("a7", "11")
                gen.add_system_call()
                # Salto etiqueta de salida
                gen.add_jump(newLabel)
                # Se agregan las etiquetas falsas
                for lvl in result.falselvl:
                    gen.new_body_label(lvl)
                # Imprimiendo expresion
                gen.add_br()
                gen.add_la("a0", "str_false")
                gen.add_li("a7", "4")
                gen.add_system_call()
                # Imprimiendo salto de linea
                gen.add_br()
                gen.add_li("a0", "10")
                gen.add_li("a7", "11")
                gen.add_system_call()
                # Etiqueta de salida
                gen.new_body_label(newLabel)
            else:
                exception.append("Error, tipo de dato no valido para imprimir")
                return None

        gen.add_br()
        gen.add_li("a0", "10")
        gen.add_li("a7", "11")
        gen.add_system_call()

        consola.append(text)
        return None


class Function(Instruccion):
    """Clase abs de funciones"""

    def __init__(self, id, params, type, instrs):
        self.id = id
        self.params = params
        self.type = type
        self.instrs = instrs
        self.init = True

    def execute(self, ts, consola, exception, gen):
        if self.init:
            typeFunction = "void"
            if self.type != None:
                typeFunction = self.type.upper()
            symbol = Symbol(self.id, typeFunction, self, "var", "function")
            symbol.setEnvironment(ts.environment)
            if self.id in ts.symbols:
                exception.append(f"Function {self.id} already exists")

            ts.add(symbol)
            self.init = False


class FunctionCall(Instruccion):
    """Clase abs de llamadas a funciones"""

    def __init__(self, id, params):
        self.id = id
        self.params = params

    def execute(self, ts, consola, exception, gen):
        function = ts.find(self.id, exception)

        if function == None:
            exception.append("Error, funcion no encontrada, " + self.id)
            return None
        function = function.value
        if len(function.params) != len(self.params):
            exception.append("Error, numero de parametros no coincide en " + self.id)
            return None

        tsLocal = TablaSymbols({}, self.id)
        symbolsFunction = ts.getFunctions()

        for symbol in symbolsFunction:
            tsLocal.add(symbol)

        for i in range(len(function.params)):
            param = function.params[i]
            result = self.params[i].execute(ts, consola, exception, gen)
            size = 0
            if isinstance(param[1], list):
                paramType = param[1][0].upper()
                size = param[1][1]
            else:
                paramType = str(param[1]).upper()

            print(paramType, result.type)
            if result.type != paramType:
                exception.append(
                    "Error, tipo de dato no coincide en "
                    + param[0]
                    + " "
                    + paramType
                    + " "
                    + result.type
                )
                return None

            typeOf = "variable" if size == 0 else "matrix"

            symbol = Symbol(param[0], paramType, result.value, "var", typeOf, size)
            symbol.setEnvironment(self.id)

            tsLocal.add(symbol)

        result = executeInstrs(function.instrs, tsLocal, consola, exception)

        print(result, "result")

        if isinstance(result, Factor):
            # validate type of return
            if function.type != "void" and result.type != function.type.upper():
                exception.append(
                    "Error, tipo de dato no coincide en "
                    + self.id
                    + " "
                    + function.type
                    + " "
                    + result.type
                )
                return None

        return result


class Interface(Instruccion):
    """Clase abs de interfaces"""

    def __init__(self, id, params):
        self.id = id
        self.params = params
        self.init = True

    def execute(self, ts, consola, exception, gen):
        if self.init:
            symbol = Symbol(self.id, "void", self, "var", "interface")
            symbol.setEnvironment("global")

            if self.id in ts.symbols:
                exception.append(f"Interface {self.id} already exists")

            ts.add(symbol)
            self.init = False


class InterfaceCall(Instruccion):
    """Clase abs de llamadas a interfaces"""

    def __init__(self, params):
        self.params = params

    def setID(self, id):
        self.id = id

    def execute(self, ts, consola, exception, gen):

        dictParams = {}

        for param2 in self.params:
            dictParams[param2[0]] = None

        try:
            interface2 = ts.find(self.id, exception)
            if interface2 == None:
                exception.append("Error, interface no encontrada")
                return None

            interface2 = interface2.value

            if len(interface2.params) != len(self.params):
                exception.append(
                    "Error, numero de parametros no coincide en interface " + self.id
                )
                return None

            for param in self.params:
                result = param[1].execute(ts, consola, exception, gen)
                interfaceParam = None

                for param2 in interface2.params:
                    if param2[0] == param[0]:
                        interfaceParam = param2
                        break

                if interfaceParam == None:
                    exception.append(
                        "Error, parametro no encontrado en interface " + param[0]
                    )
                    return None

                if result.type != interfaceParam[1].upper():
                    exception.append(
                        "Error, tipo de dato no coincide en "
                        + param[0]
                        + " "
                        + interfaceParam[1]
                        + " "
                        + result.type
                    )
                    return None

                dictParams[param[0]] = result.value
        except:
            exception.append("Error al llamar interface: " + self.id)

        return Factor(self.id.upper(), dictParams, "dict")


class InterfaceAssign(Instruccion):
    """Clase abs de asignacion de interfaces"""

    def __init__(self, interfaceDimen, value):
        self.interfaceDimen = interfaceDimen
        self.value = value

    def execute(self, ts, consola, exception, gen):
        result = self.value.execute(ts, consola, exception, gen)
        deep = len(self.interfaceDimen)

        id = self.interfaceDimen[0].value
        dicInterface = ts.find(id, exception)

        if dicInterface == None:
            exception.append("Error, interface no encontrada")
            return None

        if dicInterface.typeOf != "dict":
            exception.append("Error, variable no es una interface")
            return None

        self.updateValue(dicInterface.value, deep, result.value, exception)

        return None

    def updateValue(self, dic, deep, value, exception):
        for i in range(1, deep):
            id = self.interfaceDimen[i].value
            if i == deep - 1:
                dic[id] = value
                break
            else:
                dic = dic[id]
                if dic == None:
                    exception.append("Error, variable no encontrada")
                    return None


class InterfaceAccess(Instruccion):
    """Clase abs de acceso a interfaces"""

    def __init__(self, interfaceDimen):
        self.interfaceDimen = interfaceDimen

    def execute(self, ts, consola, exception, gen):
        deep = len(self.interfaceDimen)
        id = self.interfaceDimen[0].value
        dicInterface = ts.find(id, exception)

        if dicInterface == None:
            exception.append("Error, interface no encontrada")
            return None

        result = self.getValue(dicInterface.value, deep, exception)

        return Factor(self.validateType(result), result)

    def validateType(self, value):
        if isinstance(value, dict):
            return "STRING"

        if isinstance(value, int):
            return "NUMBER"

        if isinstance(value, float):
            return "FLOAT"

        if isinstance(value, bool):
            return "BOOLEAN"

        if isinstance(value, str):
            return "STRING"

        if isinstance(value, list):
            return "STRING"

    def getValue(self, dic, deep, exception):
        for i in range(1, deep):
            id = self.interfaceDimen[i].value

            if i == deep - 1:
                return dic[id]
            else:
                dic = dic[id]
                if dic == None:
                    exception.append("Error, variable no encontrada")
                    return None


class InterfaceUtils(Instruccion):
    """Clase abs de utilidades de interfaces"""

    def __init__(self, type, exp, exp2=None):
        self.type = type
        self.exp = exp
        self.exp2 = exp2

    def execute(self, ts, consola, exception, gen):
        if self.type == "length":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para length")
                return None

            return Factor("NUMBER", len(result.value))

        if self.type == "keys":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para keys")
                return None

            return Factor("STRING", list(result.value.keys()), "matrix")

        if self.type == "values":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para values")
                return None

            return Factor("STRING", list(result.value.values()), "matrix")

        if self.type == "haskey":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para haskey")
                return None

            result2 = self.exp2.execute(ts, consola, exception, gen)
            if result2.type != "STRING":
                exception.append("Error, tipo de dato no valido para haskey")
                return None

            return Factor("BOOLEAN", result2.value in result.value)

        if self.type == "removekey":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para removekey")
                return None

            result2 = self.exp2.execute(ts, consola, exception, gen)
            if result2.type != "STRING":
                exception.append("Error, tipo de dato no valido para removekey")
                return None

            result.value.pop(result2.value, None)
            return None

        if self.type == "clear":
            result = self.exp.execute(ts, consola, exception, gen)
            if result.typeOf != "dict":
                exception.append("Error, tipo de dato no valido para clear")
