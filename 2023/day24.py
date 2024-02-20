import re
from os import path
import math
from typing import NamedTuple

Point = NamedTuple('Point', x=int, y=int, z=int)
Hail = NamedTuple('Hail', point=Point, delta=Point, slope=float, intercept=float)

with open('inputs/input24.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [li.strip() for li in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day24:
    def __init__(self, lines):
        self.part = 0
        self.board = self.parse_inputs(lines)

    @staticmethod
    def parse_inputs(lines):
        board = []
        for li in lines:
            m = re.match(r'(\d+), +(\d+), +(\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)', li)
            start = Point(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            deltas = Point(int(m.group(4)), int(m.group(5)), int(m.group(6)))
            slope2d = deltas.y / deltas.x
            intercept2d = start.y - slope2d * start.x
            board.append(Hail(start, deltas, slope2d, intercept2d))
        return board

    def part1(self, lower_limit, upper_limit):
        self.part = 1
        intersections = 0
        for count, h1 in enumerate(self.board):
            for i2 in range(count+1, len(self.board)):
                h2 = self.board[i2]
                if h1.slope == h2.slope:
                    # print(f'Hail stones {count} and {i2} are parallel in x-y')
                    pass
                else:
                    # lines y = ax + c and y = bx + d intersect at int_x = (d - c) / (a - b), int_y = a * int_x + c
                    int_x = (h2.intercept - h1.intercept) / (h1.slope - h2.slope)
                    int_y = h1.slope * int_x + h1.intercept
                    t1 = (int_x - h1.point.x) / h1.delta.x
                    t2 = (int_x - h2.point.x) / h2.delta.x
                    if lower_limit < int_x < upper_limit and lower_limit < int_y < upper_limit and t1 > 0 and t2 > 0:
                        intersections += 1
        print(f'Total intersections in the future = {intersections}')

    def translate(self, v1: Hail, v0: Hail) -> Hail:
        return Hail(self.sub(v1.point, v0.point), self.sub(v1.delta, v0.delta), 0, 0)

    def plane_normal(self, hail: Hail) -> Point:
        """
        Returns the normal to the plane defined by the line traced by this hail stone and the origin
        :param hail: An individual hail stone
        :return: a Point containing a vector representing the plane normal
        """
        vector1 = hail.point  # Vector1 is the original point of the hailstone
        delta = hail.delta  # Vector2 is the hailstone one integral step forward in its path
        vector2 = Point(vector1.x + delta.x, vector1.y + delta.y, vector1.z + delta.z)
        return self.cross_product(vector1, vector2)

    @staticmethod
    def cross_product(a: Point, b: Point) -> Point:
        return Point(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

    @staticmethod
    def scale(p: Point) -> Point:
        divisor = math.gcd(p.x, p.y, p.z)
        return Point(p.x // divisor, p.y // divisor, p.z // divisor)

    @staticmethod
    def div(p: Point, factor: int):
        return Point(p.x // factor, p.y // factor, p.z // factor)

    @staticmethod
    def mul(p: Point, factor: int):
        return Point(p.x * factor, p.y * factor, p.z * factor)

    @staticmethod
    def sub(p1: Point, p2: Point) -> Point:
        return Point(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

    @staticmethod
    def add(p1: Point, p2: Point) -> Point:
        return Point(p1.x + p2.x, p1.y + p2.y, p1.z + p2.z)

    @staticmethod
    def future_position(h: Hail, t: int) -> Point:
        return Point(h.point.x + t * h.delta.x, h.point.y + t * h.delta.y, h.point.z + t * h.delta.z)

    def colinear(self, p1: Point, p2: Point, p3: Point):
        delta1 = self.sub(p1, p2)
        delta2 = self.sub(p1, p3)
        # print(f'delta1 = {delta1}, delta2 = {delta2}')
        factor = delta1.x / delta2.x if delta2.x != 0 else delta1.y / delta2.y
        # print(f'Factor = {factor}')
        # print(f'{round(delta2.x * factor)} == {delta1.x}; {round(delta2.y * factor)} == {delta1.y}; {round(delta2.z * factor)} == {delta1.z}')
        return round(delta2.x * factor) == delta1.x and round(delta2.y * factor) == delta1.y and round(delta2.z * factor) == delta1.z

    @staticmethod
    def time_of_intersection(hail: Hail, m: float):
        """
        We have the direction, now we need the time at a point along it -- where does v1p intersect our line?
        Our line in this reference frame is:    x = s * line.x, y = s * line.y, z = s * line.z
        v1p's line in this reference frame is:  x = v1p.point.x + t * v1p.delta.x, y = v1p.point.y + t * v1p.delta.y,
                                                z = v1p.point.z + t * v1p.delta.z
        Solve three equations for two variables s and t
            s * line.x = v1p.point.x + t * v1p.delta.x
            s * line.y = v1p.point.y + t * v1p.delta.y
            s * line.z = v1p.point.z + t * v1p.delta.z
        We know:    s = (v1p.point.x + t * v1p.delta.x) / line.x
        Therefore:  s * line.y = v1p.point.y + t * v1p.delta.y
                    ((v1p.point.x + t * v1p.delta.x) / line.x) * line.y = v1p.point.y + t * v1p.delta.y
                    (line.y / line.x) * (v1p.point.x + t * v1p.delta.x) - t * v1p.delta.y = v1p.point.y
                    let m = line.y / line.x
                    m * (v1p.point.x + t * v1p.delta.x) - t * v1p.delta.y = v1p.point.y
                    t = - (v1p.point.y - m * v1p.point.x) / (v1p.delta.y - m * v1p.delta.x)

        :param hail: a single hailstone
        :param m: slope
        :return: The time of intersection
        """
        # Time of intersection in coordinates where self.board[0] is stationary at the origin
        return int(round(-(hail.point.y - m * hail.point.x) / (hail.delta.y - m * hail.delta.x)))

    def part2(self):
        self.part = 2
        v0 = self.board[0]
        v1 = self.board[1]
        v2 = self.board[2]

        # Translate so that v0 is always at the origin of (x, y, y):
        # This means hails #2 and #3 each form a plane that goes through the origin
        # The intersection of these two planes gives us the line
        v1p = self.translate(v1, v0)
        v2p = self.translate(v2, v0)

        plane1_normal = self.plane_normal(v1p)  # This is the normal for the plane containing line v1 and the origin
        plane2_normal = self.plane_normal(v2p)  # This is the normal for the plane containing line v2 and the origin

        # Cross the normals for the two planes to get the direction of the line of intersection for the two planes
        line = self.cross_product(plane1_normal, plane2_normal)
        # This is the direction, let's get the smallest integral version of it by scaling by GCD
        line = self.scale(line)

        # We have the direction, now we need the time at a point along it -- where does v1p intersect our line?
        m = line.y / line.x

        # Get the time of intersection in the translated reference frame, and then get the points of intersection in
        # untranslated space
        t1 = self.time_of_intersection(v1p, m)
        t2 = self.time_of_intersection(v2p, m)
        v1_point = self.future_position(v1, t1)
        v2_point = self.future_position(v2, t2)
        if t1 > t2:
            rock_direction = self.div(self.sub(v1_point, v2_point), t1 - t2)
        else:
            rock_direction = self.div(self.sub(v2_point, v1_point), t2 - t1)
        print(f'Delta per time untranslated is: {rock_direction}')

        starting_position = self.sub(v1_point, self.mul(rock_direction, t1))
        print(f'Start point is {starting_position}')
        print(f'Sum of coordinates = {starting_position.x + starting_position.y + starting_position.z}')


if path.isfile('test_inputs/test24.txt'):
    with open('test_inputs/test24.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [li.strip() for li in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day24(test_input_lines).part1(7, 27)

print('\nFULL INPUT PART 1')
Day24(full_input_lines).part1(200000000000000, 400000000000000)

if path.isfile('test_inputs/test24.txt'):
    with open('test_inputs/test24.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day24(test_input_lines).part2()

print('\nFULL INPUT PART 2')
Day24(full_input_lines).part2()
