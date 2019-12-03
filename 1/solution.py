#
# PART 1
# ---------
# Fuel required to launch a given module is based on its mass. Specifically,
# to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

#
# For example:
#
# For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
# For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
# For a mass of 1969, the fuel required is 654.
# For a mass of 100756, the fuel required is 33583.

import math

with open('../data/1.txt') as f:
    print(sum([math.floor(int(mass) / 3) - 2 for mass in f]))

