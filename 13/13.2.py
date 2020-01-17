from core.intcode import IntCode
import csv
from collections import defaultdict


# care package
# -----------
# 0 is an empty tile. No game object appears in this tile.
# 1 is a wall tile. Walls are indestructible barriers.
# 2 is a block tile. Blocks can be broken by the ball.
# 3 is a horizontal paddle tile. The paddle is indestructible.
# 4 is a ball tile. The ball moves diagonally and bounces off objects.
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


# If the joystick is in the neutral position, provide 0.
# If the joystick is tilted to the left, provide -1.
# If the joystick is tilted to the right, provide 1.
def play(data):
    intcode = IntCode(data)
    panels = defaultdict(int)  # key: (x, y), value: 0 to 4
    score = 0
    ball_x = 0
    paddle_x = 0
    joystick = 0

    while not intcode.is_done:
        x = intcode.process(joystick)
        y = intcode.process(joystick)
        z = intcode.process(joystick)

        # record the score, paddle_x, ball_x
        if x == -1 and y == 0:
            score = z
        elif z == 3:
            paddle_x = x
        elif z == 4:
            ball_x = x

        # automate moving joystick
        if ball_x < paddle_x:
            joystick = -1
        elif ball_x > paddle_x:
            joystick = 1
        else:
            joystick = 0

        # render
        panels[(x, y)] = z

    return score


codes = []
for line in csv.reader(open('../data/13.txt'), delimiter=','):
    codes = [int(i) for i in line]

codes[0] = 2  # free play
score = play(codes)

print(score)
