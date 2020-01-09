import math


def build_asteroids(data):
    asteroids = []
    for y, row in enumerate(data.split()):
        for x, point in enumerate(row):
            if point == '#':
                asteroids.append((x, y))
    return asteroids


def detect(asteroids, asteroid_num):
    slopes = set()
    detected = []
    origin_x, origin_y = asteroids[asteroid_num][0], asteroids[asteroid_num][1]
    ordered_asteroids = asteroids[asteroid_num+1:] + asteroids[:asteroid_num]  # ordered clockwise
    for asteroid in ordered_asteroids:
        slope = math.atan2(asteroid[1] - origin_y, asteroid[0] - origin_x)

        if slope not in slopes:
            slopes.add(slope)
            detected.append(asteroid)
    return detected

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
for i, a in enumerate(asteroids):
    sights = len(detect(asteroids, i))
    if sights > max:
        max = sights
        best = a

print(max, best)