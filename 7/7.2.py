from enum import Enum
import csv
import itertools
import logging
logging.basicConfig(level=logging.DEBUG)


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


class IntCode:
    output = None
    is_phased = False
    is_done = False

    def __init__(self, code_list, phase, input_number, ptr=0):
        self.codes = code_list[:]
        self.phase = int(phase)
        self.input = input_number
        self.ptr = ptr

    def generate_output(self):
        return self.output

    def get_parameter_mode(self, param_code):
        modes = [0, 0, 0]  # CBA
        if len(param_code) > 1:
            p_code = param_code[:-2]
            for idx, i in enumerate(p_code[::-1]):
                modes[idx] = int(i)

        return modes  # as a list, reversed, reading it from right to left

    def get_params(self, modes):
        p1 = self.codes[self.ptr + 1] if modes[0] else self.codes[self.codes[self.ptr + 1]]
        p2 = self.codes[self.ptr + 2] if modes[1] else self.codes[self.codes[self.ptr + 2]]
        return p1, p2

    def process(self, input_number):
        self.input = input_number
        while True:
            logging.debug("--------------")
            modes = self.get_parameter_mode(str(self.codes[self.ptr]))
            code = int(str(self.codes[self.ptr])[-1])
            #print("Code, Mode:", code, modes)
            #print("CODE:", res[ptr])
            #print("P1:", res[ptr + 1])
            #print("P2:", res[ptr + 2])
            #print("P3:", res[ptr + 3])

            if int(str(self.codes[self.ptr])[-2:]) == OpCode.HALT.value:
                self.is_done = True
                return self.generate_output()

            elif code == OpCode.ADD.value:
                p1, p2 = self.get_params(modes)
                #print("AP1:", p1)
                #print("AP2:", p2)

                self.codes[self.codes[self.ptr + 3]] = p1 + p2
                #print("A_target:", res[ptr + 3], res[res[ptr + 3]])
                self.ptr += 4

            elif code == OpCode.MULTIPLY.value:
                p1, p2 = self.get_params(modes)
                #print("MP1:", p1)
                #print("MP2:", p2)

                self.codes[self.codes[self.ptr + 3]] = p1 * p2
                #print("M_target:", res[ptr + 3], res[res[ptr + 3]])
                self.ptr += 4

            elif code == OpCode.SAVE.value:
                self.codes[self.codes[self.ptr + 1]] = self.input if self.is_phased else self.phase
                if not self.is_phased:
                    self.is_phased = True
                #print("Save_target:", res[ptr + 1], res[res[ptr + 1]], input_number)
                self.ptr += 2

            elif code == OpCode.GET.value:
                p1 = self.codes[self.ptr + 1] if modes[0] else self.codes[self.codes[self.ptr + 1]]
                self.output = p1
                self.ptr += 2
                return self.generate_output()

            elif code == OpCode.JIT.value:
                p1, p2 = self.get_params(modes)

                if p1 != 0:
                    self.ptr = p2
                else:
                    self.ptr += 3

            elif code == OpCode.JIF.value:
                p1, p2 = self.get_params(modes)

                if p1 == 0:
                    self.ptr = p2
                else:
                    self.ptr += 3

            elif code == OpCode.LESS.value:
                p1, p2 = self.get_params(modes)

                if p1 < p2:
                    self.codes[self.codes[self.ptr + 3]] = 1
                else:
                    self.codes[self.codes[self.ptr + 3]] = 0

                self.ptr += 4

            elif code == OpCode.EQUAL.value:
                p1, p2 = self.get_params(modes)

                if p1 == p2:
                    self.codes[self.codes[self.ptr + 3]] = 1
                else:
                    self.codes[self.codes[self.ptr + 3]] = 0

                self.ptr += 4


def run_amplifiers(code_list, phase_list, initial_input):
    int_codes = [IntCode(code_list, phase, initial_input) for phase in phase_list]
    output = initial_input
    while not int_codes[-1].is_done:
        for int_code in int_codes:
            output = int_code.process(output)

    return output


codes = []
for line in csv.reader(open('../data/7.txt'), delimiter=','):
    codes = [int(i) for i in line]


test = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
test2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

outputs = set()
for phases in map("".join, itertools.permutations('56789')):
    outputs.add(run_amplifiers(codes, phases, 0))

print(max(outputs))
