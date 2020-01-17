# Jupiter's moons (Io, Europa, Ganymede, Callisto)


class Moon:
    x: int
    y: int
    z: int
    dx: int = 0
    dy: int = 0
    dz: int = 0
    potential_energy: int = 0
    kinetic_energy: int = 0
    total_energy: int = 0

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return 'x,y,z | {0}, {1}, {2} | dx, dy, dz | {3}, {4}, {5}'\
            .format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.calculate_energy()

    def calculate_energy(self):
        self.potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
        self.kinetic_energy = abs(self.dx) + abs(self.dy) + abs(self.dz)
        self.total_energy = self.potential_energy * self.kinetic_energy


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


moons = parse('../data/12.txt')

for _ in range(1000):
    apply_gravity(moons)
    apply_velocity(moons)

energy = 0
for moon in moons:
    energy += moon.total_energy

print(energy)
