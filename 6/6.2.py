def generate_orbits(data):
    return {o2: o1 for (o1, o2) in [orbit.split(')') for orbit in data]}


def get_path(orbit_map, target):
    path = []
    obj = target
    while obj != 'COM':
        path.append(obj)
        obj = orbit_map[obj]

    return path


def get_all_paths(orbit_map):
    path = []
    for k, v in orbit_map.items():
        path.extend(get_path(orbit_map, k))

    return path


with open('../data/6.txt') as f:
    orbits = generate_orbits(f.read().splitlines())
    y = set(get_path(orbits, 'YOU'))
    s = set(get_path(orbits, 'SAN'))
    shortest = y ^ s
    print(len(shortest) - 2)
