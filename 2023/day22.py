import re
from os import path
from typing import NamedTuple

Point = NamedTuple('Point', x=int, y=int, z=int)
Brick = NamedTuple('Brick', end1=Point, end2=Point, orient=str, number=int)


with open('inputs/input22.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day22:
    def __init__(self, lines):
        self.board = self.parse_inputs(lines)
        self.part = 0
        self.brick_steps = 0
        self.falling_brick_set = set()

    @staticmethod
    def parse_inputs(lines):
        board = []
        for cnt, l in enumerate(lines):
            m = re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', l)
            end1 = Point(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            end2 = Point(int(m.group(4)), int(m.group(5)), int(m.group(6)))

            # Make sure end1 is always has the lower coordinate value
            if end1.x != end2.x:
                if end1.x > end2.x:
                    end1, end2 = end2, end1
                board.append(Brick(end1, end2, orient='x', number=cnt))
            elif end1.y != end2.y:
                if end1.y > end2.y:
                    end1, end2 = end2, end1
                board.append(Brick(end1, end2, orient='y', number=cnt))
            elif end1.z != end2.z:
                if end1.z > end2.z:
                    end1, end2 = end2, end1
                board.append(Brick(end1, end2, orient='z', number=cnt))
            else:
                board.append(Brick(end1, end2, orient='-', number=cnt))

        return board

    @staticmethod
    def is_supporting(b1: Brick, b2: Brick):
        """
        Return True if b2 is supporting b1, False otherwise
        """
        # print(f'Comparing {b1.name} and {b2.name}')

        # To be supporting, the bottom of b2 has to be one below the top of b1
        if b2.end2.z + 1 != b1.end1.z:
            return False

        # Do the two bricks intersect in x,y?
        if b1.orient == b2.orient:
            # If orientations are the same, comparison is easy, look for overlap in the orientation coord
            if b1.orient == 'x':
                return b1.end1.y == b2.end1.y and b1.end1.x <= b2.end2.x and b2.end1.x <= b1.end2.x
            elif b1.orient == 'y':
                return b1.end1.x == b2.end1.x and b1.end1.y <= b2.end2.y and b2.end1.y <= b1.end2.y
            else:  # 'z' or single cube
                return b1.end1.x == b2.end1.x and b1.end1.y == b2.end1.y

        if b1.orient == 'x':  # b2 is 'y' or 'z' or single cube
            return b1.end1.x <= b2.end1.x <= b1.end2.x and b2.end1.y <= b1.end1.y <= b2.end2.y
        elif b1.orient == 'y':  # b2 is 'x' or 'z' or single cube
            return b1.end1.y <= b2.end1.y <= b1.end2.y and b2.end1.x <= b1.end1.x <= b2.end2.x
        else:  # b1 is 'z' or single cube
            if b2.orient == 'x':
                return b2.end1.x <= b1.end1.x <= b2.end2.x and b1.end1.y == b2.end1.y
            elif b2.orient == 'y':
                return b2.end1.y <= b1.end1.y <= b2.end2.y and b1.end1.x == b2.end1.x
            else:
                return b1.end1.x == b2.end1.x and b1.end1.y == b2.end1.y

    def get_supporter_list(self, brick: Brick) -> set[Brick]:
        if brick.end1.z == 1:
            return {Brick(end1=(500, 500, 0), end2=(-500, -500, 0), orient='xy', number=-1)}

        return set([b for b in self.board if b != brick and self.is_supporting(brick, b)])

    def gravity(self) -> dict[Brick, set[Brick]]:
        changed = True
        supporter_map = {}
        while changed:
            changed = False
            supporter_map = {}
            for brick in self.board.copy():
                supporters_list = self.get_supporter_list(brick)
                if len(supporters_list) == 0:
                    # print(f'Brick is not supported and will drop one z: {brick}')
                    self.brick_steps += 1
                    changed = True
                    self.falling_brick_set.add(brick.number)
                    self.board.remove(brick)
                    self.board.append(Brick(Point(brick.end1.x, brick.end1.y, brick.end1.z - 1),
                                            Point(brick.end2.x, brick.end2.y, brick.end2.z - 1),
                                            orient=brick.orient, number=brick.number))
                supporter_map[brick] = set(supporters_list)
        return supporter_map

    def part1(self):
        self.part = 1
        supporter_map = self.gravity()
        print(f'{len(self.falling_brick_set)} bricks fell a total of {self.brick_steps} steps to settle')
        # print(supporter_map)
        possible_supporters = self.board.copy()
        for key, value in supporter_map.items():
            if len(value) == 1:
                one_item = list(value)[0]
                if one_item in possible_supporters:
                    possible_supporters.remove(one_item)
        print(f'Safe to zap: {len(possible_supporters)} bricks')

    @staticmethod
    def check_remove(brick: Brick, supporter_map: dict[Brick, set[Brick]]):
        altered = True
        removed_set = {brick}
        while altered:
            altered = False
            for key, supporter_list in supporter_map.items():
                if key not in removed_set and all([b in removed_set for b in supporter_list]):
                    altered = True
                    removed_set.add(key)

        # print(f'Removing {brick}, {len(removed_set) - 1} bricks can fall')
        return len(removed_set) - 1

    def part2(self):
        self.part = 2
        supporter_map = self.gravity()
        print(f'{len(self.falling_brick_set)} bricks fell a total of {self.brick_steps} steps to settle')

        # See how many bricks fall as we delete each brick in isolation, but count chain reactions
        total_bricks = 0
        for b in self.board:
            total_bricks += self.check_remove(b, supporter_map)
        print(f'Removing each brick 1 at a time, {total_bricks} total bricks can fall')


if path.isfile('test_inputs/test22.txt'):
    with open('test_inputs/test22.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day22(test_input_lines).part1()

print('\nFULL INPUT PART 1')
Day22(full_input_lines).part1()

if path.isfile('test_inputs/test22.txt'):
    with open('test_inputs/test22.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day22(test_input_lines).part2()

print('\nFULL INPUT PART 2')
Day22(full_input_lines).part2()
