from core.intcode import IntCode
import csv
from collections import defaultdict


# emergency hull painting robot
# -----------
# input = 0: black panel, 1: white panel
# output = (paint, turn)
# -----------
# paint | 0: black, 1: white
# turn | 0: turn left 90 deg, 1: turn right 90 deg
#
# after turn, move robot forward one panel
# robot starts facing up
def paint(data):
    intcode = IntCode(data)
    panels = defaultdict(int)  # key: (x, y), value: 0 or 1
    x, y = 0, 0
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
    facing = 0

    while not intcode.is_done:
        panels[(x, y)] = intcode.process(panels[(x, y)])  # first output = color to paint panel
        turn = intcode.process(panels[(x, y)])  # second output = turn direction

        facing = (facing + 1) % 4 if turn else (facing - 1) % 4

        # Move
        x += directions[facing][0]
        y += directions[facing][1]

    return panels


codes = []
for line in csv.reader(open('../data/11.txt'), delimiter=','):
    codes = [int(i) for i in line]


print(len(paint(codes)))
