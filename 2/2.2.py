# "With terminology out of the way, we're ready to proceed.
# To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."
# The inputs should still be provided to the program by replacing the values at addresses 1 and 2,
# just like before. In this program, the value placed in address 1 is called the noun,
# and the value placed in address 2 is called the verb.
# Each of the two input values will be between 0 and 99, inclusive.
# Once the program has halted, its output is available at address 0, also just like before.
# Each time you try a pair of inputs,
# make sure you first reset the computer's memory to the values in the program (your puzzle input)
# - in other words, don't reuse memory from a previous attempt.
# Find the input noun and verb that cause the program to produce the output 19690720.
# What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)

from enum import Enum
import csv
import itertools


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99


def process(code_list):
    res = code_list[:]
    ptr = 0
    while ptr != len(res):
        code = res[ptr]

        if code == OpCode.HALT.value:
            return res

        a = res[res[ptr + 1]]
        b = res[res[ptr + 2]]

        if code == OpCode.ADD.value:
            res[res[ptr + 3]] = a + b
        elif code == OpCode.MULTIPLY.value:
            res[res[ptr + 3]] = a * b

        ptr += 4
    return res


def find_noun_verb(codes, target):
    t1 = (i for i in range(99))
    t2 = (i for i in range(99))
    nvs = list(itertools.product(t1, t2))

    # for nv in nvs:
    #     res = codes[:]
    #     res[1] = nv[0]
    #     res[2] = nv[1]
    #
    #     output = process(res)[0]
    #
    #     if output == target:
    #         return nv

    # binary search
    l = 0
    r = len(nvs)
    while l <= r:
        res = codes[:]
        mid = int(l + (r - l) / 2)
        res[1] = nvs[mid][0]
        res[2] = nvs[mid][1]

        output = process(res)[0]

        if output == target:
            return nvs[mid]

        elif output < target:
            l = mid + 1

        else:
            r = mid - 1

    return None


codes = []
for line in csv.reader(open('../data/2.txt'), delimiter=','):
    codes = [int(i) for i in line]

print(find_noun_verb(codes, 19690720))
