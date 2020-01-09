from enum import Enum
import csv
import itertools
import logging
logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    GET = 4
    JIT = 5  # JUMP IF TRUE
    JIF = 6  # JUMP IF FALSE
    LESS = 7
    EQUAL = 8
    RELATIVE = 9
    HALT = 99


class IntCode:
    output = None
    is_done = False
    rel_base = 0
    modes = [0, 0, 0]  # CBA as a list, reversed, reading it from right to left

    def __init__(self, code_list, input_number=None, ptr=0, phase=None, memsize=10000):
        self.codes = code_list[:]
        self.phase = int(phase) if phase else None
        self.input = input_number
        self.ptr = ptr

        if len(self.codes) < memsize:
            for _ in range(memsize - len(self.codes)):
                self.codes.append(0)

    def generate_output(self):
        return self.output

    def get_parameter_mode(self, param_code):
        self.modes = [0, 0, 0]
        if len(param_code) > 1:
            p_code = param_code[:-2]
            for idx, i in enumerate(p_code[::-1]):
                self.modes[idx] = int(i)

    def get_param_value(self, mode, address):
        if mode == 0:
            return self.codes[address]
        elif mode == 1:
            return address
        elif mode == 2:
            logging.debug("base: %d", self.rel_base)
            return self.codes[self.rel_base + address]

    def get_write_position(self, mode, address):
        if mode == 0:
            return address
        elif mode == 1:
            return None
        elif mode == 2:
            return self.rel_base + address

    @property
    def p1(self):
        return self.get_param_value(self.modes[0], self.codes[self.ptr + 1])

    @property
    def p2(self):
        return self.get_param_value(self.modes[1], self.codes[self.ptr + 2])

    @property
    def p3(self):
        return self.get_write_position(self.modes[2], self.codes[self.ptr + 3])

    def process(self, input_number=None):
        self.input = input_number
        logging.debug("codes: %s", self.codes)
        while True:
            logging.debug("%s --------------", self.ptr)
            self.get_parameter_mode(str(self.codes[self.ptr]))
            code = int(str(self.codes[self.ptr])[-1])
            logging.debug("code: %s", int(str(self.codes[self.ptr])))

            if int(str(self.codes[self.ptr])[-2:]) == OpCode.HALT.value:
                self.is_done = True
                return self.generate_output()

            elif code == OpCode.ADD.value:
                logging.debug("ADD | target: %d, address: %d, p1: %d, p2: %d", self.codes[self.p3],
                              self.p3, self.p1, self.p2)
                self.codes[self.p3] = self.p1 + self.p2
                self.ptr += 4

            elif code == OpCode.MULTIPLY.value:
                self.codes[self.p3] = self.p1 * self.p2
                logging.debug("MULT | target: %d, address: %d, p1: %d, p2: %d", self.codes[self.p3],
                              self.p3, self.p1, self.p2)
                self.ptr += 4

            elif code == OpCode.SAVE.value:
                pos = self.get_write_position(self.modes[0], self.codes[self.ptr + 1])
                self.codes[pos] = self.phase if self.phase else self.input
                self.ptr += 2
                logging.debug("SAVE | address: %d, pos: %d, input: %d", self.codes[self.ptr + 1], pos, self.input)

            elif code == OpCode.GET.value:
                self.output = self.p1
                self.ptr += 2
                #print(self.generate_output())
                logging.debug("GET | output: %d", self.output)

            elif code == OpCode.JIT.value:
                if self.p1 != 0:
                    self.ptr = self.p2
                else:
                    logging.debug("JIT ptr+3 | p1: %d", self.p1)
                    self.ptr += 3

            elif code == OpCode.JIF.value:
                if self.p1 == 0:
                    self.ptr = self.p2
                    logging.debug("JIF | p1: %d", self.p1)
                else:
                    logging.debug("JIF ptr+3 | p1: %d", self.p1)
                    self.ptr += 3

            elif code == OpCode.LESS.value:
                logging.debug("LESS | p1: %d, p2: %d", self.p1, self.p2)
                if self.p1 < self.p2:
                    self.codes[self.p3] = 1
                else:
                    self.codes[self.p3] = 0
                logging.debug("LESS | address: %d, target: %d", self.p3, self.codes[self.p3])

                self.ptr += 4

            elif code == OpCode.EQUAL.value:
                logging.debug("EQUAL | target: %d, p1: %d, p2: %d", self.codes[self.p3], self.p1, self.p2)
                if self.p1 == self.p2:
                    self.codes[self.p3] = 1
                else:
                    self.codes[self.p3] = 0
                logging.debug("EQUAL | target: %d, p1: %d, p2: %d", self.codes[self.p3], self.p1, self.p2)

                self.ptr += 4

            elif code == OpCode.RELATIVE.value:
                logging.debug("RELATIVE | base: %d, p1: %d", self.rel_base, self.p1)
                self.rel_base += self.p1
                logging.debug("CHANGED | base: %d", self.rel_base)

                self.ptr += 2

            logging.debug("\n")


codes = []
for line in csv.reader(open('../data/9.txt'), delimiter=','):
    codes = [int(i) for i in line]

test = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]  # Quine
test2 = [1102,34915192,34915192,7,4,7,99,0]  # 16 digit #
test3 = [104,1125899906842624,99]  # large # in the middle
test4 = [109, 1, 9, 2, 204, -6, 99]  # 204

int_code = IntCode(codes)
int_code.process(2)
print(int_code.output)
