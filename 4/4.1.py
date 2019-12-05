# --- Day 4: Secure Container ---
# You arrive at the Venus fuel depot only to discover it's protected by a password.
# The Elves had written the password on a sticky note, but someone threw it out.
#
# However, they do remember a few key facts about the password:
#
# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
# Other than the range rule, the following are true:
#
# 111111 meets these criteria (double 11, never decreases).
# 223450 does not meet these criteria (decreasing pair of digits 50).
# 123789 does not meet these criteria (no double).
# How many different passwords within the range given in your puzzle input meet these criteria?
#
# Your puzzle input is 193651-649729.


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


def is_not_decreasing(pw):
    spw = str(pw)
    for idx, n in enumerate(spw[1:]):
        if spw[idx] > n:
            return False
    return True


def check_pw(pw, range_min, range_max):
    if all([is_six_digit(pw), is_in_range(pw, range_min, range_max), is_adj_exist(pw), is_not_decreasing(pw)]):
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

# n = 223450
# print(n)
# print("is_six_digit:", is_six_digit(n))
# print("is_in_range:", is_in_range(n, n, n+5))
# print("is_adj_exist:", is_adj_exist(n))
# print("is_not_decreasing:", is_not_decreasing(n))
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
