class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1  # point
        self.p2 = p2  # point


def build_lines(instruction):
    edges = [Point(0, 0)]
    lines = []

    for inst in instruction:
        last_x, last_y = edges[-1].x, edges[-1].y
        dir = inst[0]
        n = int(inst[1:])

        x, y = 0, 0

        if dir == 'R':
            x = n
        elif dir == 'L':
            x = -n
        elif dir == 'U':
            y = n
        elif dir == 'D':
            y = -n

        edges.append(Point(last_x + x, last_y + y))
        lines.append(Line(Point(last_x, last_y), Point(last_x + x, last_y + y)))

    return lines


def get_intersection(l1, l2):
    p1, p2, p3, p4 = l1.p1, l1.p2, l2.p1, l2.p2
    # check if x1, x2 are same
    # if x1 is within the range of x3, x4
    # if y3 is within the range of y1, y2, return (x1, y3) else no intersection
    if p1.x == p2.x and (p3.x < p1.x < p4.x or p4.x < p1.x < p3.x) and (p1.y < p3.y < p2.y or p2.y < p3.y < p1.y):
        return Point(p1.x, p3.y)

    # check if y1, y2 are same
    # check if y1 is within the range of y3, y4
    # if x3 is within the range of x1, x2, return (x3, y1) else no intersection
    if p1.y == p2.y and (p3.y < p1.y < p4.y or p4.y < p1.y < p3.y) and (p1.x < p3.x < p2.x or p2.x < p3.x < p1.x):
        return Point(p3.x, p1.y)

    return None


def min_dist_intersection(inst1, inst2):
    lines1, lines2 = build_lines(inst1), build_lines(inst2)

    min_dist = float('inf')
    for line1 in lines1:
        for line2 in lines2:
            inter_p = get_intersection(line1, line2)
            if inter_p:
                man_dist = abs(inter_p.x) + abs(inter_p.y)
                if man_dist < min_dist:
                    min_dist = man_dist

    return min_dist


# # Test (3,5), (3,2) vs (6,3), (2,3)
# # Assert (3, 3)
#
# pt1, pt2, pt3, pt4 = Point(3, 5), Point(3, 2), Point(6, 3), Point(2, 3)
# l1, l2 = Line(pt1, pt2), Line(pt3, pt4)
#
# print(get_intersection(l1, l2))
#
# # Test (3,5), (3,2) vs (6,3), (2,3)
# # Assert (6, 5)
#
# pt1, pt2, pt3, pt4 = Point(8, 5), Point(3, 5), Point(6, 7), Point(6, 3)
# l1, l2 = Line(pt1, pt2), Line(pt3, pt4)
#
# print(get_intersection(l1, l2))

testa = "R8,U5,L5,D3".split(',')
testb = "U7,R6,D4,L4".split(',')
print(min_dist_intersection(testa, testb))  # 6

test1a = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')
test1b = "U62,R66,U55,R34,D71,R55,D58,R83".split(',')

print(min_dist_intersection(test1a, test1b))  # 159

test2a = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(',')
test2b = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')

print(min_dist_intersection(test2a, test2b))  # 135


with open('../data/3.txt') as f:
    lines = f.readlines()
    print(min_dist_intersection(lines[0].split(','), lines[1].split(',')))

