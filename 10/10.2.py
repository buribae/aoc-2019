import math
from collections import defaultdict

def build_asteroids(data):
    asteroids = []
    for y, row in enumerate(data.split()):
        for x, point in enumerate(row):
            if point == '#':
                asteroids.append((x, y))
    return asteroids


def detect(asteroids, origin_x, origin_y):
    slopes = set()
    detected = []
    for asteroid in asteroids:
        x = asteroid[0]
        y = asteroid[1]

        if x == origin_x and y == origin_y:
            continue

        slope = math.atan2(asteroid[1] - origin_y, asteroid[0] - origin_x)

        if slope not in slopes:
            slopes.add(slope)
            detected.append(asteroid)
    return detected


def destroy(asteroids, origin_x, origin_y):
    destroyed = []
    detected = detect(asteroids, origin_x, origin_y)
    asteroid_map = defaultdict(list)
    for asteroid in detected:
        x = asteroid[0]
        y = asteroid[1]

        if x == origin_x and y == origin_y:
            continue

        slope = math.atan2(y - origin_y, x - origin_x)
        slope = slope if slope >= -.5 * math.pi else slope + (2 * math.pi)
        dist = abs(y - origin_y) + abs(x - origin_x)

        asteroid_map[slope].append((dist, (x, y)))

    for k, v in sorted(asteroid_map.items()):
        destroyed.extend(sorted(v, key=lambda item: item[0]))
        print(destroyed)

    new_map = set(asteroids) ^ set(destroyed)

    return new_map, destroyed


# 3,4 / 8
t = """.#..#
.....
#####
....#
...##"""

# 5,8 / 33
test = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

# 1,2 / 35
test2 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

# 6,3 / 41
test3 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

# 11,13 / 210
test4 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

map = open('../data/10.txt').read()

asteroids = build_asteroids(map)

max = 0
best = None
for asteroid in asteroids:
    num_detect = len(detect(asteroids, asteroid[0], asteroid[1]))
    if num_detect > max:
        max = num_detect
        best = asteroid

destroyed = []
ast_map = asteroids

while len(destroyed) < 200:
    ast_map, dest = destroy(ast_map, best[0], best[1])
    destroyed.extend(dest)
    print(ast_map)

print(destroyed[199])