# 1,9,10,3,
# 2,3,11,0,
# 99,
# 30,40,50
# op code 1 = adds res[1] + res[2] and store to res[res[3]]
# op code 2 = same as op code 1 but multiplies
# op code 99 = halt

from enum import Enum


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


# test = [1,9,10,3,2,3,11,0,99,30,40,50]
# test2 = [1,0,0,0,99]
# test3 = [2,3,0,3,99]
# test4 = [2,4,4,5,99,0]
# test5 = [1,1,1,4,99,5,6,0,99]
#
# print(process(test))
# print(process(test2))
# print(process(test3))
# print(process(test4))
# print(process(test5))

import csv

for line in csv.reader(open('../data/2.txt'), delimiter=','):
    codes = [int(i) for i in line]

print(codes)
print(process(codes))

# original 337042
# changed 3101844