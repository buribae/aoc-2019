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


def run(data):
    intcode = IntCode(data)
    panels = defaultdict(int)  # key: (x, y), value: 0 to 4

    while not intcode.is_done:
        x = intcode.process()
        y = intcode.process()
        z = intcode.process()

        panels[(x, y)] = z

    return panels


def count_tiles(tiles, tile_type):
    return len([1 for x in tiles.values() if x == tile_type])


codes = []
for line in csv.reader(open('../data/13.txt'), delimiter=','):
    codes = [int(i) for i in line]

tiles = run(codes)
print(count_tiles(tiles, BLOCK))
