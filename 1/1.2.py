#
# PART 2
# ---------
import math
from collections import defaultdict


def get_fuel(mass):
    return math.floor(mass / 3) - 2


with open('../data/1.txt') as f:
    fuel_dict = defaultdict(int)
    fuel_required = 0

    for idx, mass in enumerate(f):
        temp = int(mass)
        while get_fuel(temp) > 0:
            temp = get_fuel(temp)
            fuel_dict[idx] += temp
            fuel_required += temp

    print(fuel_required)
    print(fuel_dict)