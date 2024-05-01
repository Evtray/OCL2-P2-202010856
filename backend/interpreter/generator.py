from instructions import Factor
from value import Value


class Generator:
    def __init__(self):
        self.Temporal = 0
        self.Label = 0
        self.Code = []
        self.Data = []
        self.FinalCode = []
        self.Natives = []
        self.FuncCode = []
        self.TempList = []
        self.PrintStringFlag = True
        self.ConcatStringFlag = True
        self.BreakLabel = ""
        self.BreakLabels = []
        self.ContinueLabels = []
        self.ContinueLabel = ""
        self.MainCode = False
        self.actualExit = ""

    def get_code(self):
        return self.Code

    def get_final_code(self):
        self.add_headers()
        self.add_footers()
        outstring = "".join(self.Code)
        return outstring

    def get_temps(self):
        return self.TempList

    def add_break(self, lvl):
        self.BreakLabel = lvl

    def add_code(self, code):
        self.Code.append(code)

    def add_data_code(self, code):
        self.Data.append(code)

    def add_continue(self, lvl):
        self.ContinueLabel = lvl

    def new_temp(self):
        self.Temporal += 4
        return self.Temporal

    def new_label(self):
        temp = self.Label
        self.Label += 1
        return "L" + str(temp)

    def add_br(self):
        self.Code.append("\n")

    def comment(self, txt):
        self.Code.append(f"### {txt} \n")

    def variable_data(self, name, type, value):
        self.Data.append(f"{name}: .{type} {value} \n")

    def add_li(self, left, right):
        self.Code.append(f"\tli {left}, {right}\n")

    def add_la(self, left, right):
        self.Code.append(f"\tla {left}, {right}\n")

    def add_lw(self, left, right):
        self.Code.append(f"\tlw {left}, {right}\n")

    def add_sw(self, left, right):
        self.Code.append(f"\tsw {left}, {right}\n")

    def add_slli(self, target, left, right):
        self.Code.append(f"\tslli {target}, {left}, {right}\n")

    def add_blt(self, left, right, target):
        self.Code.append(f"\tblt {left}, {right}, {target}\n")

    def add_bgt(self, left, right, target):
        self.Code.append(f"\tbgt {left}, {right}, {target}\n")

    def add_bge(self, left, right, target):
        self.Code.append(f"\tbge {left}, {right}, {target}\n")

    def add_ble(self, left, right, target):
        self.Code.append(f"\tble {left}, {right}, {target}\n")

    def add_beq(self, left, right, target):
        self.Code.append(f"\tbeq {left}, {right}, {target}\n")

    def add_bne(self, left, right, target):
        self.Code.append(f"\tbne {left}, {right}, {target}\n")

    def add_jump(self, lvl):
        self.Code.append(f"\tj {lvl}\n")

    def new_body_label(self, lvl):
        self.Code.append(f"\t{lvl}:\n")

    def add_move(self, left, right):
        self.Code.append(f"\tmv {left}, {right}\n")

    def add_operation(self, operation, target, left, right):
        self.Code.append(f"\t{operation} {target}, {left}, {right}\n")

    def add_system_call(self):
        self.Code.append("\tecall\n")

    def add_headers(self):
        self.Code.insert(0, "\n.text\n.globl _start\n\n_start:\n")
        self.Data.insert(0, ".data\n")
        self.variable_data("str_true", "string", '"true"')
        self.variable_data("str_false", "string", '"false"')
        self.Code[:0] = self.Data

    def add_footers(self):
        self.Code.append("\n\tli a0, 0\n")
        self.Code.append("\tli a7, 93\n")
        self.Code.append("\tecall\n")

    def add_operation_values_simple(self, op1, op2):
        self.add_li("t1", str(op1))
        self.add_li("t2", str(op2))

    def add_breaks(self, label):
        self.BreakLabels.append(label)

    def add_operation_values(self, op1, op2):
        temp1 = 0
        isTemp1 = False
        temp2 = 0
        isTemp2 = False
        if isinstance(op1, int):
            temp1 = op1
            isTemp1 = True
        elif isinstance(op1, Factor):
            if isinstance(op1.position.value, Value):
                op1.position = op1.position.value
            isTemp1 = op1.position.isTemp
            if isTemp1:
                temp1 = op1.position.value
            else:
                temp1 = op1.value
        else:
            temp1 = op1.position.value
            isTemp1 = op1.position.isTemp

        if isinstance(op2, int):
            temp2 = op2
            isTemp2 = True
        elif isinstance(op2, Factor):

            if isinstance(op2.position.value, Value):
                op2.position = op2.position.value
                
            isTemp2 = op2.position.isTemp

            if isTemp2:
                temp2 = op2.position.value
            else:
                temp2 = op2.value
        else:
            temp2 = op2.position.value
            isTemp2 = op2.position.isTemp
        print(temp1, temp2, isTemp1, isTemp2)

        self.comment("Realizando operacion")

        if isTemp1:
            self.add_li("t0", temp1)
            self.add_lw("t1", "0(t0)")
        else:
            self.add_li("t1", str(temp1))

        if isTemp2:
            self.add_li("t3", temp2)
            self.add_lw("t2", "0(t3)")
        else:
            self.add_li("t2", str(temp2))

    def add_operation_arit(self, operation):
        temp = self.new_temp()
        self.add_li("t0", "0")
        self.add_operation(operation, "t0", "t1", "t2")
        self.add_li("t3", str(temp))
        self.add_sw("t0", "0(t3)")

        return str(temp)
