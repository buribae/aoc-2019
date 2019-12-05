# --- Part Two ---
# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.
#
# Given this additional criterion, but still ignoring the range rule, the following are now true:
#
# 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
# 123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
# 111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
# How many different passwords within the range given in your puzzle input meet all of the criteria?


def is_six_digit(pw):
    return True if (len(str(pw)) == 6) else False


def is_in_range(pw, range_min, range_max):
    return True if (range_min <= pw <= range_max) else False


def is_adj_exist(pw):
    spw = str(pw)
    found = False
    for idx, n in enumerate(spw[1:]):
        if spw[idx] == n:
            found = True

    return found


# with new rule, when we find adj twice, return false
def is_adj_not_in_group(pw):
    spw = str(pw)
    found = False
    for idx, n in enumerate(spw[1:]):
        if spw[idx] == n:
            if idx == 0 and spw[idx+1] != n:
                found = True
            elif idx == len(spw)-2 and spw[idx-1] != n:
                found = True
            else:
                if spw[idx-1] != n and spw[idx+2] != n:
                    found = True
    return found


def is_not_decreasing(pw):
    spw = str(pw)
    for idx, n in enumerate(spw[1:]):
        if spw[idx] > n:
            return False
    return True


def check_pw(pw, range_min, range_max):
    if all([is_six_digit(pw), is_in_range(pw, range_min, range_max), is_adj_exist(pw), is_adj_not_in_group(pw), is_not_decreasing(pw)]):
        return True
    else:
        return False


def generate_pw(range_min, range_max):
    count = 0
    for n in range(range_min, range_max+1):
        if check_pw(n, range_min, range_max):
            count += 1

    return count

# TESTS
# 112233 T, 123444 F, 111122 T
n = 111122
print(n)
print("is_six_digit:", is_six_digit(n))
print("is_in_range:", is_in_range(n, n, n+5))
print("is_adj_exist:", is_adj_exist(n))
print("is_adj_not_in_group:", is_adj_not_in_group(n))
print("is_not_decreasing:", is_not_decreasing(n))
#
# # # test check_pw
# test1 = check_pw(111111, 111111, 111115)
# test2 = check_pw(223450, 223450, 223455)
# test3 = check_pw(123789, 123789, 123799)
#
# print(test1)
# print(test2)
# print(test3)

res = generate_pw(193651, 649729)
print(res)
