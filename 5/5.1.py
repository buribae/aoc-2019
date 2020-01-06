# Opcode 3 takes a single integer as input and saves it to the position given by its only parameter.
# For example, the instruction 3,50 would take an input value and store it at address 50.
# Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.

# Second, you'll need to add support for parameter modes:
# Each parameter of an instruction is handled based on its parameter mode.
# Right now, your ship computer already understands parameter mode 0, position mode,
# which causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory.
# Until now, all parameters have been in position mode.
# Now, your ship computer will also need to handle parameters in mode 1, immediate mode.
# In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50.

from enum import Enum
import csv


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    GET = 4
    HALT = 99


def get_parameter_mode(param_code):
    modes = [0, 0, 0]  # CBA
    if len(param_code) > 1:
        p_code = param_code[:-2]
        for idx, i in enumerate(p_code[::-1]):
            modes[idx] = int(i)

    return modes  # as a list, reversed, reading it from right to left


def process(code_list, input):
    res = code_list[:]
    ptr = 0
    while ptr <= len(res):
        #print("--------------")
        #print(ptr)
        modes = get_parameter_mode(str(res[ptr]))
        code = int(str(res[ptr])[-1])
        #print("Code, Mode:", code, modes)
        #print("CODE:", res[ptr])
        #print("P1:", res[ptr + 1])
        #print("P2:", res[ptr + 2])
        #print("P3:", res[ptr + 3])

        increment = 4

        if int(str(res[ptr])[-2:]) == OpCode.HALT.value:
            return res

        elif code == OpCode.ADD.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]
            #print("AP1:", p1)
            #print("AP2:", p2)

            res[res[ptr + 3]] = p1 + p2
            #print("A_target:", res[ptr + 3], res[res[ptr + 3]])

        elif code == OpCode.MULTIPLY.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]
            #print("MP1:", p1)
            #print("MP2:", p2)

            res[res[ptr + 3]] = p1 * p2
            #print("M_target:", res[ptr + 3], res[res[ptr + 3]])

        elif code == OpCode.SAVE.value:
            res[res[ptr + 1]] = input
            #print("Save_target:", res[ptr + 1], res[res[ptr + 1]], input)
            increment = 2

        elif code == OpCode.GET.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            print(p1)
            increment = 2

        ptr += increment
    return res


codes = []
for line in csv.reader(open('../data/5.txt'), delimiter=','):
    codes = [int(i) for i in line]


test1 = [1002,4,3,4,33]
test2 = [1101,100,-1,4,0]

print(process(codes, 1))
