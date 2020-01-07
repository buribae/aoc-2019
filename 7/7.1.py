from enum import Enum
import csv
import itertools


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    GET = 4
    JIT = 5  # JUMP IF TRUE
    JIF = 6  # JUMP IF FALSE
    LESS = 7
    EQUAL = 8
    HALT = 99


def get_parameter_mode(param_code):
    modes = [0, 0, 0]  # CBA
    if len(param_code) > 1:
        p_code = param_code[:-2]
        for idx, i in enumerate(p_code[::-1]):
            modes[idx] = int(i)

    return modes  # as a list, reversed, reading it from right to left


def process(code_list, phase, input_number):
    res = code_list[:]
    ptr = 0
    output = None
    is_phased = False
    while True:
        #print("--------------")
        #print(ptr)
        modes = get_parameter_mode(str(res[ptr]))
        code = int(str(res[ptr])[-1])
        #print("Code, Mode:", code, modes)
        #print("CODE:", res[ptr])
        #print("P1:", res[ptr + 1])
        #print("P2:", res[ptr + 2])
        #print("P3:", res[ptr + 3])

        if int(str(res[ptr])[-2:]) == OpCode.HALT.value:
            return output

        elif code == OpCode.ADD.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]
            #print("AP1:", p1)
            #print("AP2:", p2)

            res[res[ptr + 3]] = p1 + p2
            #print("A_target:", res[ptr + 3], res[res[ptr + 3]])
            ptr += 4

        elif code == OpCode.MULTIPLY.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]
            #print("MP1:", p1)
            #print("MP2:", p2)

            res[res[ptr + 3]] = p1 * p2
            #print("M_target:", res[ptr + 3], res[res[ptr + 3]])
            ptr += 4

        elif code == OpCode.SAVE.value:
            res[res[ptr + 1]] = input_number if is_phased else phase
            if not is_phased:
                is_phased = True
            #print("Save_target:", res[ptr + 1], res[res[ptr + 1]], input_number)
            ptr += 2

        elif code == OpCode.GET.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            output = p1
            ptr += 2

        elif code == OpCode.JIT.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]

            if p1 != 0:
                ptr = p2
            else:
                ptr += 3

        elif code == OpCode.JIF.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]

            if p1 == 0:
                ptr = p2
            else:
                ptr += 3

        elif code == OpCode.LESS.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]

            if p1 < p2:
                res[res[ptr + 3]] = 1
            else:
                res[res[ptr + 3]] = 0

            ptr += 4

        elif code == OpCode.EQUAL.value:
            p1 = res[ptr + 1] if modes[0] else res[res[ptr + 1]]
            p2 = res[ptr + 2] if modes[1] else res[res[ptr + 2]]

            if p1 == p2:
                res[res[ptr + 3]] = 1
            else:
                res[res[ptr + 3]] = 0

            ptr += 4


def run_amplifiers(code_list, phase_list, initial_input):
    cur_list = code_list[:]
    output = initial_input
    for phase in phase_list:
        output = process(cur_list, int(phase), output)
    return output


codes = []
for line in csv.reader(open('../data/7.txt'), delimiter=','):
    codes = [int(i) for i in line]


test = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
test2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0]
test3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

outputs = set()
for phases in map("".join, itertools.permutations('01234')):
    outputs.add(run_amplifiers(codes, phases, 0))

print(max(outputs))
