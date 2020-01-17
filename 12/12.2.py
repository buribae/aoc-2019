# Jupiter's moons (Io, Europa, Ganymede, Callisto)
from math import gcd


def lcm(a, b):
    return a*b//gcd(a, b)


class Moon:
    x: int
    y: int
    z: int
    dx: int = 0
    dy: int = 0
    dz: int = 0
    # potential_energy: int = 0
    # kinetic_energy: int = 0
    # total_energy: int = 0

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return 'x,y,z | {0}, {1}, {2} | dx, dy, dz | {3}, {4}, {5}'\
            .format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def position(self, axis):
        if axis == 0:
            return self.x
        elif axis == 1:
            return self.y
        elif axis == 2:
            return self.z

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def is_moving(self, axis):
        if axis == 0:
            return False if self.dx == 0 else True
        elif axis == 1:
            return False if self.dy == 0 else True
        elif axis == 2:
            return False if self.dz == 0 else True


def parse(f):
    moons = []
    for line in open(f):
        x, y, z = [int(x[2:]) for x in line.strip('<>\n').split(', ')]
        moons.append(Moon(x, y, z))
    return moons


def get_gravity(pos1, pos2):
    if pos1 < pos2:
        return 1
    elif pos1 > pos2:
        return -1
    else:
        return 0


def apply_gravity(moons):
    for i, m in enumerate(moons):
        other_moons = moons[:i] + moons[i+1:]
        for om in other_moons:
            m.dx += get_gravity(m.x, om.x)
            m.dy += get_gravity(m.y, om.y)
            m.dz += get_gravity(m.z, om.z)


def apply_velocity(moons):
    for m in moons:
        m.move()


def equal(m1, m2):
    return True if m1.x == m2.x and m1.y == m2.y and m1.z == m2.z else False


def equals(ms1, ms2):
    for i, m in enumerate(ms1):
        if not equal(m, ms2[i]):
            return False
    return True


def not_moving(moons, axis):
    for moon in moons:
        if moon.is_moving(axis):
            return False
    return True


def check(moons, axis, initial_moons):
    for n, moon in enumerate(moons):
        if moon.position(axis) != initial_moons[n].position(axis):
            return False
    return True


def print_moons(moons):
    for moon in moons:
        print(moon)


steps = [0, 0, 0]
step = 0

for i in range(3):
    moons = parse('../data/12.txt')
    initial_moons = parse('../data/12.txt')
    while True:
        apply_gravity(moons)
        apply_velocity(moons)

        step += 1

        if steps[i] == 0 and check(moons, i, initial_moons) and not_moving(moons, i):
            steps[i] = step
            step = 0
            break

print(steps)
print(lcm(lcm(steps[0], steps[1]), steps[2]))

